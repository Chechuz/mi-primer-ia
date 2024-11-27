import os

class FileService:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

    def validate_file(self, file):
        # Verificar extensión
        if not file.filename.endswith('.txt'):
            raise ValueError("Formato de archivo no permitido. Solo se aceptan archivos .txt")

        # Verificar tamaño
        content = file.stream.read().decode('utf-8')
        if len(content) > 1000:
            raise ValueError("El fichero excede el tamaño máximo permitido (1000 caracteres)")

        # Verificar si está vacío
        if len(content.strip()) == 0:
            raise ValueError("El fichero subido se encuentra vacío")
        
        # Resetear el stream para permitir guardar el archivo después
        file.stream.seek(0)

        return content

    def save_file(self, file):
        file_path = os.path.join(self.upload_folder, file.filename)
        file.save(file_path)
        return file_path
