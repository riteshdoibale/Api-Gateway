from datetime import datetime, timedelta
from email.message import EmailMessage
import hashlib
import secrets
import smtplib
import uuid
from sqlalchemy import select, update

from app.models.enums import CommunicationstatusEnum
from app.configs.constant import ist_timezone
from app.configs.config import email_host, email_port, email_admin, email_pass
from app.schemas.database_schema import CommunicationTransaction, User
from app.utils.db_helper_functions import to_dict
from app.utils.hashing_service import HashingService


class CommunicationService:
    def __init__(self, trackingId, dbCon, headers, payload=None, queryParams=None):
        self.trackingId = trackingId
        self.dbCon = dbCon
        self.headers = headers
        self.payload = payload if payload else {}
        self.queryParams = queryParams if queryParams else {}
        
    def generateOtp(self, length: int = 6) -> str:
        rangeStart = 10**(length - 1)
        rangeEnd = 10**length - 1
        return str(secrets.randbelow(rangeEnd - rangeStart + 1) + rangeStart)
    
    def sendSms(self):
        try:
            import boto3 # type: ignore
            client = boto3.client('sns', region_name='us-east-1', aws_access_key_id='YOUR_KEY', aws_secret_access_key='YOUR_SECRET')
            response = client.publish(
                PhoneNumber=self.payload.get('mobileNumber'),
                Message = f"{self.payload.get('otp')} is your one time password, it will expire in 5 minutes. Thank You."
            )
            return True, ""
        except Exception as e:
            return False, f"exception : {e}"
    
    def sendEmail(self):
        try:
            msg = EmailMessage()
            msg['Subject'] = "Your OTP Code"
            msg['From'] = email_admin
            msg['To'] = self.payload.get('emailId')
            msg.set_content(f"{self.payload.get('otp')} is your one-time password. It will expire in 5 minutes. Thank you.")
            with smtplib.SMTP(email_host, email_port, timeout=30) as smtp:
                smtp.starttls()  # Secure the connection
                smtp.login(email_admin, email_pass)
                smtp.send_message(msg)
            return True, ""
        except Exception as e:
            return False, f"exception : {e}"
    
    def sendNotification(self):
        status = {}
        if self.payload.get('emailId'):
            emailResp, errorMessage = self.sendEmail()
            status['emailStatus'] = CommunicationstatusEnum.success if emailResp else CommunicationstatusEnum.failure
            status['emailErrorMessage'] = errorMessage
        if self.payload.get('mobileNumber'):
            smsResp, errorMessage = self.sendSms()
            status['smsStatus'] = CommunicationstatusEnum.success if smsResp else CommunicationstatusEnum.failure
            status['smsErrorMessage'] = errorMessage
        return status
    
    def createTransation(self, response, expiryTime):
        try:
            transactionData = {
                "userId" : response['userId'],
                "transactionId" : self.payload['transactionId'],
                "trackingId" : self.trackingId,
                "sendTime" : datetime.now(ist_timezone),
                "validateTime" : expiryTime,
                "status" : CommunicationstatusEnum.success if CommunicationstatusEnum.success in list(set(response.values())) else CommunicationstatusEnum.failure,
                "statusDescription" : f"{response.get('emailErrorMessage', '')} : {response.get('smsErrorMessage', '')}",
                "otpHash" : HashingService(self.payload['otp'], self.payload['transactionId'], hashlib.sha256).get_hashed_data()
            }
            transactionResponse = CommunicationTransaction(**transactionData)
            self.dbCon.add(transactionResponse)
            self.dbCon.commit()
            self.dbCon.refresh(transactionResponse)
        except Exception as e:
            print(f"{self.trackingId} Exception in createTransation : ", e)
            
    def fetchTransaction(self, transactionId, userId):
        transactionData = self.dbCon.execute(select(CommunicationTransaction).where(CommunicationTransaction.transactionId == transactionId, CommunicationTransaction.userId == userId))
        if transactionData:
            transactionData = [to_dict(transaction) for transaction in transactionData.first()]
            return transactionData[0]
        return False
        
    def updateTransation(self, response, expiryTime):
        try:
            transactionData = self.fetchTransaction(self.payload['transactionId'], response['userId'])
            if self.trackingId:
                transactionData['trackingId'] = self.trackingId
            transactionData['sendTime'] = datetime.now(ist_timezone)
            transactionData['validateTime'] = expiryTime
            transactionData['status'] = CommunicationstatusEnum.success if CommunicationstatusEnum.success in list(set(response.values())) else CommunicationstatusEnum.failure
            transactionData['statusDescription'] = f"{response.get('emailErrorMessage', '')} : {response.get('smsErrorMessage', '')}"
            transactionData['otpHash'] = HashingService(self.payload['otp'], self.payload['transactionId'], hashlib.sha256).get_hashed_data()
            self.dbCon.execute(update(CommunicationTransaction).where(CommunicationTransaction.transactionId == self.payload['transactionId']).values(**transactionData))
            self.dbCon.commit()
        except Exception as e:
            print("Exception in updateTransation : ", e)
    
    def sendOtp(self):
        errors = []
        userDetail = self.dbCon.execute(select(User).where(User.userName == self.headers.get('Username'), User.is_active == 1))
        userDetail = [to_dict(user) for user in userDetail.first()]
        userDetail = userDetail[0]
        self.payload['transactionId'] = self.payload.get('transactionId', str(uuid.uuid4()))
        self.payload['otp'] = self.generateOtp()
        self.payload['emailId'] = userDetail['userName']
        self.payload['mobileNumber'] = userDetail['mobileNumber']
        response = self.sendNotification()
        response['userId'] = userDetail['userId']
        expiryTime = datetime.now(ist_timezone) + timedelta(minutes=5)
        self.createTransation(response, expiryTime)
        if CommunicationstatusEnum.success not in list(set(response.values())):
            errors.append({"errorMessege": "Failed to send email and sms"})
            return errors, {}
        return errors, {
                        "message": "OTP sent successfully",
                        "transactionId": self.payload.get('transactionId'),
                        "expiryTime": expiryTime}
        
    def resendOtp(self):
        errors = []
        userDetail = self.dbCon.execute(select(User).where(User.userName == self.headers.get('Username'), User.is_active == 1))
        userDetail = [to_dict(user) for user in userDetail.first()]
        userDetail = userDetail[0]
        isTransactionExists = self.fetchTransaction(self.payload['transactionId'], userDetail['userId'])
        if not isTransactionExists:
            errors.append({"errorMessege": f"Transaction does not exists for transactionId {self.payload['transactionId']}"})
            return errors, {}
        self.payload['otp'] = self.generateOtp()
        self.payload['emailId'] = userDetail['userName']
        self.payload['mobileNumber'] = userDetail['mobileNumber']
        response = self.sendNotification()
        response['userId'] = userDetail['userId']
        expiryTime = datetime.now(ist_timezone) + timedelta(minutes=5)
        self.updateTransation(response, expiryTime)
        if CommunicationstatusEnum.success not in list(set(response.values())):
            errors.append({"errorMessege": "Failed to send email and sms"})
            return errors, {}
        return errors, {
                        "message": "OTP resent successfully",
                        "transactionId": self.payload.get('transactionId'),
                        "expiryTime": expiryTime}
    
    def validateOtp(self):
        errors = []
        userDetail = self.dbCon.execute(select(User).where(User.userName == self.headers.get('Username'), User.is_active == 1))
        userDetail = [to_dict(user) for user in userDetail.first()]
        userDetail = userDetail[0]
        isTransactionExists = self.fetchTransaction(self.payload['transactionId'], userDetail['userId'])
        if not isTransactionExists:
            errors.append({"errorMessege": f"Transaction does not exists for transactionId {self.payload['transactionId']}"})
            return errors, {}
        if not isTransactionExists == HashingService(self.payload['otp'], self.payload['transactionId'], hashlib.sha256).get_hashed_data():
            errors.append({"errorMessege": f"Invalid OTP, Enter correct OTP or resend"})
            return errors, {}
        if not datetime.now(ist_timezone) < isTransactionExists['validateTime']:
            errors.append({"errorMessege": f"OTP expired, kindly resend OTP"})
            return errors, {}
        return errors, {"message": "OTP validated successfully"}, 
        