import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv
from creds import u, p


def my_send_email(Group):
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        message = MIMEMultipart("alternative")
        message["Subject"] = "Kaisenmasters Ops Update"
        message["From"] = u
        recipients = Group.emails
        message["To"] = ", ".join(recipients)
        html = """\
        <html>
          <body>
            <p><br>
            </p>
          </body>
        </html>
        """
        part2 = MIMEText(html, "html")
        message.attach(part2)
        # attachement

        filename = f'{Group.id}/hourly_summary_{Group.id}.xlsx'

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(filename, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        f'attachment; filename="{filename}"')
        message.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(u, p)
            server.sendmail(u, recipients, message.as_string())

    except Exception as e:
        print(f'Something went wrong... | {e}')


if __name__ == '__main__':

    class Group:
        def __init__(self, name, id, pw, emails):
            self.name = name
            self.id = id
            self.pw = pw
            self.emails = emails

    groups = []
    with open("groups.csv") as csvfile:  # not tracked
        rows = csv.reader(csvfile)
        for row in rows:
            groups.append(Group(row[0], row[1], row[2], [x for x in row[3:]]))
    my_send_email(groups[0])
