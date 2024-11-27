from flask import Blueprint, request, jsonify
from services.file_service import FileService
from services.llm_service import LLMService
import os

app_controller = Blueprint('app_controller', __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
file_service = FileService(UPLOAD_FOLDER)
llm_service = LLMService()

#######------------ C H A T --------######
@app_controller.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "El mensaje es obligatorio"}), 400
        print(f"Mensaje recibido: {data['message']}") 
        
        response = llm_service.chat(data['message'])
        return jsonify({"response": response}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error inesperado: {str(e)}") 
        return jsonify({"error": "Error en el endpoint de chat"}), 500

#######------------ UPLOADS --------######

@app_controller.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        # Obtener el archivo
        if 'file' not in request.files:
            return jsonify({"error": "No se encontró un archivo en la solicitud"}), 400
        
        file = request.files['file']

        # Validar y guardar el archivo
        content = file_service.validate_file(file)
        file_path = file_service.save_file(file)

        return jsonify({
            "message": "Archivo subido con éxito",
            "file_path": file_path,
            "content": content
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error al subir el archivo"}), 500
    
#######------------ SUMMARIZE --------######

@app_controller.route('/api/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Se debe proporcionar un cuerpo JSON"}), 400

        # Extraer texto utilizando el método del servicio
        text = llm_service.get_text_from_request(data)
        summary = llm_service.summarize(text)

        return jsonify({"summary": summary}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el endpoint de resumen"}), 500

#######------------ TRANSLATE --------######

@app_controller.route('/api/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        if not data or 'language' not in data:
            return jsonify({"error": "Se debe proporcionar un idioma de destino"}), 400

        # Extraer texto utilizando el método del servicio
        text = llm_service.get_text_from_request(data)
        translation = llm_service.translate(text, data['language'])

        return jsonify({"translation": translation}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error inesperado: {str(e)}") 
        return jsonify({"error": "Error en el endpoint de traducción"}), 500
