from flask import Flask
from app.configs.database import DatabaseConnection
DatabaseConnection.establish_db_connection()
from app.configs.database import Base, engine
Base.metadata.create_all(engine)



app = Flask(__name__)


from app.controllers.auth_controller import auth_app
from app.controllers.data_controller import data_app

app.register_blueprint(auth_app)
app.register_blueprint(data_app)


if __name__ == '__main__':
    app.run(debug=True)