import unittest
from services.file_service import FileService
from werkzeug.datastructures import FileStorage
import os

class TestFileService(unittest.TestCase):
    def setUp(self):
        # Crear carpeta de prueba
        self.upload_folder = "test_uploads"
        os.makedirs(self.upload_folder, exist_ok=True)
        self.file_service = FileService(upload_folder=self.upload_folder)

    def tearDown(self):
        # Eliminar archivos y carpeta después de las pruebas
        for file in os.listdir(self.upload_folder):
            os.remove(os.path.join(self.upload_folder, file))
        os.rmdir(self.upload_folder)

    def test_validate_file_success(self):
        # Caso: archivo válido
        file_name = "valid.txt"
        content = "Texto de prueba"
        file_path = os.path.join(self.upload_folder, file_name)

        # Crear el archivo de prueba
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        # Simular un archivo Flask usando FileStorage
        with open(file_path, "rb") as file:
            file_storage = FileStorage(
                stream=file,
                filename=file_name,
                content_type="text/plain"
        )
            result = self.file_service.validate_file(file_storage)
        self.assertEqual(result, content)

    def test_validate_file_invalid_extension(self):
        # Caso: archivo con extensión inválida
        file_name = "invalid.pdf"
        content = "Texto de prueba"
        file_path = os.path.join(self.upload_folder, file_name)

        # Crear el archivo de prueba
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        # Simular un archivo Flask usando FileStorage
        with open(file_path, "rb") as file:
            file_storage = FileStorage(
                stream=file,
                filename=file_name,
                content_type="application/pdf"
            )
            with self.assertRaises(ValueError) as context:
                self.file_service.validate_file(file_storage)
            self.assertEqual(str(context.exception), "Formato de archivo no permitido. Solo se aceptan archivos .txt")

    def test_validate_file_empty(self):
        # Caso: archivo vacío
        file_name = "empty.txt"
        file_path = os.path.join(self.upload_folder, file_name)

        # Crear un archivo vacío
        with open(file_path, "w", encoding="utf-8") as file:
            pass

        # Simular un archivo Flask usando FileStorage
        with open(file_path, "rb") as file:
            file_storage = FileStorage(
                stream=file,
                filename=file_name,
                content_type="text/plain"
            )
            with self.assertRaises(ValueError) as context:
                self.file_service.validate_file(file_storage)
            self.assertEqual(str(context.exception), "El fichero subido se encuentra vacío")

    def test_save_file(self):
        # Caso: guardar archivo correctamente
        file_name = "save_test.txt"
        content = "Texto de prueba para guardar"
        file_path = os.path.join(self.upload_folder, file_name)

        # Crear el archivo de prueba
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        # Simular un archivo Flask usando FileStorage
        with open(file_path, "rb") as file:
            file_storage = FileStorage(
                stream=file,
                filename=file_name,
                content_type="text/plain"
            )
            saved_path = self.file_service.save_file(file_storage)
            self.assertTrue(os.path.exists(saved_path))


if __name__ == '__main__':
    unittest.main()
