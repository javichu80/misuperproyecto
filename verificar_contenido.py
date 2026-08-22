import os
import sys

# Intentamos importar PyYAML de forma segura
try:
    import yaml
except ImportError:
    print("❌ ERROR: No tienes instalada la librería 'pyyaml' en tu entorno virtual.")
    print("Por favor, actívalo y ejecuta en tu terminal: pip install pyyaml")
    sys.exit(1)

def verificar_estructura_stem():
    print("🔍 Iniciando verificación de estructura de contenidos STEM...\n")
    
    # Definición de rutas según el Blueprint
    base_dir = "courses/matematicas_1eso"
    tema_dir = os.path.join(base_dir, "tema_01_numeros_naturales")
    
    # 1. Verificar existencia de directorios
    dirs_a_comprobar = [base_dir, tema_dir]
    for d in dirs_a_comprobar:
        if os.path.exists(d):
            print(f"✅ Directorio encontrado: '{d}'")
        else:
            print(f"❌ ERROR: El directorio '{d}' no existe.")
            print(f"   Tip: Creadlo usando: mkdir -p {d}")
            return False
            
    # 2. Verificar y leer course.yaml (Estructura del Curso)
    course_yaml_path = os.path.join(base_dir, "course.yaml")
    if os.path.exists(course_yaml_path):
        print(f"✅ Archivo encontrado: '{course_yaml_path}'")
        try:
            with open(course_yaml_path, "r", encoding="utf-8") as f:
                course_data = yaml.safe_load(f)
                print(f"   📖 ID de Curso: {course_data.get('course_id')}")
                print(f"   📖 Título del Curso: {course_data.get('title')}")
                print(f"   📖 Descripción: {course_data.get('description')}")
                print(f"   📂 Temas definidos: {[t['title'] for t in course_data.get('topics', [])]}")
        except Exception as e:
            print(f"💥 ERROR al procesar '{course_yaml_path}': {e}")
            return False
    else:
        print(f"❌ ERROR: No se encuentra '{course_yaml_path}'")
        return False

    # 3. Verificar y leer metadata.yaml (Estructura de Lecciones)
    metadata_yaml_path = os.path.join(tema_dir, "metadata.yaml")
    if os.path.exists(metadata_yaml_path):
        print(f"✅ Archivo encontrado: '{metadata_yaml_path}'")
        try:
            with open(metadata_yaml_path, "r", encoding="utf-8") as f:
                metadata_data = yaml.safe_load(f)
                lessons = metadata_data.get("lessons", [])
                print(f"   📂 Lecciones mapeadas en Tema 1 ({len(lessons)} lecciones):")
                for lesson in lessons:
                    print(f"      - ID: {lesson.get('lesson_id')} -> {lesson.get('title')} ({lesson.get('file')})")
        except Exception as e:
            print(f"💥 ERROR al procesar '{metadata_yaml_path}': {e}")
            return False
    else:
        print(f"❌ ERROR: No se encuentra '{metadata_yaml_path}'")
        return False

    # 4. Verificar y leer la primera lección en Markdown
    lesson_file = os.path.join(tema_dir, "lesson_01.md")
    if os.path.exists(lesson_file):
        print(f"✅ Archivo de Lección encontrado: '{lesson_file}'")
        try:
            with open(lesson_file, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")
                # Mostramos las primeras 10 líneas de la lección
                preview = "\n".join(lines[:12])
                print(f"\n   📖 Previsualización del Markdown:\n   " + "─"*50)
                for line in lines[:12]:
                    print(f"   {line}")
                print("   " + "─"*50 + "\n")
        except Exception as e:
            print(f"💥 ERROR al abrir '{lesson_file}': {e}")
            return False
    else:
        print(f"❌ ERROR: No se encuentra '{lesson_file}'")
        return False

    print("🎉 ¡TODO PERFECTO! Tu base de datos de contenidos está lista para integrarse en el State de tu App.")
    return True

if __name__ == "__main__":
    verificar_estructura_stem()