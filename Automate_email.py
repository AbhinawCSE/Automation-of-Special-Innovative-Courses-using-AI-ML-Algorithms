import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def sendEmail(Teachermail,time,date,student_id):
	email = 'p.working2020@gmail.com'
	password = 'projectwork@2020'
	subject = 'Manual Validation'
	message = 'This mail is reagrding manual validation option opted by student having student id: ' + student_id+'.Your allocated time for meeting is TIME:'+time+' DATE:'+date
	msg = MIMEMultipart()
	msg['From'] = email
	msg['To'] = Teachermail
	msg['Subject'] = subject
	msg .attach(MIMEText(message,'plain'))
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()	
	server.login(email,password)
	text = msg.as_string()
	server.sendmail(email,Teachermail,text)
	server.quit()

def sendEmail1(Studentmail,time,date,faculty_name):
	email = 'p.working2020@gmail.com'
	password = 'projectwork@2020'
	subject = 'Manual Validation'
	message = 'Your allocated time and date for meeting with professor '+ faculty_name+' is TIME:'+ time+' DATE:'+ date+'. kindly come to the meeting on time.'
	msg = MIMEMultipart()
	msg['From'] = email
	msg['To'] = Studentmail
	msg['Subject'] = subject
	msg .attach(MIMEText(message,'plain'))
	
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(email,password)
	text = msg.as_string()
	server.sendmail(email,Studentmail,text)
	server.quit()
if __name__ == '__main__':
	sendEmail1('abhinawsingh007@gmail.com','1:30','12 June 2020','Hari')
