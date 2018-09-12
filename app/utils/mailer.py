
import datetime
from flask_mail import Message
from datetime import timedelta

# Build mail object
def mailBuilder(subject, sender, sendTo, message):
    msg = Message(subject,
              sender=sender,
              recipients=[sendTo])
    msg.html = message
    return msg

# Send email to reset user password
def sendResetPassword(user, request, code):
	htmlMessage = '<p>P'u'\xeb''rsh'u'\xeb''ndetje '+user['firstName']+',<br>Ju keni k'u'\xeb''rkuar ta ndryshoni fjal'u'\xeb''kalimin. <a href="http://localhost:4000/kcsf-data-visualizer/reset_password?code='+code+'">Klikoni k'u'\xeb''tu</b></a> p'u'\xeb''r ta ndryshuar fjal'u'\xeb''kalimin</p>'
	htmlMessage += '<p><b>Njoftim:</b> Ky link do t'u'\xeb'' skadoj pas 24 or'u'\xeb''ve</p>'
	resetEmail = mailBuilder("KCSF - Reset password!", None, user['email'], htmlMessage)
	return resetEmail

