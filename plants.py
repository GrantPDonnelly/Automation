import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pickle

water_schedule = {
    'Snake Plants': 21,
    'Spider Plants': 11,
    'Aloes': 21,
    'Rubber Trees': 11,
    'Money Trees': 11,
    'Corn Plants': 9,
    'Bamboo': 3,
    'Creeping Charlies': 7,
    'Pothos Pictas': 11,
    'Anthuriums': 7,
}

instructions = {
    'Snake Plants': 'Soil should be completely dry before watering.',
    'Spider Plants': 'The top inch of the soil should be dry before watering.',
    'Aloes': 'The top third of the soil should be dry before watering.',
    'Rubber Trees': 'Soil should be kept moist but not wet.',
    'Money Trees': 'Water until water runs through drainage holes. Do not allow water to remain pooled on the surface.',
    'Corn Plants': 'Soil should just be moist after watering',
    'Bamboo': 'Water thouroughly but allow to drain completely.',
    'Creeping Charlies': 'Keep soil moist but not wet. Drain any excess water.',
    'Pothos Pictas': 'Top two inches of soil shoild be totally dry before watering. Drain excess water.',
    'Anthuriums': 'Top two inches of soil shoild be totally dry before watering. Drain excess water.',
}

f = open('data', 'rb')
days_since_watered = pickle.load(f)
needs_watered = []
for i in days_since_watered:
    days_since_watered[i] += 1
    if days_since_watered[i] == water_schedule[i]:
        needs_watered.append(i)
        days_since_watered[i] = 0
f = open('data', 'wb')
pickle.dump(days_since_watered, f)

if len(needs_watered) > 0:
    port = 465
    email = 'python.updater500@gmail.com'
    password = 
    receivers = ['python.updater500@gmail.com']

    context = ssl.create_default_context()
    message = MIMEMultipart("alternative")
    message["Subject"] = "Plant Watering Reminder"
    message["From"] = email

    text = "Water these plants today:\n"

    for i in needs_watered:
        text += i+': '+instructions[i]+'\n'

    message.attach(MIMEText(text, "plain"))
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, receivers, message.as_string())

'''
# init:
days_since_watered = {
    'Snake Plants': 0,
    'Spider Plants': 0,
    'Aloes': 0,
    'Rubber Trees': 0,
    'Money Trees': 0,
    'Corn Plants': 0,
    'Bamboo': 0,
    'Creeping Charlies': 0,
    'Pothos Pictas': 0,
    'Anthuriums': 0,
}
f = open('data', 'wb')
pickle.dump(days_since_watered, f)
'''
