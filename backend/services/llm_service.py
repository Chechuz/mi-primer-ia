import os
from langchain_community.llms import Ollama 

class LLMService:
    def __init__(self, model_name='llama3.1', upload_folder="uploads", mock_mode=False):
        if mock_mode:
            self.llm = None  # En modo mock, no se configura el modelo real
        else:
            self.llm = Ollama(model=model_name)
        self.upload_folder = upload_folder
        self.mock_mode = mock_mode

    def get_text_from_request(self, data):
        """
        Extrae el texto desde un JSON, ya sea proporcionado directamente
        o a través del nombre de un archivo en 'uploads'.
        """
        if 'text' in data :
            return data
        elif 'file_name' in data and data['file_name']:
            if not self.upload_folder:
                raise ValueError("No se configuró la carpeta de uploads")
            
            file_path = os.path.join(self.upload_folder, data['file_name'])
            if not os.path.exists(file_path):
                raise ValueError(f"El archivo {data['file_name']} no existe")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            raise ValueError("Se debe proporcionar texto o un archivo válido")

    def chat(self, prompt):
        if not prompt.strip():
            raise ValueError("El mensaje no puede estar vacío")
        if self.mock_mode:
            return "Mock response for chat"
        response = self.llm.invoke(prompt)
        return response

    def summarize(self, text):
        if not text.strip():
            raise ValueError("El texto para resumir no puede estar vacío")
        prompt = f"Por favor, genera un resumen breve del siguiente texto:\n\n{text}"
        if self.mock_mode:
            return "Resumen generado"
        response = self.llm(prompt)
        return response

    def translate(self, text, target_language):
        if not text:
            raise ValueError("El texto para traducir no puede estar vacío")
        if not target_language:
            raise ValueError("Debe especificar un idioma de destino")
        prompt = f"Por favor, traduce el siguiente texto al {target_language}:\n\n{text}"
        if self.mock_mode:
            return "Texto traducido"
        response = self.llm(prompt)
        return response
