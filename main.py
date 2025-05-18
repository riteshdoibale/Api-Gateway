from flask import Flask
from app.configs.database import DatabaseConnection
from app.utils.middleware import Middleware
DatabaseConnection.establish_db_connection()
from app.configs.database import Base, engine
Base.metadata.create_all(engine)



app = Flask(__name__)
app.wsgi_app = Middleware(app.wsgi_app)


from app.controllers.auth_controller import auth_app
from app.controllers.data_controller import data_app
from app.controllers.communication_controller import communication_app
from app.controllers.audit_controller import audit_app

app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(data_app, url_prefix='/data')
app.register_blueprint(communication_app, url_prefix='/communication')
app.register_blueprint(audit_app, url_prefix='/audit')


if __name__ == '__main__':
    app.run(debug=True)