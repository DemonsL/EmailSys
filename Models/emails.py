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
    Asin = Column(String(20), primary_key=True)
    EmailType = Column(String(50), primary_key=True)
    EmailTitle = Column(String(50))
    EmailBodyUrl = Column(String(200))
    BackUp = Column(String(200))

    def data_to_dict(self):
        data_dict = {
            'id': self.ID,
            'asin': self.Asin,
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
    EmailTitle = Column(String(200))
    TempletId = Column(Integer, primary_key=True)
    State = Column(Integer)
    ResendTimes = Column(Integer)

    def data_to_dict(self):
        data_dict = {
            'send_date': self.SendDate,
            'send_hour': self.SendHour,
            'order_id': self.AmazonOrderId,
            'inbox_mail': self.InboxMail,
            'inbox_name': self.InboxName,
            'email_title': self.EmailTitle,
            'templet_id': self.TempletId,
            'state': self.State,
            'resend_times': self.ResendTimes
        }
        return data_dict
