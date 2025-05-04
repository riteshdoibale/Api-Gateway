import uuid
from flask import Blueprint, request
from sqlalchemy.orm import Session
from app.configs.database import DatabaseConnection

from app.models.data_model import GetDailyWorkModel, NewDailyWorkModel, UpdateDailyWorkModel
from app.services.data_service import DataService
from app.utils.standard_response import responseModel

data_app = Blueprint('data', __name__)


@data_app.route('/daily/task', methods=['POST'])
def AddDailyWork(request=request, model=NewDailyWorkModel, db: Session = DatabaseConnection.get_db_connection()):
    payload = model(**request.get_json()).dict()
    queryParams = (request.args).to_dict()
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    error, data = DataService(trackingId, db, headers, payload, queryParams).addDailyWork()
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])


@data_app.route('/daily/task/<string:columnName>', methods=['GET'])
def GetColumnData(columnName, request=request,  db: Session = DatabaseConnection.get_db_connection()):
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    error, data = DataService(trackingId, db, headers).getColumnData(columnName)
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])


@data_app.route('/daily/task', methods=['GET'])
def GetDailyWork(request=request, model=GetDailyWorkModel, db: Session = DatabaseConnection.get_db_connection()):
    queryParams = model(**request.args.to_dict()).dict()
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    print(trackingId)
    error, data = DataService(trackingId, db, headers, {}, queryParams).getDailyWork()
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])


@data_app.route('/daily/task/<int:workId>', methods=['PUT'])
def UpdateDailyWork(workId, request=request, model=UpdateDailyWorkModel, db: Session = DatabaseConnection.get_db_connection()):
    payload = model(**request.get_json()).dict()
    queryParams = (request.args).to_dict()
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    # pathParams = request.view_args
    error, data = DataService(trackingId, db, headers, payload, queryParams).updateDailyWork(workId)
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])


@data_app.route('/daily/task/<int:workId>', methods=['DELETE'])
def DeleteWork(workId, request=request, db: Session = DatabaseConnection.get_db_connection()):
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    # pathParams = request.view_args
    error, data = DataService(trackingId, db, headers).deleteWork(workId)
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])
