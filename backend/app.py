from flask import Flask
from controllers.app_controller import app_controller

app = Flask(__name__)

# Registrar el controlador
app.register_blueprint(app_controller)

if __name__ == '__main__':
    app.run(debug=True)

