from datetime import datetime
import hashlib
from sqlalchemy import select, update

from app.schemas.database_schema import User
from app.utils.db_helper_functions import to_dict
from app.utils.hashing_service import HashingService



class AuthService:
    def __init__(self, dbCon, payload):
        self.dbCon = dbCon
        self.payload = payload
        
    def createUser(self):
        errors = []
        userDetail = self.dbCon.execute(select(User).where(User.userName == self.payload.get('userName'), User.is_active == 1))
        userDetail = userDetail.first()
        if userDetail:
            errors.append({'errorMessege':'user already exist'})
            return errors, {}
        hashed_password = HashingService(self.payload.get('password'), self.payload.get('userName'), hashlib.sha256).get_hashed_data()
        new_user = User(fullName=self.payload.get('fullName'),
                        userName=self.payload.get('userName'), 
                        userSecret=hashed_password,
                        mobileNumber=self.payload.get('mobileNumber'),
                        premiumMember=0,
                        is_active=1,
                        createdDate=datetime.utcnow().isoformat(),
                        modifiedDate=datetime.utcnow().isoformat())
        self.dbCon.add(new_user)
        self.dbCon.commit()
        self.dbCon.refresh(new_user)
        return errors, {'messege':'user created successfully'}
    
    def verifyUser(self):
        errors = []
        hashed_password = HashingService(self.payload.get('password'), self.payload.get('userName'), hashlib.sha256).get_hashed_data()
        userDetail = self.dbCon.execute(select(User).where(User.userName==self.payload.get('userName'), User.userSecret==hashed_password, User.is_active==1))
        userDetail = userDetail.first()
        if not userDetail:
            errors.append({'errorMessege':'user does not exist'})
            return errors, {}
        return errors, {'messege': f"{userDetail}"}
    
    def checkUserExists(self):
        errors = []
        if 'userName' not in self.payload or not self.payload.get('userName'):
            errors.append({'errorMessege':'queryParam.userName is null or not found'})
            return errors, {}
        userDetail = self.dbCon.execute(select(User).where(User.userName == self.payload.get('userName')))
        userDetail = userDetail.first()
        if not userDetail:
            errors.append({'errorMessege':'user does not exist'})
            return errors, {}
        userDetail = [to_dict(user) for user in userDetail]
        userDetail[0]['modifiedDate'] = datetime.utcnow().isoformat()
        userDetail[0]['is_active'] = 0
        del userDetail[0]['userSecret']
        self.dbCon.execute(update(User).where(User.userName == self.payload.get('userName')).values(**userDetail[0]))
        self.dbCon.commit()
        return errors, {'messege': f"{userDetail[0]}"}
    
    def storeNewPass(self):
        errors = []
        userDetail = self.dbCon.execute(select(User).where(User.userName == self.payload.get('userName'), User.is_active==0))
        userDetail = userDetail.first()
        if not userDetail:
            errors.append({'errorMessege':'user does not exist or does not request for password change'})
            return errors, {}
        userDetail = [to_dict(user) for user in userDetail]
        hashed_password = HashingService(self.payload.get('password'), self.payload.get('userName'), hashlib.sha256).get_hashed_data()
        userDetail[0]['userSecret'] = hashed_password
        userDetail[0]['modifiedDate'] = datetime.utcnow().isoformat()
        userDetail[0]['is_active'] = 1
        self.dbCon.execute(update(User).where(User.userName == self.payload.get('userName')).values(**userDetail[0]))
        self.dbCon.commit()
        return errors, {'messege': "password change successfully"}
        