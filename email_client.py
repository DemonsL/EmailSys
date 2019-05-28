# coding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header


class EmailClient:

    def __init__(self, host, port=465):
        self.host = host
        self.port = port

    def make_msg(self, m_from, m_to, m_subject, m_body, m_type='plain'):
        msg = MIMEText(m_body, m_type, 'utf-8')
        msg['From'] = Header(m_from, 'utf-8')
        msg['To'] = Header(m_to, 'utf-8')
        msg['Subject'] = Header(m_subject, 'utf-8')
        return msg

    def send(self, m_user, m_pass, m_rece, msg):
        smtp_obj = smtplib.SMTP_SSL(host=self.host, port=self.port)
        try:
            smtp_obj.login(m_user, m_pass)
            smtp_obj.sendmail(m_user, m_rece, msg.as_string())
            print('Send mail success!')
        except smtplib.SMTPException as e:
            print('SendEmailError: ', e)
        finally:
            smtp_obj.quit()