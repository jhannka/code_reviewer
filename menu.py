import os
import sys
import subprocess

# Obtener el directorio de instalación absoluto de este script
INSTALL_DIR = os.path.dirname(os.path.abspath(__file__))

__version__ = "1.0.0"
CLI_LANG = "es"  # Idioma por defecto

# ANSI escape codes for modern terminal coloring
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Enable virtual terminal processing on Windows natively
if os.name == 'nt':
    os.system('')

LOCALES = {
    "es": {
        "title": "AGENTE ARQUITECTO - MENÚ DE REVISIÓN",
        "opt_1": "Revisar cambios de Git (pendientes de commit)",
        "opt_2": "Revisar un archivo de código específico",
        "opt_3": "Analizar y listar las directivas (skills)",
        "opt_4": "Configurar API Key, Modelo e Idioma",
        "opt_5": "Salir",
        "status_bar": "[↑/↓] Navegar  |  [Enter] Seleccionar  |  [Esc/Q] Salir",
        "update_available": "✨ ¡NUEVA ACTUALIZACIÓN DISPONIBLE: v{}! ✨",
        "update_changes": "Cambios en esta versión:",
        "update_prompt": "¿Deseás descargar e instalar la actualización? [s/N]: ",
        "update_in_progress": "\n📦 Iniciando actualización limpia y segura...",
        "update_dirty_error": "\n❌ Error: Tenés cambios locales no committeados en el revisor de código.\nGuardá tus cambios (git stash o git commit) antes de actualizar.",
        "update_fetching": "📥 Buscando nuevas etiquetas en GitHub...",
        "update_checkout": "🔄 Cambiando a la versión {}...",
        "update_symlink": "🔄 Actualizando enlace simbólico global...",
        "update_success": "\n✅ ¡Actualización completada con éxito!\nReiniciando el programa...",
        "update_error": "\n❌ Error durante el proceso de actualización: {}\nSe recomienda realizar un 'git pull' manual.",
        "press_enter": "\nPresioná Enter para volver al menú...",
        "press_enter_continue": "\nPresioná Enter para continuar...",
        "git_title": "--- REVISANDO CAMBIOS PENDIENTES DE GIT ---",
        "git_query": "Analizá todos los cambios pendientes de commit (git diff) usando 'get_git_changes'. Revisalos según las skills del proyecto y mostrá el informe.",
        "file_title": "--- REVISAR ARCHIVO ESPECÍFICO ---",
        "file_prompt": "Ingresá la ruta del archivo a revisar: ",
        "file_empty": "Ruta vacía. Cancelando operación.",
        "file_not_exist": "\n❌ El archivo '{}' no existe en el disco.",
        "file_query": "Leé y analizá el archivo '{}' usando 'read_source_file'. Revisalo minuciosamente de acuerdo a las skills del proyecto y presentá el informe.",
        "skills_title": "--- ANALIZAR Y LISTAR SKILLS ---",
        "skills_query": "Leé todas las skills del proyecto usando 'read_project_skills', listalas y generá un breve resumen explicativo de cada una.",
        "config_title": "--- CONFIGURAR CONFIGURACIÓN ---",
        "config_status": "Estado actual:",
        "config_key": "- Google API Key: {}",
        "config_model": "- Modelo de Gemini: {}",
        "config_lang": "- Idioma actual: {}",
        "config_key_prompt": "\nIngresá la nueva Google API Key (presioná Enter para mantener la actual): ",
        "config_model_title": "\nModelos de Gemini recomendados:",
        "config_model_options": "1. gemini-3.5-flash (Por defecto, rápido y de bajo costo)\n2. gemini-2.5-flash\n3. gemini-2.5-pro (Excelente para análisis de código complejo)\n4. Ingresar otro modelo personalizado\n5. Mantener el actual",
        "config_model_prompt": "Seleccioná una opción para el modelo [1-5]: ",
        "config_lang_title": "\nIdiomas disponibles:",
        "config_lang_options": "1. Español\n2. English\n3. Mantener el actual",
        "config_lang_prompt": "Seleccioná una opción para el idioma [1-3]: ",
        "config_saved": "\n✅ Configuración guardada correctamente.",
        "not_configured": "No configurada",
        "exit_msg": "\n¡Nos vemos! Éxitos en el código.",
        "invalid_opt": "\nOpción no válida. Por favor ingresá un número de 1 a 5.",
        "running_rev": "\n🚀 Iniciando revisión: '{}'\n",
        "agent_err": "\n⚠️  El agente terminó con algún error (código de salida diferente de 0).",
        "rev_canceled": "\n\n(Revisión cancelada por el usuario)",
        "exec_err": "\n❌ Error al ejecutar el agente: {}",
        "adk_missing": "\n❌ Error: No se encontró el ejecutable de ADK en el entorno virtual.\nAsegurate de haber creado el entorno virtual '.venv' e instalado los paquetes.",
        "config_opt_key": "Clave API: {}",
        "config_opt_model": "Modelo: {}",
        "config_opt_lang": "Idioma: {}",
        "config_opt_save": "Guardar y Regresar",
        "config_opt_cancel": "Cancelar y Volver",
        "model_menu_title": "SELECCIONAR MODELO DE GEMINI",
        "model_custom": "Ingresar modelo personalizado...",
        "lang_menu_title": "SELECCIONAR IDIOMA DEL CLI",
        "back": "Regresar",
        "custom_model_prompt": "Ingresá el identificador del modelo (ej: gemini-1.5-pro): "
    },
    "en": {
        "title": "ARCHITECT AGENT - CODE REVIEW MENU",
        "opt_1": "Review Git Changes (uncommitted diffs)",
        "opt_2": "Review a specific code file",
        "opt_3": "Analyze and list design guidelines (skills)",
        "opt_4": "Configure API Key, Model & Language",
        "opt_5": "Exit",
        "status_bar": "[↑/↓] Navigate  |  [Enter] Select  |  [Esc/Q] Exit",
        "update_available": "✨ NEW UPDATE AVAILABLE: v{}! ✨",
        "update_changes": "Changes in this version:",
        "update_prompt": "Do you want to download and install the update? [y/N]: ",
        "update_in_progress": "\n📦 Starting clean and safe update...",
        "update_dirty_error": "\n❌ Error: You have uncommitted changes in your code reviewer repository.\nStash or commit your changes before updating to prevent loss.",
        "update_fetching": "📥 Fetching new tags from GitHub...",
        "update_checkout": "🔄 Switching to version {}...",
        "update_symlink": "🔄 Updating global symbolic link...",
        "update_success": "\n✅ Update completed successfully!\nRestarting program...",
        "update_error": "\n❌ Error during the update process: {}\nWe recommend performing a manual 'git pull'.",
        "press_enter": "\nPress Enter to return to the menu...",
        "press_enter_continue": "\nPress Enter to continue...",
        "git_title": "--- REVIEWING UNCOMMITTED GIT CHANGES ---",
        "git_query": "Review all uncommitted git diff modifications using 'get_git_changes'. Validate them against project design skills and show the report.",
        "file_title": "--- REVIEW SPECIFIC FILE ---",
        "file_prompt": "Enter the relative path of the file to review: ",
        "file_empty": "Empty path. Canceling operation.",
        "file_not_exist": "\n❌ The file '{}' does not exist on disk.",
        "file_query": "Read and analyze the file '{}' using 'read_source_file'. Review it thoroughly based on project skills and present the report.",
        "skills_title": "--- ANALYZING AND LISTING GUIDELINES ---",
        "skills_query": "Read all project design skills using 'read_project_skills', list them, and generate a brief summary of each.",
        "config_title": "--- CONFIGURE CONFIGURATION ---",
        "config_status": "Current status:",
        "config_key": "- Google API Key: {}",
        "config_model": "- Gemini Model: {}",
        "config_lang": "- Current Language: {}",
        "config_key_prompt": "\nEnter new Google API Key (press Enter to keep current): ",
        "config_model_title": "\nRecommended Gemini Models:",
        "config_model_options": "1. gemini-3.5-flash (Default, fast & cost-efficient)\n2. gemini-2.5-flash\n3. gemini-2.5-pro (Excellent for complex code reasoning)\n4. Enter custom model ID\n5. Keep current",
        "config_model_prompt": "Select an option for the model [1-5]: ",
        "config_lang_title": "\nAvailable Languages:",
        "config_lang_options": "1. Español\n2. English\n3. Keep current",
        "config_lang_prompt": "Select an option for the language [1-3]: ",
        "config_saved": "\n✅ Configuration saved successfully.",
        "not_configured": "Not configured",
        "exit_msg": "\nGoodbye! Happy coding.",
        "invalid_opt": "\nInvalid option. Please enter a number between 1 and 5.",
        "running_rev": "\n🚀 Starting review: '{}'\n",
        "agent_err": "\n⚠️  The agent exited with an error (exit code not equal to 0).",
        "rev_canceled": "\n\n(Review canceled by user)",
        "exec_err": "\n❌ Error running the agent: {}",
        "adk_missing": "\n❌ Error: ADK executable not found in virtual environment.\nMake sure you created the '.venv' directory and installed packages.",
        "config_opt_key": "API Key: {}",
        "config_opt_model": "Model: {}",
        "config_opt_lang": "Language: {}",
        "config_opt_save": "Save and Return",
        "config_opt_cancel": "Cancel and Return",
        "model_menu_title": "SELECT GEMINI MODEL",
        "model_custom": "Enter custom model ID...",
        "lang_menu_title": "SELECT CLI LANGUAGE",
        "back": "Back",
        "custom_model_prompt": "Enter custom model ID (eg: gemini-1.5-pro): "
    }
}

