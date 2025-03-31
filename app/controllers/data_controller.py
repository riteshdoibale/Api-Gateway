from flask import Blueprint, request
from sqlalchemy.orm import Session
from app.configs.database import DatabaseConnection

from app.models.data_model import GetDailyWorkModel, NewDailyWorkModel, UpdateDailyWorkModel
from app.services.data_service import DataService

data_app = Blueprint('data', __name__)


@data_app.route('/daily/task', methods=['POST'])
def AddDailyWork(request=request, model=NewDailyWorkModel, db: Session = DatabaseConnection.get_db_connection()):
    payload = model(**request.get_json()).dict()
    queryParams = (request.args).to_dict()
    headers = dict(request.headers)
    error, data = DataService(db, headers, payload, queryParams).addDailyWork()
    if error:
        print(error)
        return error
    return data


@data_app.route('/daily/task/<string:columnName>', methods=['GET'])
def GetColumnData(columnName, request=request,  db: Session = DatabaseConnection.get_db_connection()):
    headers = dict(request.headers)
    error, data = DataService(db, headers).getColumnData(columnName)
    if error:
        print(error)
        return error
    return data


@data_app.route('/daily/task', methods=['GET'])
def GetDailyWork(request=request, model=GetDailyWorkModel, db: Session = DatabaseConnection.get_db_connection()):
    queryParams = model(**request.args.to_dict()).dict()
    headers = dict(request.headers)
    error, data = DataService(db, headers, {}, queryParams).getDailyWork()
    if error:
        print(error)
        return error
    return data


@data_app.route('/daily/task/<int:workId>', methods=['PUT'])
def UpdateDailyWork(workId, request=request, model=UpdateDailyWorkModel, db: Session = DatabaseConnection.get_db_connection()):
    payload = model(**request.get_json()).dict()
    queryParams = (request.args).to_dict()
    headers = dict(request.headers)
    # pathParams = request.view_args
    error, data = DataService(db, headers, payload, queryParams).updateDailyWork(workId)
    if error:
        print(error)
        return error
    return data


@data_app.route('/daily/task/<int:workId>', methods=['DELETE'])
def DeleteWork(workId, request=request, db: Session = DatabaseConnection.get_db_connection()):
    headers = dict(request.headers)
    # pathParams = request.view_args
    error, data = DataService(db, headers).deleteWork(workId)
    if error:
        print(error)
        return error
    return data


