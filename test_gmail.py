# import smtplib
# from email.message import EmailMessage

# class gmail_sender:
#     def __init__(self, sender_email, receiver_email, sender_password, cc_email = "", bcc_email=""):
#         self.s_email = sender_email
#         self.r_email = receiver_email
#         self.pw = sender_password
#         self.server_name = "smtp.gmail.com"
#         self.server_port = 587
        
#         self.msg = EmailMessage()
#         self.msg["From"] = self.s_email
#         self.msg["To"] = self.r_email
#         if cc_email != "":
#             self.cc_email = cc_email
#             self.msg["Cc"] = self.cc_email
#         if bcc_email != "":
#             self.bcc_email = bcc_email
#             self.msg["Bcc"] = self.bcc_email
#         self.smtp = smtplib.SMTP(self.server_name, self.server_port)
        
#     def msg_get(self, msg_title, msg_body):
#         self.msg["Subject"] = msg_title
#         self.msg.set_content(msg_body)
        
#     def smtp_connect_send(self):
#         self.smtp.ehlo()
#         self.smtp.starttls()
#         self.smtp.login(self.s_email, self.pw)
#         self.smtp.send_message(self.msg)
        
#     def smtp_disconect(self):
#         self.smtp.close()
        
# # test_email = gmail_sender("HancomTasking@gmail.com", "inchoon.yeo@gmail.com", "Tasking123!" )
# test_email = gmail_sender("paul.yeo94@gmail.com", "inchoon.yeo@gmail.com", "kissme!004" )
# test_email.msg_get("test_title","test_msg")    
# test_email.smtp_connect_send()
# test_email.smtp_disconect()

# import smtplib, ssl

# class Mail:

#     def __init__(self):
#         self.port = 465
#         self.smtp_server_domain_name = "smtp.gmail.com"
#         self.sender_mail = "HancomTasking@gmail.com"
#         self.password = "Tasking123!"

#     def send(self, emails, subject, content):
#         ssl_context = ssl.create_default_context()
#         service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
#         service.login(self.sender_mail, self.password)
        
#         for email in emails:
#             result = service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}")

#         service.quit()


# if __name__ == '__main__':
#     # mails = input("Enter emails: ").split()
#     # subject = input("Enter subject: ")
#     # content = input("Enter content: ")
#     mails = "inchoon.yeo@gmail.com"
#     subject = "test title"
#     content = "test content"
#     mail = Mail()
#     mail.send(mails, subject, content)

import smtplib, ssl
from email.message import EmailMessage

my_email = "HancomTasking@gmail.com"
my_password = "Tasking123!"
other_email = "inchoon.yeo@gmail.com"

email = EmailMessage()
email['from'] = my_email
email['to'] = other_email
email['subject'] = 'Test'
email.set_content('Just testing')
smtp = smtplib.SMTP(host='smtp.gmail.com',port=587)
smtp.ehlo()
smtp.starttls()
smtp.login(my_email,my_password)