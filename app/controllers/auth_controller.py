from flask import Blueprint, request
from sqlalchemy.orm import Session
from app.configs.database import DatabaseConnection

from app.models.auth_model import SignUpModel, SignInModel
from app.services.auth_service import AuthService

auth_app = Blueprint('auth', __name__)


@auth_app.route('/auth/signup', methods=['POST'])
def signUp(request=request, model=SignUpModel, db: Session = DatabaseConnection.get_db_connection()):
    signup_data = model(**request.get_json())
    payload = signup_data.dict()
    error, data = AuthService(db, payload).createUser()
    if error:
        print(error)
        return error
    return data


@auth_app.route('/auth/login', methods=['POST'])
def logIn(request=request, model=SignInModel, db: Session = DatabaseConnection.get_db_connection()):
    signin_data = model(**request.get_json())
    payload = signin_data.dict()
    error, data = AuthService(db, payload).verifyUser()
    if error:
        print(error)
        return error
    return data
    

@auth_app.route('/auth/forgotpassword', methods=['GET'])
def forgotPassword(request=request, db: Session = DatabaseConnection.get_db_connection()):
    queryParams = (request.args).to_dict()
    error, data = AuthService(db, queryParams).checkUserExists()
    if error:
        print(error)
        return error
    return data
    
@auth_app.route('/auth/resetpassword', methods=['POST'])
def resetpassword(request=request, model=SignInModel, db: Session = DatabaseConnection.get_db_connection()):
    resetpass_data = model(**request.get_json())
    payload = resetpass_data.dict()
    error, data = AuthService(db, payload).storeNewPass()
    if error:
        print(error)
        return error
    return data