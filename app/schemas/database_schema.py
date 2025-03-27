from pytz import timezone
from sqlalchemy import Column, Date, ForeignKey, Index, Integer, Boolean, DateTime, func
from sqlalchemy.sql.sqltypes import VARCHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from app.configs.database import Base

class User(Base):
    __tablename__ = 'user'
    
    userId = Column(Integer, primary_key=True, autoincrement=True)
    fullName = Column(VARCHAR(50), nullable=False)
    userName = Column(VARCHAR(50), unique=True)
    userSecret = Column(VARCHAR(150), nullable=False)
    mobileNumber = Column(VARCHAR(1000), nullable=False)
    premiumMember = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    createdDate = Column(DateTime, default=datetime.now(timezone("Asia/Kolkata")).isoformat)
    modifiedDate = Column(DateTime, nullable=True)
    
    dailywork = relationship("DailyWork", back_populates="user")
    

class DailyWork(Base):
    __tablename__ = "dailywork"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("user.userId", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
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
    )