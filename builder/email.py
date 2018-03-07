import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

__all__ = ['Email']


class Email:
    """Class to handle the SMTP server and send emails    
    """
    def __init__(self, server, port, username, password):
        self._server = server
        self._port = port
        self._username = username
        self._password = password

    @staticmethod
    def body_from_builder_output(log_to_send, stdout, stderr):
        return "\nCHANGELOG: \n{}\nSTDOUT: \n{}\nSTDERR: \n{}".format(log_to_send, stdout, stderr)

    def send(self, email_from, email_to, subject, body):
        msg = MIMEMultipart()

        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = email_to

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(self._server, self._port)
        server.ehlo()
        server.starttls()
        server.login(self._username, self._password)

        server.sendmail(email_from, email_to, msg.as_string())
        server.quit()
