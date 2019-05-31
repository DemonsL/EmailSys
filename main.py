# coding: utf-8
import pytz
import datetime
from Config import email_config
from Models import emails
from email_client import EmailClient


class SendMail:

    def get_template_by_id(self, temp_id):
        session = emails.DBSession()
        resp = session.query(emails.PubEmailTemplet).filter_by(ID=temp_id).one()
        session.close()
        return resp

    def get_email_pending(self, state):
        session = emails.DBSession()
        resp = session.query(emails.PubEmailPending).filter_by(State=state).all()
        session.close()
        return resp

    def put_email_pending(self, pen_id, resend_times):
        session = emails.DBSession()
        session.query(emails.PubEmailPending).filter_by(ID=pen_id).update({
            'State': 1,
            'ResendTimes': resend_times + 1
        })
        session.commit()


    def send_mail(self, subject, url, params):
        mail_host = email_config.mail_host_info.get('gmail_host')
        mail_user_info = email_config.mail_user_info.get('mws_user')
        mail_user = mail_user_info.split(',')[0]
        mail_pass = mail_user_info.split(',')[1]
        mail_rece = params.get('buyer_email')
        mail_type = params.get('email_type')

        with open('Template' + url, 'r') as f:
            if mail_type == 'AmzShip':
                m_body = f.read().format(
                    buyer_name = params.get('buyer_name'),
                    carrier_name = params.get('carrier_name'),
                    tracking_number= params.get('tracking_number'),
                    arrival_date = params.get('arrival_date')
                )
            else:
                m_body = f.read().format(
                    buyer_name=params.get('buyer_name')
                )

        emc = EmailClient(mail_host)
        msg = emc.make_msg(mail_user, mail_rece, subject, m_body, 'html')
        emc.send(mail_user, mail_pass, mail_rece, msg)

    def start_send(self, pend):
        pen_id = pend.get('id')
        send_date = pend.get('send_date')
        send_hour = pend.get('send_hour')
        inbox_mail = pend.get('inbox_mail')
        inbox_name = pend.get('inbox_name')
        templet_id = pend.get('templet_id')
        carrier = pend.get('carrier')
        tracking_num = pend.get('tracking_num')
        arrival_date = pend.get('arrival_date')
        resend_times = pend.get('resend_times')

        temp = send_obj.get_template_by_id(templet_id)
        temp = temp.data_to_dict()
        email_title = temp.get('email_title')
        email_type = temp.get('email_type')
        email_body_url = temp.get('email_body_url')

        params = {
            'buyer_name': inbox_name,
            'buyer_email': inbox_mail,
            'email_type': email_type,
            'carrier_name': carrier,
            'tracking_number': tracking_num,
            'arrival_date': datetime.datetime.strftime(arrival_date, '%Y-%m-%d')
        }

        start_date = datetime.datetime.strftime(send_date, '%Y-%m-%d {}'.format(send_hour))
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H')
        now_us = datetime.datetime.now().astimezone(pytz.timezone('US/Pacific'))
        now_us = datetime.datetime.strptime(now_us.strftime('%Y-%m-%d %H'), '%Y-%m-%d %H')
        if now_us == start_date:
            send_obj.send_mail(email_title, email_body_url, params)
            send_obj.put_email_pending(pen_id, resend_times)



if __name__ == '__main__':

    send_obj = SendMail()
    pending = send_obj.get_email_pending(0)

    for pend in pending:
        pend = pend.data_to_dict()
        send_obj.start_send(pend)