def t(key, *args):
    """Obtiene el texto localizado para el idioma actual."""
    lang_dict = LOCALES.get(CLI_LANG, LOCALES["es"])
    text = lang_dict.get(key, key)
    if args:
        return text.format(*args)
    return text

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_env_vars():
    """Lee las variables del archivo .env local en el directorio de instalación."""
    global CLI_LANG
    env_path = os.path.join(INSTALL_DIR, "code_reviewer", ".env")
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
    CLI_LANG = vars.get("CLI_LANG", "es").strip().lower()
    if CLI_LANG not in ["es", "en"]:
        CLI_LANG = "es"
    return vars

def save_env_vars(vars):
    """Guarda las variables en el archivo .env local en el directorio de instalación."""
    global CLI_LANG
    CLI_LANG = vars.get("CLI_LANG", CLI_LANG)
    env_path = os.path.join(INSTALL_DIR, "code_reviewer", ".env")
    try:
        with open(env_path, "w", encoding="utf-8") as f:
            for key, val in vars.items():
                f.write(f"{key}={val}\n")
    except Exception as e:
        print(f"Error al escribir en .env: {str(e)}")

def check_for_updates():
    """Verifica si hay actualizaciones en el repositorio remoto usando la API de GitHub."""
    import urllib.request
    import json
    import ssl
    
    # 1. Intentar primero obtener la última release publicada (con descripción de cambios)
    release_url = "https://api.github.com/repos/jhannka/code_reviewer/releases/latest"
    req = urllib.request.Request(release_url, headers={"User-Agent": "code-reviewer-cli"})
    try:
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=1.5, context=context) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                tag_name = data.get("tag_name", "").strip()
                body = data.get("body", "Sin descripción.")
                _prompt_update_if_needed(tag_name, body)
                return
    except Exception:
        pass

    # 2. Si falla (ej. si no hay releases publicadas aún), caer a la lista de tags
    tags_url = "https://api.github.com/repos/jhannka/code_reviewer/tags"
    req = urllib.request.Request(tags_url, headers={"User-Agent": "code-reviewer-cli"})
    try:
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=1.5, context=context) as response:
            if response.status == 200:
                tags = json.loads(response.read().decode("utf-8"))
                if tags:
                    tag_name = tags[0].get("name", "").strip()
                    body = "Hay una nueva versión disponible en GitHub. Consultá el CHANGELOG.md para ver los detalles." if CLI_LANG == "es" else "A new version is available on GitHub. Check CHANGELOG.md for details."
                    _prompt_update_if_needed(tag_name, body)
    except Exception:
        pass

