
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
	htmlMessage = "<p>Dear "+user['firstName']+",<br>You have requested to reset password. <a href="'http://localhost:4000/reset_password?code='+code+">Click here</b></a> to reset your password</p>"
	htmlMessage += "<p><b>Note:</b> This link will expire after 24h</p>"
	resetEmail = mailBuilder("KCSF - Reset password!", None, user['email'], htmlMessage)
	return resetEmail

