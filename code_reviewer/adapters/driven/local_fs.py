import os
from code_reviewer.ports.driven import FileSystemPort

class LocalFileSystemAdapter(FileSystemPort):
    def read_file(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error leyendo el archivo {file_path}: {str(e)}"

    def write_file(self, file_path: str, content: str) -> str:
        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Archivo {file_path} escrito correctamente."
        except Exception as e:
            return f"Error escribiendo en el archivo {file_path}: {str(e)}"
