#!/usr/bin/env python3

import flask
import os
import sendgrid

import orton_restitution

app = flask.Flask(__name__)
app.secret_key = 'dfjkladsfjkljj5k66vnkv3458jklfjds3e13231'


@app.route('/')
def index():
	"""Index page."""
	return flask.render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
	email = flask.request.form['email']
	if '@' not in email:
		student = ort_res.get_student(email)
		email += '@georgeschool.org'

		sg = sendgrid.SendGridClient(sendgrid_username, sendgrid_password, raise_errors=True)
		message = sendgrid.Mail()
		message.add_to('{} <{}>'.format(student.name, email))
		message.set_subject('Your Orton Restitution History')
		msg  = 'As requested, your Orton restitution history is here.\n\n'
		for rest in student.restitutions:
			msg += str(rest) + '\n'
		if not student.restitutions:
			msg += 'You have no restitutions.\n'
		msg += '\nIf you have any questions or concerns, please contact the Orton staff.'
		message.set_text(msg)
		message.set_from('Orton <orton@ortres.sidney.kochman.org>')

		_, msg = sg.send(message)
		flask.flash('Email sent to {}.'.format(email))
		return flask.redirect('/')

sendgrid_username = os.getenv('SENDGRID_USERNAME')
sendgrid_password = os.getenv('SENDGRID_PASSWORD')
google_drive_username = os.getenv("GOOGLE_DRIVE_USERNAME")
google_drive_password = os.getenv("GOOGLE_DRIVE_PASSWORD")
google_drive_spreadsheet_key = os.getenv("GOOGLE_DRIVE_SPREADSHEET_KEY")

ort_res = orton_restitution.OrtonRestitution(
	google_drive_username,
	google_drive_password,
	google_drive_spreadsheet_key
)

if __name__ == '__main__':
	app.debug = True
	app.run()
