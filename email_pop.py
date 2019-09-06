# coding: utf-8
import poplib
from email.parser import Parser
from email.header import decode_header

poplib._MAXLINE = 20480

class EmailPop:

    def __init__(self, host):
        self.host = host

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
        c_value = msg.get_payload(decode=True)
        charset = self.get_charset(msg)
        if charset:
            c_value = c_value.decode(charset)
        return c_value

    def receive(self, m_user, m_pass, num=1):
        pop_obj = poplib.POP3_SSL(self.host)
        try:
            pop_obj.user(m_user)
            pop_obj.pass_(m_pass)
            m_count = pop_obj.stat()[0]

            msg_content = b"\r\n".join(pop_obj.retr(num)[1]).decode("utf-8")
            email_msg = Parser().parsestr(msg_content)
            return m_count, email_msg
        except Exception as e:
            print('ReceiveEmailError: ', e)
        finally:
            pop_obj.quit()



# if __name__ == '__main__':
#
#     m_host = 'pop.exmail.qq.com'
#     m_user = 'luomurong@yulong.com'
#     m_pass = 'YL50315yl'
#     exit_date = datetime.today().date() - timedelta(days=2)
#
#     ep = EmailPop(m_host)
#     rece_count, rece_msg = ep.receive(m_user, m_pass)
#
#     while rece_count > 0:
#         rece = ep.receive(m_user, m_pass, rece_count)
#         # 邮件超过两天时退出
#         email_date = ep.get_email_info(rece[1], 'Date')
#         email_date = datetime.strptime(email_date.split(',')[1].split('+')[0].strip(), '%d %b %Y %H:%M:%S') \
#                              .strftime('%Y-%m-%d %H:%M:%S').split(' ')[0]
#         if email_date < str(exit_date):
#             exit()
#         # 保存通知邮件地址
#         email_subject = ep.get_email_info(rece[1], 'Subject')
#         if email_subject == 'AWS Notification Message':
#             email_bodys = json.loads(ep.get_email_body(rece[1]).split('--')[0].strip())
#             nosend_email = email_bodys.get('complaint').get('complainedRecipients')[0].get('emailAddress')
#
#         rece_count -= 1