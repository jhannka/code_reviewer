# Propuesta: Estandarizar Importaciones y Rutas

## Propósito

Resolver los errores relacionados con las importaciones y las referencias fijas (hardcoded) a la ruta de inicio del usuario para hacer que la aplicación sea portable en diferentes entornos de usuario y tiempos de ejecución del entorno virtual.

## Alcance

### Dentro del Alcance
- Refactorizar la sentencia de importación en [agent.py](file:///Users/jhanncarlos/Documents/App/My%20Apps/code_reviewer/code_reviewer/agent.py) para utilizar una importación absoluta desde `code_reviewer.tools` (o una importación relativa de paquete).
- Resolver dinámicamente la ruta de inicio fija `/Users/jhanncarlos` en [tools.py](file:///Users/jhanncarlos/Documents/App/My%20Apps/code_reviewer/code_reviewer/tools.py) utilizando `os.path.expanduser("~")`.

### Fuera del Alcance
- Modificar el funcionamiento o comportamiento general del agente.
- Introducir un mecanismo de empaquetado (como poetry o pipenv) o contenedorización.
- Modificar las interacciones del menú de la interfaz de línea de comandos (CLI).

## Capacidades

### Nuevas Capacidades
Ninguna

### Capacidades Modificadas
Ninguna

## Enfoque

- Actualizar la línea 3 de `code_reviewer/agent.py` de `from tools import ...` a `from code_reviewer.tools import ...` o `from .tools import ...`.
- Actualizar la línea 16 de `code_reviewer/tools.py` de `"/Users/jhanncarlos/.gemini/config/skills"` para utilizar `os.path.expanduser("~/.gemini/config/skills")` o `os.path.join(os.path.expanduser("~"), ".gemini/config/skills")`.
- Verificar las importaciones y rutas ejecutando la suite de pruebas unitarias y el script de la CLI.

## Áreas Afectadas

| Área | Impacto | Descripción |
|------|--------|-------------|
| [agent.py](file:///Users/jhanncarlos/Documents/App/My%20Apps/code_reviewer/code_reviewer/agent.py) | Modificado | Actualizar la ruta de importación absoluta/relativa para las herramientas locales. |
| [tools.py](file:///Users/jhanncarlos/Documents/App/My%20Apps/code_reviewer/code_reviewer/tools.py) | Modificado | Resolver el directorio de inicio dinámicamente en lugar de fijarlo en el código. |

## Riesgos

| Riesgo | Probabilidad | Mitigación |
|------|------------|------------|
| La resolución de importaciones falla al ejecutar los scripts del paquete directamente | Baja | Verificar mediante ejecución del módulo de Python y el ejecutor de pruebas existente. |
| Permisos de la ruta de inicio del usuario o estructura de carpetas diferente en otros sistemas | Baja | `os.path.expanduser` maneja de forma nativa los directorios de inicio específicos de cada plataforma. |

## Plan de Retorno (Rollback)

Revertir los cambios usando git:
```bash
git checkout -- code_reviewer/agent.py code_reviewer/tools.py
```

## Dependencias

- Ninguna

## Criterios de Éxito

- [ ] La suite de pruebas de Pytest se ejecuta con éxito usando `PYTHONPATH=.:code_reviewer .venv/bin/pytest`.
- [ ] El agente se inicializa sin errores de importación de módulos.
- [ ] La herramienta `read_project_skills` busca la ruta estándar del directorio de inicio dinámicamente.