def _prompt_update_if_needed(tag_name: str, body: str):
    remote_ver = tag_name.lstrip("v")
    local_ver = __version__.lstrip("v")
    if remote_ver != local_ver:
        try:
            remote_parts = [int(x) for x in remote_ver.split(".")]
            local_parts = [int(x) for x in local_ver.split(".")]
            if remote_parts > local_parts:
                _show_update_dialog(tag_name, remote_ver, body)
        except ValueError:
            if remote_ver > local_ver:
                _show_update_dialog(tag_name, remote_ver, body)

def _show_update_dialog(tag_name: str, remote_ver: str, body: str):
    print("\n==================================================")
    print(t("update_available", remote_ver))
    print("==================================================")
    print(f"{t('update_changes')}\n{body}")
    print("--------------------------------------------------")
    ans = input(t("update_prompt")).strip().lower()
    if ans in ["s", "si", "yes", "y"]:
        apply_update(tag_name)
        sys.exit(0)

def apply_update(tag_name: str):
    """Aplica la actualización de manera segura utilizando comandos de Git."""
    print(t("update_in_progress"))
    try:
        diff_status = subprocess.run(["git", "diff", "--quiet"], cwd=INSTALL_DIR)
        cached_status = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=INSTALL_DIR)
        if diff_status.returncode != 0 or cached_status.returncode != 0:
            print(t("update_dirty_error"))
            input(t("press_enter_continue"))
            return
    except Exception as e:
        print(t("update_error", str(e)))
        input(t("press_enter_continue"))
        return
        
    try:
        print(t("update_fetching"))
        subprocess.run(["git", "fetch", "--tags"], cwd=INSTALL_DIR, check=True)
        
        print(t("update_checkout", tag_name))
        subprocess.run(["git", "checkout", f"tags/{tag_name}"], cwd=INSTALL_DIR, check=True)
        
        if os.name != 'nt':
            install_sh = os.path.join(INSTALL_DIR, "install.sh")
            if os.path.exists(install_sh):
                print(t("update_symlink"))
                subprocess.run(["chmod", "+x", install_sh], cwd=INSTALL_DIR)
                sym_path = "/opt/homebrew/bin/code-reviewer"
                wrapper_path = os.path.join(INSTALL_DIR, "bin", "code-reviewer")
                if os.path.exists(sym_path):
                    subprocess.run(["ln", "-sf", wrapper_path, sym_path])
                    
        print(t("update_success"))
        input(t("press_enter_continue"))
    except Exception as e:
        print(t("update_error", str(e)))
        input(t("press_enter_continue"))

