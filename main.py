# coding: utf-8
import pytz
import logging
import datetime
import random
from Config import email_config
from Models import emails
from email_client import EmailClient
from sqlalchemy import and_

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_name = '/home/develop/logs/email_logs/{}.log'.format(datetime.date.today())
log = logging.getLogger()
log.setLevel(logging.INFO)


fh = logging.FileHandler(file_name, mode='a+')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

class SendMail:

    def get_nosend_list(self):
        session = emails.DBSession()
        resp = session.query(emails.NoSentEmailAddress).all()
        session.close()
        nosends = [r.model_to_data() for r in resp]
        return nosends

    def del_nosend_email_from_pend(self, nosend_email):
        session = emails.DBSession()
        nosend_pend = session.query(emails.PubEmailPending).filter(and_(emails.PubEmailPending.InboxMail == nosend_email,
                                                                        emails.PubEmailPending.State == 0)).all()
        if nosend_pend:
            log.info('No send email: %s' % nosend_email)
            for nosend_p in nosend_pend:
                session.delete(nosend_p)
            session.commit()


    def get_template_by_id(self, temp_id):
        session = emails.DBSession()
        resp = session.query(emails.PubEmailTemplet).filter_by(ID=temp_id).one()
        session.close()
        return resp

    def get_email_pending(self, date, time, stat, times):
        session = emails.DBSession()
        resp = session.query(emails.PubEmailPending).filter(and_(and_(and_(
                                                     emails.PubEmailPending.SendDate == date),
                                                     emails.PubEmailPending.SendHour == time),
                                                     emails.PubEmailPending.State != stat,
                                                     emails.PubEmailPending.ResendTimes < times)).all()
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
        mail_rece = params.get('buyer_email')
        mail_type = params.get('email_type')

        # user_type = 'mws_user_ship'
        # if mail_type == 'AmzReceipt':
        #     user_type = 'mws_user_receipt'
        # elif mail_type == 'AmzInvite':
        #     user_type = 'mws_user_invite'
        # log.info('UserType: %s', user_type)
        mail_user_info = random.choice(email_config.mail_user_info.get('mws_users'))
        mail_from = mail_user_info.split(',')[0]
        mail_user = email_config.mail_user_info.get('aws_user').split(',')[0]
        mail_pass = email_config.mail_user_info.get('aws_user').split(',')[1]
        mail_host = email_config.mail_host_info.get('aws_host')


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
        msg = emc.make_msg(mail_from, mail_rece, subject, m_body, 'html')
        emc.send(mail_user, mail_pass, mail_from, mail_rece, msg)

    def start_send(self, pend):
        pen_id = pend.get('id')
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
        log.info('EmailType: %s', email_type)

        attemps, sucess = 0, False
        while attemps < 3 and not sucess:
            try:
                send_obj.send_mail(email_title, email_body_url, params)
                send_obj.put_email_pending(pen_id, resend_times)
                sucess = True
            except Exception as e:
                attemps += 1
                log.info('SendEmailError: %s', e)



if __name__ == '__main__':

    date_us = datetime.datetime.now().astimezone(pytz.timezone('US/Pacific')).date()
    time_us = datetime.datetime.now().astimezone(pytz.timezone('US/Pacific')).time().hour
    state = 1
    resend_times = 3

    send_obj = SendMail()
    pending = send_obj.get_email_pending(date_us, time_us, state, resend_times)
    if pending:
        log.info('Delete no send email from pending...')
        nosend_list = send_obj.get_nosend_list()
        for nosend in nosend_list:
            send_obj.del_nosend_email_from_pend(nosend)
        log.info('Delete no send email from pending...end!')
        for pend in pending:
            pend = pend.data_to_dict()
            log.info('US Date: %s', str(date_us) + ' ' + str(time_us))
            send_obj.start_send(pend)




