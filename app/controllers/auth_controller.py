import uuid
from flask import Blueprint, request
from sqlalchemy.orm import Session
from app.configs.database import DatabaseConnection

from app.models.auth_model import SignUpModel, SignInModel
from app.services.auth_service import AuthService
from app.utils.standard_response import responseModel

auth_app = Blueprint('auth', __name__)


@auth_app.route('/signup', methods=['POST'])
def signUp(request=request, model=SignUpModel, db: Session = DatabaseConnection.get_db_connection()):
    payload = model(**request.get_json()).dict()
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    print(trackingId)
    error, data = AuthService(trackingId, db, payload).createUser()
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])


@auth_app.route('/login', methods=['POST'])
def logIn(request=request, model=SignInModel, db: Session = DatabaseConnection.get_db_connection()):
    payload = model(**request.get_json()).dict()
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    print(trackingId)
    error, data = AuthService(trackingId, db, payload).verifyUser()
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])


@auth_app.route('/forgotpassword', methods=['GET'])
def forgotPassword(request=request, db: Session = DatabaseConnection.get_db_connection()):
    queryParams = (request.args).to_dict()
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    print(trackingId)
    error, data = AuthService(trackingId, db, queryParams).checkUserExists()
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])


@auth_app.route('/resetpassword', methods=['POST'])
def resetpassword(request=request, model=SignInModel, db: Session = DatabaseConnection.get_db_connection()):
    payload = model(**request.get_json()).dict()
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    print(trackingId)
    error, data = AuthService(trackingId, db, payload).storeNewPass()
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])