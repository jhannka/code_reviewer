import os
import sys
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_env_vars():
    """Lee las variables del archivo .env local."""
    env_path = os.path.join("code_reviewer", ".env")
    vars = {}
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        vars[key.strip()] = val.strip()
        except Exception as e:
            print(f"Error al leer .env: {str(e)}")
    return vars

def save_env_vars(vars):
    """Guarda las variables en el archivo .env local."""
    env_path = os.path.join("code_reviewer", ".env")
    try:
        with open(env_path, "w", encoding="utf-8") as f:
            for key, val in vars.items():
                f.write(f"{key}={val}\n")
    except Exception as e:
        print(f"Error al escribir en .env: {str(e)}")

def run_agent_query(query: str):
    """Ejecuta el agente ADK usando la CLI compartiendo la terminal interactiva."""
    adk_path = os.path.join(".venv", "bin", "adk")
    if not os.path.exists(adk_path):
        # Intentar en Windows
        adk_path = os.path.join(".venv", "Scripts", "adk")
        if not os.path.exists(adk_path):
            print("\n❌ Error: No se encontró el ejecutable de ADK en el entorno virtual.")
            print("Asegurate de haber creado el entorno virtual '.venv' e instalado los paquetes.")
            return
            
    print(f"\n🚀 Iniciando revisión: '{query}'\n")
    try:
        # Usamos subprocess.run permitiendo que herede stdin, stdout y stderr
        # para que el usuario pueda interactuar con el agente en tiempo real.
        result = subprocess.run([adk_path, "run", "code_reviewer", query])
        if result.returncode != 0:
            print("\n⚠️  El agente terminó con algún error (código de salida diferente de 0).")
    except KeyboardInterrupt:
        print("\n\n(Revisión cancelada por el usuario)")
    except Exception as e:
        print(f"\n❌ Error al ejecutar el agente: {str(e)}")

def menu():
    while True:
        clear_screen()
        print("==================================================")
        print("      AGENTE ARQUITECTO - MENÚ DE REVISIÓN        ")
        print("==================================================")
        print("1. Revisar cambios de Git (pendientes de commit)")
        print("2. Revisar un archivo de código específico")
        print("3. Analizar y listar las directivas (skills)")
        print("4. Configurar API Key y Modelo de Gemini")
        print("5. Salir")
        print("==================================================")
        
        try:
            opcion = input("Seleccioná una opción [1-5]: ").strip()
        except KeyboardInterrupt:
            print("\n¡Chau!")
            break
            
        if opcion == "1":
            clear_screen()
            print("--- REVISANDO CAMBIOS PENDIENTES DE GIT ---")
            query = "Analizá todos los cambios pendientes de commit (git diff) usando 'get_git_changes'. Revisalos según las skills del proyecto y mostrá el informe."
            run_agent_query(query)
            input("\nPresioná Enter para volver al menú...")
            
        elif opcion == "2":
            clear_screen()
            print("--- REVISAR ARCHIVO ESPECÍFICO ---")
            file_path = input("Ingresá la ruta del archivo (relativa al proyecto, ej: code_reviewer/agent.py): ").strip()
            if not file_path:
                print("Ruta vacía. Cancelando operación.")
                input("\nPresioná Enter para volver al menú...")
                continue
                
            if not os.path.exists(file_path):
                print(f"\n❌ El archivo '{file_path}' no existe en el disco.")
                input("\nPresioná Enter para volver al menú...")
                continue
                
            query = f"Leé y analizá el archivo '{file_path}' usando 'read_source_file'. Revisalo minuciosamente de acuerdo a las skills del proyecto y presentá el informe."
            run_agent_query(query)
            input("\nPresioná Enter para volver al menú...")
            
        elif opcion == "3":
            clear_screen()
            print("--- ANALIZAR Y LISTAR SKILLS ---")
            query = "Leé todas las skills del proyecto usando 'read_project_skills', listalas y generá un breve resumen explicativo de cada una."
            run_agent_query(query)
            input("\nPresioná Enter para volver al menú...")
            
        elif opcion == "4":
            clear_screen()
            print("--- CONFIGURAR API KEY Y MODELO ---")
            vars = load_env_vars()
            current_key = vars.get("GOOGLE_API_KEY", "")
            current_model = vars.get("GEMINI_MODEL", "gemini-3.5-flash")
            
            # Ofuscar clave para mostrar
            if current_key and current_key != "placeholder_key":
                display_key = current_key[:4] + "..." + current_key[-4:] if len(current_key) > 8 else "Configurada"
            else:
                display_key = "No configurada (placeholder)"
                
            print("Estado actual:")
            print(f"- Google API Key: {display_key}")
            print(f"- Modelo de Gemini: {current_model}")
            print("----------------------------------")
            
            new_key = input("\nIngresá la nueva Google API Key (presioná Enter para mantener la actual): ").strip()
            if new_key:
                vars["GOOGLE_API_KEY"] = new_key
                
            print("\nModelos de Gemini recomendados:")
            print("1. gemini-3.5-flash (Por defecto, rápido y de bajo costo)")
            print("2. gemini-2.5-flash")
            print("3. gemini-2.5-pro (Excelente para análisis de código complejo)")
            print("4. Ingresar otro modelo personalizado")
            print("5. Mantener el actual")
            
            sel = input("Seleccioná una opción para el modelo [1-5]: ").strip()
            if sel == "1":
                vars["GEMINI_MODEL"] = "gemini-3.5-flash"
            elif sel == "2":
                vars["GEMINI_MODEL"] = "gemini-2.5-flash"
            elif sel == "3":
                vars["GEMINI_MODEL"] = "gemini-2.5-pro"
            elif sel == "4":
                custom = input("Ingresá el identificador del modelo (ej: gemini-1.5-pro): ").strip()
                if custom:
                    vars["GEMINI_MODEL"] = custom
            
            # Asegurar que se guarde el flag de enterprise para evitar problemas
            if "GOOGLE_GENAI_USE_ENTERPRISE" not in vars:
                vars["GOOGLE_GENAI_USE_ENTERPRISE"] = "0"
                
            save_env_vars(vars)
            print("\n✅ Configuración guardada correctamente en 'code_reviewer/.env'.")
            input("\nPresioná Enter para volver al menú...")
            
        elif opcion == "5":
            print("\n¡Nos vemos! Éxitos en el código.")
            break
        else:
            print("\nOpción no válida. Por favor ingresá un número de 1 a 5.")
            input("\nPresioná Enter para continuar...")

if __name__ == "__main__":
    menu()
