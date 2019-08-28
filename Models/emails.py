# coding: utf-8
from Config import db
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % \
               (db.User, db.Passwd, db.Host, db.Port, db.DB, db.CharSet)
engine = create_engine(DBConnection)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()
class PubEmailTemplet(Base):

    __tablename__ = 'Pub_Email_Templet'

    ID = Column(Integer)
    Sku = Column(String(50), primary_key=True)
    EmailType = Column(String(50), primary_key=True)
    EmailTitle = Column(String(50))
    EmailBodyUrl = Column(String(200))
    BackUp = Column(String(200))

    def data_to_dict(self):
        data_dict = {
            'id': self.ID,
            'sku': self.Sku,
            'email_type': self.EmailType,
            'email_title': self.EmailTitle,
            'email_body_url': self.EmailBodyUrl
        }
        return data_dict



class PubEmailPending(Base):

    __tablename__ = 'Pub_Email_Pending'

    ID = Column(Integer)
    SendDate = Column(DateTime)
    SendHour = Column(Integer)
    AmazonOrderId = Column(String(20), primary_key=True)
    InboxMail = Column(String(200))
    InboxName = Column(String(100))
    TempletId = Column(Integer, primary_key=True)
    Carrier = Column(String(30))
    TrackingNum = Column(String(50))
    EstimatedArrivalDate = Column(DateTime)
    State = Column(Integer)
    ResendTimes = Column(Integer)

    def data_to_dict(self):
        data_dict = {
            'id': self.ID,
            'send_date': self.SendDate,
            'send_hour': self.SendHour,
            'order_id': self.AmazonOrderId,
            'inbox_mail': self.InboxMail,
            'inbox_name': self.InboxName,
            'templet_id': self.TempletId,
            'carrier': self.Carrier,
            'tracking_num': self.TrackingNum,
            'arrival_date': self.EstimatedArrivalDate,
            'state': self.State,
            'resend_times': self.ResendTimes
        }
        return data_dict


class NoSentEmailAddress(Base):

    __tablename__ = 'NoSentEmailAddress'

    CustomerEmailAddress = Column(String(100), primary_key=True)

    def __init__(self, email_address):
        self.CustomerEmailAddress=email_address

    def model_to_data(self):
        return self.CustomerEmailAddress.strip()


class PubEmailAlertTemplet(Base):

    __tablename__ = 'Pub_Email_Alert_Templet'

    ID = Column(Integer)
    TempletType = Column(String(50), primary_key=True)
    RoleId = Column(Integer, primary_key=True)
    SendHour = Column(Integer)
    EmailTitle = Column(String(50))
    EmailBodyUrl = Column(String(200))
    BackUp = Column(String(200))

    def data_to_dict(self):
        data_dict = {
            'id': self.ID,
            'templet_type': self.TempletType,
            'email_title': self.EmailTitle,
            'email_body_url': self.EmailBodyUrl
        }
        return data_dict


class PubEmailAlertPending(Base):

    __tablename__ = 'Pub_Email_Alert_Pending'

    ID = Column(Integer)
    SendDate = Column(DateTime, primary_key=True)
    SendHour = Column(Integer, primary_key=True)
    TempletId = Column(Integer, primary_key=True)
    InboxMail = Column(String(200), primary_key=True)
    State = Column(Integer)
    ResendTimes = Column(Integer)

    def data_to_dict(self):
        data_dict = {
            'id': self.ID,
            'send_date': self.SendDate,
            'send_hour': self.SendHour,
            'templet_id': self.TempletId,
            'inbox_mail': self.InboxMail,
            'state': self.State,
            'resend_times': self.ResendTimes
        }
        return data_dict