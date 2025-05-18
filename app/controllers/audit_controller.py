import uuid
from flask import Blueprint, request
from sqlalchemy.orm import Session

from app.configs.database import DatabaseConnection
from app.models.audit_model import AddAuditModel
from app.services.audit_service import AuditService
from app.utils.standard_response import responseModel


audit_app = Blueprint('audit', __name__)


@audit_app.route('', methods=['POST'])
def addAudit(request=request, model=AddAuditModel, db: Session = DatabaseConnection.get_db_connection()):
    payload = model(**request.get_json()).dict()
    headers = dict(request.headers)
    trackingId = headers.get('Trackingid', str(uuid.uuid4()))
    print(trackingId)
    error, data = AuditService(trackingId, db, headers, payload).addAuditlog()
    if error:
        print(error)
        return responseModel(trackingId, data={}, errors=error)
    return responseModel(trackingId, data=data, errors=[])