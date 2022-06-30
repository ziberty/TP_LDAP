import email
import imaplib
import smtplib
from email.header import decode_header
from email.mime.text import MIMEText

choix_server = int(input("Choisissez votre boîte mail : \n"
              "1. Outlook\n"
              "2. Epsi\n"
              "3. Gmail\n"))
usermail = input("Entrez votre adresse mail :\n")
password = input("Entrez votre mot de passe :\n")

if choix_server == 1 or choix_server == 2:
    server = 'outlook.office365.com'
else:
    server = 'imap.gmail.com'

mail = imaplib.IMAP4_SSL(server)
mail.login(usermail, password)

choix_action = int(input("Choisissez une action : \n"
                         "1. Lire les mails \n" 
                         "2. Envoyer un mail \n"))

mail.select('inbox')

if (choix_action == 1 and role == "read"):
    status, mails = mail.search(None, 'ALL')

    id_mails = []
    for id_mail in mails:
        id_mails += id_mail.split()

    id_mails = list(reversed(id_mails))
    id_mails = id_mails[:10]

    for i in id_mails:
        res, msg = mail.fetch(str(i.decode("utf-8")), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                print("Sujet :", subject)

elif (choix_action == 2 and role == "upload"):
    print("Envoie d'un mail :\n")
    to = input("Qui est le destinataire : \n")

    smtp_ssl_host = 'smtp.'+server
    smtp_ssl_port = 465

    corp = MIMEText(input("Quel est le corp de votre mail : \n"))
    res, msg = mail.fetch(str(id_mails[0].decode("utf-8")), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            first_subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(first_subject, bytes):
                corp['subject'] = first_subject.decode(encoding)

    corp['from'] = usermail
    corp['to'] = ', '.join(to)

    send_mail = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    send_mail.login(usermail, password)
    send_mail.sendmail(usermail, to, corp.as_string())
    send_mail.quit()


mail.close()
mail.logout()

