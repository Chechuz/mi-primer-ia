import unittest
from unittest.mock import MagicMock, patch
from services.llm_service import LLMService
import os

class TestLLMService(unittest.TestCase):

    def setUp(self):
        # Configuración inicial para las pruebas
        self.upload_folder = "test_uploads"
        os.makedirs(self.upload_folder, exist_ok=True)
        self.llm_service = LLMService(upload_folder=self.upload_folder, mock_mode=True)

    def tearDown(self):
        # Limpieza después de las pruebas
        for file in os.listdir(self.upload_folder):
            os.remove(os.path.join(self.upload_folder, file))
        os.rmdir(self.upload_folder)

    def test_get_text_from_request_with_text(self):
        # Caso: texto proporcionado directamente
        data = {"text": "Texto directo para la prueba"}
        result = self.llm_service.get_text_from_request(data)
        self.assertEqual(result, data["text"])

    def test_get_text_from_request_with_file(self):
        # Caso: texto proporcionado desde un archivo
        file_name = "test.txt"
        file_content = "Texto de prueba desde un archivo"
        file_path = os.path.join(self.upload_folder, file_name)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(file_content)

        data = {"file_name": file_name}
        result = self.llm_service.get_text_from_request(data)
        self.assertEqual(result, file_content)

    def test_get_text_from_request_no_text_or_file(self):
        # Caso: ni texto ni archivo proporcionado
        data = {}
        with self.assertRaises(ValueError) as context:
            self.llm_service.get_text_from_request(data)
        self.assertEqual(str(context.exception), "Se debe proporcionar texto o un archivo válido")

    def test_get_text_from_request_file_not_found(self):
        # Caso: archivo no existente
        data = {"file_name": "inexistente.txt"}
        with self.assertRaises(ValueError) as context:
            self.llm_service.get_text_from_request(data)
        self.assertTrue("no existe" in str(context.exception))

    @patch('services.llm_service.Ollama')
    def test_summarize(self, MockOllama):
        # Caso: resumen exitoso con un modelo simulado
        mock_instance = MockOllama.return_value
        mock_instance.return_value = {"content": "Resumen generado"}

        result = self.llm_service.summarize("Texto a resumir")
        self.assertEqual(result, "Resumen generado")

    @patch('services.llm_service.Ollama')
    def test_translate(self, MockOllama):
        # Caso: traducción exitosa con un modelo simulado
        mock_instance = MockOllama.return_value
        mock_instance.return_value = {"content": "Texto traducido"}

        result = self.llm_service.translate("Texto a traducir", "inglés")
        self.assertEqual(result, "Texto traducido")


if __name__ == '__main__':
    unittest.main()
