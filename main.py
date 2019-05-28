# coding: utf-8
from Config import email_config
from email_client import EmailClient


def main():
    mail_host = email_config.mail_host_info.get('gmail_host')
    mail_user_info = email_config.mail_user_info.get('mws_user')
    mail_user = mail_user_info.split(',')[0]
    mail_pass = mail_user_info.split(',')[1]
    mail_rece = 'rain.chen@xcentz.com'

    emc = EmailClient(mail_host)
    msg = emc.make_msg(mail_user, mail_rece, '测试', '这是个测试！')
    emc.send(mail_user, mail_pass, mail_rece, msg)



if __name__ == '__main__':

    main()




