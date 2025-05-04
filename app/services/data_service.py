from sqlalchemy import delete, distinct, func, select, update

from app.schemas.database_schema import User, DailyWork
from app.utils.db_helper_functions import to_dict


class DataService:
    
    def __init__(self, trackingId, dbCon, headers, payload=None, queryParams=None):
        self.trackingId = trackingId
        self.dbCon = dbCon
        self.headers = headers
        self.payload = payload if payload else {} 
        self.queryParams = queryParams if queryParams else {} 
    
    def addDailyWork(self):
        errors = []
        userDetail = self.dbCon.execute(select(User).where(User.userName == self.headers.get('Username'), User.is_active == 1))
        userDetail = [to_dict(user) for user in userDetail.first()]
        userDetail = userDetail[0]
        for workDetail in self.payload['workDetails']:
            new_work = DailyWork(userId = userDetail['userId'],
                                    company = self.payload['companyName'],
                                    team = self.payload['teamName'],
                                    sprint = self.payload['sprintName'],
                                    workDate = self.payload['workDate'],
                                    ticketId = workDetail['ticketName'],
                                    workDescription = workDetail['workDescription'],
                                    achievements = self.payload['achievements'])
            self.dbCon.add(new_work)
            self.dbCon.commit()
            self.dbCon.refresh(new_work)
        return errors, {'messege':'data added successfully'}
    
    def getColumnData(self, columnName):
        errors = []
        if not hasattr(DailyWork, columnName):
            errors.append({'errorMessege':'Invalid column name'})
            return errors, {}
        column = getattr(DailyWork, columnName)
        userDetail = self.dbCon.execute(select(User).where(User.userName == self.headers.get('Username'), User.is_active == 1))
        userDetail = [to_dict(user) for user in userDetail.first()]
        userDetail = userDetail[0]
        response = self.dbCon.execute(select(distinct(column)).where(DailyWork.userId == userDetail['userId'])).scalars().all()
        return errors, response
    
    def getDailyWork(self):
        errors = []
        userDetail = self.dbCon.execute(select(User).where(User.userName == self.headers.get('Username'), User.is_active == 1))
        userDetail = [to_dict(user) for user in userDetail.first()]
        userDetail = userDetail[0]
        workDetailFilters = []
        if self.queryParams.get('startDate') and self.queryParams.get('endDate') and self.queryParams.get('startDate') > self.queryParams.get('endDate'):
            errors.append({'errorMessege':'startDate can not be greater than endDate'})
            return errors, {}
        if self.queryParams.get('startDate'):
            workDetailFilters.append(DailyWork.workDate > self.queryParams.get('startDate'))
        if self.queryParams.get('endDate'):
            workDetailFilters.append(DailyWork.workDate < self.queryParams.get('endDate'))
        if self.queryParams.get('company'):
            workDetailFilters.append(DailyWork.company == self.queryParams.get('company'))
        if self.queryParams.get('team'):
            workDetailFilters.append(DailyWork.team == self.queryParams.get('team'))
        if self.queryParams.get('sprint'):
            workDetailFilters.append(DailyWork.sprint == self.queryParams.get('sprint'))
        if self.queryParams.get('ticketId'):
            workDetailFilters.append(DailyWork.ticketId == self.queryParams.get('ticketId'))
        workDetail = self.dbCon.execute(select(*DailyWork.__table__.columns).where(*workDetailFilters, DailyWork.userId == userDetail['userId']) \
                        .limit(self.queryParams.get('pageSize')).offset((self.queryParams.get('pageNumber')-1)*self.queryParams.get('pageSize')))
        workDetail = [work._asdict() for work in workDetail.fetchall()]
        if not workDetail:
            errors.append({'errorMessege':'work detail not found'})
            return errors, {}
        count = select(func.count()).where(*workDetailFilters, DailyWork.userId == userDetail['userId'])
        count = self.dbCon.execute(count).scalar() or 0
        response = {
            "count" : count,
            "pageNumber" : self.queryParams.get('pageNumber'),
            "pageSize" : self.queryParams.get('pageSize'),
            "data" : workDetail
        }
        return errors, response
    
    def updateDailyWork(self, workId):
        errors = []
        userDetail = self.dbCon.execute(select(User).where(User.userName == self.headers.get('Username'), User.is_active == 1))
        userDetail = [to_dict(user) for user in userDetail.first()]
        userDetail = userDetail[0]
        workDetail = self.dbCon.execute(select(DailyWork).where(DailyWork.id == workId, DailyWork.userId == userDetail['userId']))
        workDetail = [to_dict(work) for work in workDetail.first()]
        workDetail = workDetail[0]
        if not workDetail:
            errors.append({'errorMessege':'work detail not found'})
            return errors, {}
        workDetail['company'] = self.payload.get('company')
        workDetail['team'] = self.payload.get('team')
        workDetail['sprint'] = self.payload.get('sprint')
        workDetail['workDate'] = self.payload.get('workDate')
        workDetail['ticketId'] = self.payload.get('ticketName')
        workDetail['workDescription'] = self.payload.get('workDescription')
        workDetail['achievements'] = self.payload.get('achievements')
        self.dbCon.execute(update(DailyWork).where(DailyWork.id == workId, DailyWork.userId == userDetail['userId']).values(**workDetail))
        self.dbCon.commit()
        return errors, {'messege':'data updated successfully'}
    
    def deleteWork(self, workId):
        errors = []
        userDetail = self.dbCon.execute(select(User).where(User.userName == self.headers.get('Username'), User.is_active == 1))
        userDetail = [to_dict(user) for user in userDetail.first()]
        userDetail = userDetail[0]
        workDetail = self.dbCon.execute(delete(DailyWork).where(DailyWork.id == workId, DailyWork.userId == userDetail['userId']))
        if workDetail.rowcount > 0:
            self.dbCon.commit()
            response = {"message": "Record deleted successfully"}
        else:
            response = {"message": "No matching record found"}
        return errors, response