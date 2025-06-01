from flask import Flask
from src.routes import bp
from src.database.database import init_db, db

app = Flask(
    __name__,
    template_folder="src/templates",
    static_folder="src/static"
)
app.secret_key = 'tu_clave_secreta_aqui'

# Inicializa la base de datos
init_db(app)

app.register_blueprint(bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)