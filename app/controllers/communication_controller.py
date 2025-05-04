
import uuid
from flask import Blueprint, request
from sqlalchemy.orm import Session

from app.configs.database import DatabaseConnection
from app.models.communication_model import ResendOtpModel, SendOtpModel, ValidateOtpModel
from app.services.communication_service import CommunicationService
from app.utils.standard_response import responseModel


communication_app = Blueprint('communication', __name__)


@communication_app.route('/send/otp', methods=['POST'])
def SendOtp(request=request, model=SendOtpModel, db: Session = DatabaseConnection.get_db_connection()):
    payload = model(**request.get_json()).dict()
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    print(trackingId)
    error, data = CommunicationService(trackingId, db, headers, payload).sendOtp()
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])


@communication_app.route('/resend/otp', methods=['POST'])
def ResendOtp(request=request, model=ResendOtpModel, db: Session = DatabaseConnection.get_db_connection()):
    payload = model(**request.get_json()).dict()
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    print(trackingId)
    error, data = CommunicationService(trackingId, db, headers, payload).resendOtp()
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])


@communication_app.route('/validate/otp', methods=['POST'])
def ValidateOtp(request=request, model=ValidateOtpModel, db: Session = DatabaseConnection.get_db_connection()):
    payload = model(**request.get_json()).dict()
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    print(trackingId)
    error, data = CommunicationService(trackingId, db, headers, payload).validateOtp()
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])
