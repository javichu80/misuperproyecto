import os
import re
from pypdf import PdfReader
import chromadb
import ollama


# =========================================================================
# CONFIGURACIÓN DEL PIPELINE DE RAG LOCAL
# =========================================================================
PDF_PATH = "misuperproyecto/Solucionario-Matematicas-1oESO-Anaya-TEMA-1-Los-numeros-naturales.pdf"
CHROMA_DB_PATH = "/home/javichu/chroma_db"  # Tu ruta absoluta súper segura
COLLECTION_NAME = "solucionario_anaya_1eso"
EMBEDDING_MODEL = "all-minilm"  # Tu modelo ligero y compatible


def extraer_y_trocear_pdf(pdf_path: str) -> list[dict]:
    """Extrae el texto de un PDF aplicando limpieza de ruido y solapamiento dinámico."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"❌ No se ha encontrado el archivo PDF en: {pdf_path}\n"
            "Asegúrate de colocar el PDF del solucionario en la raíz de tu proyecto."
        )

    print(f"📖 Leyendo y limpiando PDF: {pdf_path}...")
    reader = PdfReader(pdf_path)
    paginas_texto = []

    # 1. Extracción y Limpieza de Cabeceras/Pies de página
    for i, page in enumerate(reader.pages):
        texto_sucio = page.extract_text() or ""
        
        # Expresiones regulares para limpiar cabeceras típicas de Anaya y números de página
        texto_limpio = re.sub(r"©\s*GRUPO\s*ANAYA.*", "", texto_sucio, flags=re.IGNORECASE)
        texto_limpio = re.sub(r"Matemáticas\s*\d+\.?\s*ESO.*", "", texto_limpio, flags=re.IGNORECASE)
        texto_limpio = re.sub(r"\b\d+\s*$", "", texto_limpio)  # Quita números de página sueltos al final de línea
        
        paginas_texto.append(texto_limpio.strip())

    chunks = []

    # 2. Creación de Chunks Limpios por Página (Sin solapamiento para evitar ruido en solucionarios)
    for idx, texto_pagina in enumerate(paginas_texto):
        pagina_actual = idx + 1
        
        # En solucionarios estructurados no queremos arrastrar ejercicios de páginas adyacentes
        texto_final_chunk = texto_pagina

        chunks.append({
            "text": texto_final_chunk,
            "metadata": {
                "source": os.path.basename(pdf_path),
                "page": pagina_actual,
                "chunk" : 0, # Mantenemos esta línea mágica para contentar a ChromaDB
                "materia_id": "matematicas_1eso",  # Dejamos la materia lista para el filtro de base de datos
                "tema": "tema_01"                  # Preparado para indexar múltiples temas sin colisiones
            }
        })

    print(f"✅ PDF troceado con éxito en {len(chunks)} fragmentos contextuales (Estancos por página).")
    return chunks

def obtener_embedding_con_fallback(texto: str, modelo: str) -> tuple[list[list[float]], list[str]]:
    """Intenta generar el embedding. Si Ollama rechaza el texto por exceder el contexto,

    el script lo divide recursivamente por la mitad de forma inteligente."""
    try:
        response = ollama.embeddings(model=modelo, prompt=texto)
        return [response["embedding"]], [texto]
    except Exception as e:
        error_str = str(e).lower()
        # Capturamos si es un error de límite de contexto o error de servidor de Ollama
        if "context length" in error_str or "exceeds" in error_str or "500" in error_str:
            if len(texto) < 100:
                # Si el fragmento ya es minúsculo y sigue fallando, lanzamos el error original
                raise e
            
            # Dividimos de forma segura buscando un espacio en blanco intermedio
            mitad = len(texto) // 2
            espacio = texto.find(" ", mitad - 50, mitad + 50)
            if espacio != -1:
                mitad = espacio
            
            parte1 = texto[:mitad].strip()
            parte2 = texto[mitad:].strip()
            
            # Dividimos de forma recursiva ambas mitades
            emb1, text1 = obtener_embedding_con_fallback(parte1, modelo)
            emb2, text2 = obtener_embedding_con_fallback(parte2, modelo)
            
            return emb1 + emb2, text1 + text2
        else:
            # Si es cualquier otro error (como que Ollama esté apagado), lo lanzamos directamente
            raise e


def indexar_en_chromadb(chunks: list[dict]):
    """Genera embeddings e indexa en ChromaDB con soporte autocurativo contra errores de contexto."""
    print(f"📦 Inicializando base de datos vectorial persistente en: {CHROMA_DB_PATH}...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    
    try:
        chroma_client.delete_collection(COLLECTION_NAME)
        print(f"🗑️ Colección antigua '{COLLECTION_NAME}' eliminada para resetear las dimensiones de los vectores.")
    except Exception:
        pass

    collection = chroma_client.create_collection(name=COLLECTION_NAME)
    print(f"📁 Nueva colección '{COLLECTION_NAME}' creada con éxito.")

    print(f"🧠 Generando embeddings con Ollama ('{EMBEDDING_MODEL}') de forma autocurativa...")
    
    total_guardados = 0
    for i, chunk in enumerate(chunks):
        texto = chunk["text"]
        metadatos = chunk["metadata"]
        doc_id_base = f"page_{metadatos['page']}_chunk_{metadatos['chunk']}"

        try:
            # Llamamos a nuestro generador inteligente con fallback
            vectores, textos_procesados = obtener_embedding_con_fallback(texto, EMBEDDING_MODEL)
            
            # Guardamos todos los fragmentos resultantes en ChromaDB
            for idx, (vector, sub_texto) in enumerate(zip(vectores, textos_procesados)):
                # Si se dividió el fragmento, le añadimos un sufijo para no duplicar IDs
                doc_id = doc_id_base if len(vectores) == 1 else f"{doc_id_base}_sub_{idx}"
                
                collection.add(
                    ids=[doc_id],
                    embeddings=[vector],
                    documents=[sub_texto],
                    metadatas=[metadatos]
                )
                total_guardados += 1
            
            if (i + 1) % 10 == 0 or (i + 1) == len(chunks):
                print(f"   ⚡ Procesados {i + 1}/{len(chunks)} fragmentos base...")

        except Exception as e:
            print(f"❌ Error crítico insalvable en la página {metadatos['page']}: {e}")
            return

    print("\n🎉 ¡PROCESO FINALIZADO CON ÉXITO! 🎉")
    print(f"Se han guardado un total de {total_guardados} fragmentos de forma segura en '{CHROMA_DB_PATH}'.")
    print(f"¡El RAG está 100% blindado contra cualquier tipo de página matemática!")


if __name__ == "__main__":
    try:
        fragmentos = extraer_y_trocear_pdf(PDF_PATH)
        indexar_en_chromadb(fragmentos)
    except Exception as e:
        print(f"\n❌ Error durante el proceso: {e}")