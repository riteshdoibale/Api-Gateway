from datetime import datetime
from sqlalchemy import select

from app.schemas.database_schema import Audit, User
from app.utils.db_helper_functions import to_dict
from app.configs.constant import ist_timezone


class AuditService:
    def __init__(self, trackingId, dbCon, headers, payload=None, queryParams=None):
        self.trackingId = trackingId
        self.dbCon = dbCon
        self.headers = headers
        self.payload = payload if payload else {}
        self.queryParams = queryParams if queryParams else {}
        
    def addAuditlog(self):
        errors = []
        userDetail = self.dbCon.execute(select(User).where(User.userName == self.headers.get('Username'), User.is_active == 1))
        userDetail = [to_dict(user) for user in userDetail.first()]
        userDetail = userDetail[0]
        try:
            auditData = {
                    "userId" : userDetail['userId'],
                    "previousData" : self.payload['previousData'],
                    "modifiedData" : self.payload['modifiedData'],
                    "modifiedDate" : self.payload.get('modifiedDate', datetime.now(ist_timezone)),
                    "trackingId" : self.trackingId
                }
            auditResponse = Audit(**auditData)
            self.dbCon.add(auditResponse)
            self.dbCon.commit()
            self.dbCon.refresh(auditResponse)
            return errors, {"message": "audit added successfully"}
        except Exception as e:
            print(f"{self.trackingId} Exception in add audit : ", e)
            errors.append({"errorMessege": "Failed to add audit : {e}"})
            return errors, {}