def get_key():
    """Lee una sola pulsación de tecla y retorna una cadena descriptiva."""
    if os.name == 'nt':
        import msvcrt
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            if ch2 == b'H': return "up"
            if ch2 == b'P': return "down"
            if ch2 == b'M': return "right"
            if ch2 == b'K': return "left"
            return None
        if ch == b'\r': return "enter"
        if ch == b'\x1b': return "esc"
        try:
            char = ch.decode('utf-8').lower()
            if char == 'q': return "esc"
            return char
        except Exception:
            return None
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'A': return "up"
                    if ch3 == 'B': return "down"
                    if ch3 == 'C': return "right"
                    if ch3 == 'D': return "left"
                return "esc"
            if ch == '\r' or ch == '\n': return "enter"
            if ch == 'q' or ch == 'Q': return "esc"
            return ch.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def is_interactive():
    """Retorna True si la entrada estándar es una terminal interactiva (TTY)."""
    return sys.stdin.isatty()

def select_from_menu(title: str, options: list) -> int:
    """Muestra un menú de selección interactiva y retorna el índice de la opción elegida.
    Si se presiona Esc, retorna -1.
    """
    selected_index = 0
    while True:
        clear_screen()
        print(f"{CYAN}┌──────────────────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│{BOLD} {title.center(48)} {RESET}{CYAN}│{RESET}")
        print(f"{CYAN}└──────────────────────────────────────────────────┘{RESET}")
        
        for idx, opt in enumerate(options):
            if idx == selected_index:
                print(f" {GREEN}➔ {BOLD}{opt}{RESET}")
            else:
                print(f"    {GRAY}{opt}{RESET}")
        
        print(f"{CYAN}--------------------------------------------------{RESET}")
        print(f"{GRAY}{t('status_bar')}{RESET}")
        
        key = get_key()
        if key == "up":
            selected_index = (selected_index - 1) % len(options)
        elif key == "down":
            selected_index = (selected_index + 1) % len(options)
        elif key in [str(i+1) for i in range(len(options))]:
            selected_index = int(key) - 1
            return selected_index
        elif key == "enter":
            return selected_index
        elif key == "esc":
            return -1

