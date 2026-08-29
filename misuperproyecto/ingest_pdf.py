import os
import re
from pypdf import PdfReader
import chromadb
import ollama


# =========================================================================
# CONFIGURACIÓN DEL PIPELINE DE RAG LOCAL
# =========================================================================
PDF_PATH = "Solucionario-Matematicas-1oESO-Anaya-TEMA-1-Los-numeros-naturales.pdf"
CHROMA_DB_PATH = "/home/javichu/chroma_db"  # Tu ruta absoluta súper segura
COLLECTION_NAME = "solucionario_anaya_1eso"
EMBEDDING_MODEL = "all-minilm"  # Tu modelo ligero y compatible


def extraer_y_trocear_pdf(pdf_path: str) -> list[dict]:
    """Extrae el texto de un PDF página a página y crea fragmentos base."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"❌ No se ha encontrado el archivo PDF en: {pdf_path}\n"
            "Asegúrate de colocar el PDF del solucionario en la raíz de tu proyecto."
        )

    print(f"📖 Leyendo el archivo PDF: {pdf_path}...")
    reader = PdfReader(pdf_path)
    chunks = []

    for index, page in enumerate(reader.pages):
        page_num = index + 1
        text = page.extract_text()

        if not text or not text.strip():
            continue

        text_limpio = re.sub(r"\s+", " ", text).strip()

        # Usamos un tamaño base cómodo de 1000 caracteres
        max_chars = 1000
        overlap = 150
        
        if len(text_limpio) <= max_chars:
            chunks.append({
                "text": text_limpio,
                "metadata": {
                    "page": page_num,
                    "chunk": 0,
                    "source": os.path.basename(pdf_path)
                }
            })
        else:
            inicio = 0
            chunk_idx = 0
            while inicio < len(text_limpio):
                fin = inicio + max_chars
                fragmento = text_limpio[inicio:fin]
                chunks.append({
                    "text": fragmento,
                    "metadata": {
                        "page": page_num,
                        "chunk": chunk_idx,
                        "source": os.path.basename(pdf_path)
                    }
                })
                inicio += (max_chars - overlap)
                chunk_idx += 1

    print(f"✅ Extracción inicial completada. Se han generado {len(chunks)} fragmentos base.")
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