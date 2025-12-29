import smtplib
from email.mime.text import MIMEText

# Email details
sender = "abrarnitsri0@gmail.com"
receiver = "tavaheed_2022bite008@nitsri.ac.in"
password = "znor ifqn psaw mfwd "

msg = MIMEText("Hello from Langchain \n Krish ka sune ga krish ka")
msg["Subject"] = "Test Mail"
msg["From"] = sender
msg["To"] = receiver

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender, password)
server.sendmail(sender, receiver, msg.as_string())
server.quit()

print("Email sent successfully")