def run_agent_query(query: str):
    """Ejecuta el agente ADK usando la CLI compartiendo la terminal interactiva."""
    adk_path = os.path.join(INSTALL_DIR, ".venv", "bin", "adk")
    if not os.path.exists(adk_path):
        adk_path = os.path.join(INSTALL_DIR, ".venv", "Scripts", "adk")
        if not os.path.exists(adk_path):
            print(t("adk_missing"))
            return
            
    print(t("running_rev", query))
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{INSTALL_DIR}:{env.get('PYTHONPATH', '')}"
        
        result = subprocess.run([adk_path, "run", "code_reviewer", query], env=env)
        if result.returncode != 0:
            print(t("agent_err"))
    except KeyboardInterrupt:
        print(t("rev_canceled"))
    except Exception as e:
        print(t("exec_err", str(e)))

def execute_option(choice: int):
    """Ejecuta la acción asociada al número de opción elegido."""
    if choice == 1:
        clear_screen()
        print(f"{CYAN}{t('git_title')}{RESET}")
        run_agent_query(t("git_query"))
        input(t("press_enter"))
        
    elif choice == 2:
        clear_screen()
        print(f"{CYAN}{t('file_title')}{RESET}")
        file_path = input(t("file_prompt")).strip()
        if not file_path:
            print(t("file_empty"))
            input(t("press_enter"))
            return
            
        if not os.path.exists(file_path):
            print(t("file_not_exist", file_path))
            input(t("press_enter"))
            return
            
        run_agent_query(t("file_query", file_path))
        input(t("press_enter"))
        
    elif choice == 3:
        clear_screen()
        print(f"{CYAN}{t('skills_title')}{RESET}")
        run_agent_query(t("skills_query"))
        input(t("press_enter"))
        
    elif choice == 4:
        configure_settings()
        
    elif choice == 5:
        print(t("exit_msg"))

