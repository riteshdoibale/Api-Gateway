from pytz import timezone
from sqlalchemy import TEXT, Column, Date, ForeignKey, Index, Integer, Boolean, DateTime, Enum, func
from sqlalchemy.sql.sqltypes import VARCHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from app.configs.database import Base
from app.models.enums import CommunicationstatusEnum

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullName = Column(VARCHAR(50), nullable=False)
    userName = Column(VARCHAR(50), unique=True)
    userSecret = Column(VARCHAR(150), nullable=False)
    mobileNumber = Column(VARCHAR(10), nullable=False)
    premiumMember = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    createdDate = Column(DateTime, default=datetime.now(timezone("Asia/Kolkata")).isoformat)
    modifiedDate = Column(DateTime, nullable=True)
    
    dailywork = relationship("DailyWork", back_populates="user")
    communicationtransaction = relationship("communicationTransaction", back_populates="user")
    audit = relationship("Audit", back_populates="user")
    

class DailyWork(Base):
    __tablename__ = "dailywork"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    company = Column(VARCHAR(256), nullable=False)
    team = Column(VARCHAR(256), nullable=True)
    sprint = Column(VARCHAR(256), nullable=True)
    workDate = Column(Date, nullable=False, server_default=func.current_date())
    ticketId = Column(VARCHAR(256), nullable=True)
    workDescription = Column(VARCHAR(256), nullable=True)
    achievements = Column(VARCHAR(256), nullable=True)

    user = relationship("User", back_populates="dailywork")

    __table_args__ = (
        Index("idx_company", company),
        Index("idx_team", team),
        Index("idx_sprint", sprint),
        Index("idx_workDate", workDate),
        Index('userIddailywork', userId),
    )
    

class CommunicationTransaction(Base):
    __tablename__ = "communicationTransaction"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    transactionId = Column(VARCHAR(256), nullable=True)
    trackingId = Column(VARCHAR(256), nullable=False)
    sendTime = Column(DateTime, nullable=True, default=datetime.now(timezone("Asia/Kolkata")).isoformat)
    validateTime = Column(DateTime, nullable=True, default=datetime.now(timezone("Asia/Kolkata")).isoformat)
    status = Column(Enum(CommunicationstatusEnum))
    statusDescription = Column(TEXT, nullable=False)
    otpHash = Column(VARCHAR(256), nullable=True)
    
    user = relationship("User", back_populates="communicationtransaction")
    
    __table_args__ = (
        Index("userIdandtransactionId", userId, transactionId),
        Index('userIdCommunication', userId),
    )
    
    
class Audit(Base):
    __tablename__ = 'audits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('user.id', onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False)
    trackingId = Column(VARCHAR(256), nullable=False)
    previousData = Column(VARCHAR(5000), nullable=False)
    modifiedData = Column(VARCHAR(5000), nullable=False)
    modifiedDate = Column(DateTime, default=func.now(), nullable=True)

    user = relationship("User", back_populates="audit")
    
    __table_args__ = (
        Index('userIdaudits', userId),
    )