# coding: utf-8
import logging
import smtplib
import poplib
import datetime
from email.mime.text import MIMEText
from email.header import Header
from email.parser import Parser
from email.header import decode_header

log = logging.getLogger()

class EmailClient:

    def __init__(self, host, port=465):
        self.host = host
        self.port = port

    def make_msg(self, m_from, m_to, m_subject, m_body, m_type='plain'):
        m_to = ','.join(m_to) if isinstance(m_to, list) else m_to
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
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Send mail success!')
            log.info('Send mail success!')
        except smtplib.SMTPException as e:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'SendEmailError: ', e)
            log.info('SendEmailError: %s', e)
        finally:
            smtp_obj.quit()

    # ----------------receive email ---------------
    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def get_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            c_type = msg.get('Content-Type', '').lower()
            pos = c_type.find('charset=')
            if pos >= 0:
                charset = c_type[pos + 8:].strip()
        return charset

    def get_email_info(self, msg, header):
        value = msg.get(header, "")
        if value:
            value = self.decode_str(value)
        return value

    def get_email_body(self, msg):
        if msg.is_multipart():
            parts = msg.get_payload()
            bodys = []
            for part in parts:
                bodys.append(self.get_email_body(part))
            return bodys
        else:
            c_type = msg.get_content_type()
            c_value = msg.get_payload(decode=True)
            charset = self.get_charset(msg)
            if charset:
                c_value = c_value.decode(charset)
            return c_type, c_value

    def receive(self, m_user, m_pass):
        pop_obj = poplib.POP3_SSL(self.host)
        try:
            pop_obj.user(m_user)
            pop_obj.pass_(m_pass)
            m_count = pop_obj.stat()[0]
            msg_content = b"\r\n".join(pop_obj.retr(m_count)[1]).decode("utf-8")
            email_msg = Parser().parsestr(msg_content)
            email_infos = []
            for email_header in ["Date", "From", "To", "Subject"]:
                email_info = self.get_email_info(email_msg, email_header)
                email_infos.append((email_header, email_info))
            email_bodys = self.get_email_body(email_msg)
            return email_infos, email_bodys
        except Exception as e:
            log.error('ReceiveEmailError: %s', e)
        finally:
            pop_obj.quit()