def configure_settings_interactive():
    """Panel de configuración interactiva con submenús y confirmación explícita."""
    vars = load_env_vars()
    temp_key = vars.get("GOOGLE_API_KEY", "")
    temp_model = vars.get("GEMINI_MODEL", "gemini-3.5-flash")
    temp_lang = vars.get("CLI_LANG", "es").strip().lower()
    
    selected_index = 0
    while True:
        if temp_key and temp_key != "placeholder_key":
            display_key = temp_key[:4] + "..." + temp_key[-4:] if len(temp_key) > 8 else "Configured"
        else:
            display_key = t("not_configured") + " (placeholder)"
            
        display_lang = "Español" if temp_lang == "es" else "English"
        
        rendered_options = [
            f"[{1}] {t('config_opt_key', display_key)}",
            f"[{2}] {t('config_opt_model', temp_model)}",
            f"[{3}] {t('config_opt_lang', display_lang)}",
            f"[{4}] {t('config_opt_save')}",
            f"[{5}] {t('config_opt_cancel')}"
        ]
        
        clear_screen()
        print(f"{CYAN}┌──────────────────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│{BOLD} {t('config_title').center(48)} {RESET}{CYAN}│{RESET}")
        print(f"{CYAN}└──────────────────────────────────────────────────┘{RESET}")
        
        for idx, opt in enumerate(rendered_options):
            if idx == selected_index:
                print(f" {GREEN}➔ {BOLD}{opt}{RESET}")
            else:
                print(f"    {GRAY}{opt}{RESET}")
        
        print(f"{CYAN}--------------------------------------------------{RESET}")
        print(f"{GRAY}{t('status_bar')}{RESET}")
        
        key = get_key()
        if key == "up":
            selected_index = (selected_index - 1) % len(rendered_options)
            continue
        elif key == "down":
            selected_index = (selected_index + 1) % len(rendered_options)
            continue
        elif key in ["1", "2", "3", "4", "5"]:
            selected_index = int(key) - 1
            action = selected_index
        elif key == "enter":
            action = selected_index
        elif key == "esc":
            action = 4
        else:
            continue
            
        if action == 0:  # API Key
            clear_screen()
            print(f"{CYAN}--- {t('config_opt_key', '')} ---{RESET}")
            new_key = input(t("config_key_prompt")).strip()
            if new_key:
                temp_key = new_key
                
        elif action == 1:  # Model Selector Submenu
            model_options = [
                "gemini-3.5-flash",
                "gemini-2.5-flash",
                "gemini-2.5-pro",
                t("model_custom"),
                t("back")
            ]
            idx_model = select_from_menu(t("model_menu_title"), model_options)
            if idx_model >= 0 and idx_model < 3:
                temp_model = model_options[idx_model]
            elif idx_model == 3:
                clear_screen()
                custom = input(t("custom_model_prompt")).strip()
                if custom:
                    temp_model = custom
                    
        elif action == 2:  # Language Selector Submenu
            lang_options = [
                "Español",
                "English",
                t("back")
            ]
            idx_lang = select_from_menu(t("lang_menu_title"), lang_options)
            if idx_lang == 0:
                temp_lang = "es"
                global CLI_LANG
                CLI_LANG = "es"
            elif idx_lang == 1:
                temp_lang = "en"
                CLI_LANG = "en"
                
        elif action == 3:  # Guardar
            vars["GOOGLE_API_KEY"] = temp_key
            vars["GEMINI_MODEL"] = temp_model
            vars["CLI_LANG"] = temp_lang
            save_env_vars(vars)
            print(t("config_saved"))
            input(t("press_enter"))
            break
            
        elif action == 4:  # Cancelar
            load_env_vars()  # Recarga el idioma original de .env
            break

def configure_settings_non_interactive():
    """Configuración secuencial fallback para entornos no-interactivos."""
    vars = load_env_vars()
    current_key = vars.get("GOOGLE_API_KEY", "")
    current_model = vars.get("GEMINI_MODEL", "gemini-3.5-flash")
    current_lang = vars.get("CLI_LANG", "es").strip().lower()
    
    if current_key and current_key != "placeholder_key":
        display_key = current_key[:4] + "..." + current_key[-4:] if len(current_key) > 8 else "Configured"
    else:
        display_key = t("not_configured") + " (placeholder)"
        
    print(t("config_status"))
    print(t("config_key", display_key))
    print(t("config_model", current_model))
    print(t("config_lang", "Español" if current_lang == "es" else "English"))
    print("----------------------------------")
    
    new_key = input(t("config_key_prompt")).strip()
    if new_key:
        vars["GOOGLE_API_KEY"] = new_key
        
    print(t("config_model_title"))
    print(t("config_model_options"))
    
    sel = input(t("config_model_prompt")).strip()
    if sel == "1":
        vars["GEMINI_MODEL"] = "gemini-3.5-flash"
    elif sel == "2":
        vars["GEMINI_MODEL"] = "gemini-2.5-flash"
    elif sel == "3":
        vars["GEMINI_MODEL"] = "gemini-2.5-pro"
    elif sel == "4":
        custom = input("Enter custom model ID (eg: gemini-1.5-pro): ").strip()
        if custom:
            vars["GEMINI_MODEL"] = custom
            
    print(t("config_lang_title"))
    print(t("config_lang_options"))
    
    sel_lang = input(t("config_lang_prompt")).strip()
    if sel_lang == "1":
        vars["CLI_LANG"] = "es"
    elif sel_lang == "2":
        vars["CLI_LANG"] = "en"
        
    if "GOOGLE_GENAI_USE_ENTERPRISE" not in vars:
        vars["GOOGLE_GENAI_USE_ENTERPRISE"] = "0"
        
    save_env_vars(vars)
    print(t("config_saved"))
    input(t("press_enter"))

def configure_settings():
    """Elige el flujo de configuración según el tipo de terminal."""
    if is_interactive():
        configure_settings_interactive()
    else:
        configure_settings_non_interactive()

def menu_interactive():
    """Loop del menú interactivo principal por teclado."""
    selected_index = 0
    options = ["opt_1", "opt_2", "opt_3", "opt_4", "opt_5"]
    
    while True:
        clear_screen()
        print(f"{CYAN}┌──────────────────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│{BOLD} {t('title').center(48)} {RESET}{CYAN}│{RESET}")
        print(f"{CYAN}└──────────────────────────────────────────────────┘{RESET}")
        
        for idx, opt_key in enumerate(options):
            if idx == selected_index:
                print(f" {GREEN}➔ {BOLD}[{idx+1}] {t(opt_key)}{RESET}")
            else:
                print(f"    {GRAY}[{idx+1}] {t(opt_key)}{RESET}")
        
        print(f"{CYAN}--------------------------------------------------{RESET}")
        print(f"{GRAY}{t('status_bar')}{RESET}")
        
        key = get_key()
        if key == "up":
            selected_index = (selected_index - 1) % len(options)
        elif key == "down":
            selected_index = (selected_index + 1) % len(options)
        elif key in ["1", "2", "3", "4", "5"]:
            selected_index = int(key) - 1
            execute_option(selected_index + 1)
            if selected_index == 4:
                break
        elif key == "enter":
            execute_option(selected_index + 1)
            if selected_index == 4:
                break
        elif key == "esc":
            execute_option(5)
            break

def menu_non_interactive():
    """Fallback del menú no-interactivo para pipelines o tuberías."""
    while True:
        clear_screen()
        print("==================================================")
        print(f"      {t('title')}        ")
        print("==================================================")
        print(f"1. {t('opt_1')}")
        print(f"2. {t('opt_2')}")
        print(f"3. {t('opt_3')}")
        print(f"4. {t('opt_4')}")
        print(f"5. {t('opt_5')}")
        print("==================================================")
        
        try:
            opcion = input("Seleccioná una opción [1-5]: ").strip()
        except KeyboardInterrupt:
            print(t("exit_msg"))
            break
        except EOFError:
            break
            
        if opcion in ["1", "2", "3", "4", "5"]:
            execute_option(int(opcion))
            if opcion == "5":
                break
        else:
            print(t("invalid_opt"))
            input(t("press_enter_continue"))

def menu():
    load_env_vars()
    check_for_updates()
    if is_interactive():
        menu_interactive()
    else:
        menu_non_interactive()

if __name__ == "__main__":
    menu()
