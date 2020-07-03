

from flask import Flask, render_template, url_for, request,session,redirect,make_response,flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
import textextractionfromimage
import scrap
import facebookScrap
import TwitterDataExtraction
import faceRecognize
import evaluation
import Automate_email
import functools 
import operator
import requests
from requests import Timeout

app=Flask(__name__)
app.secret_key= '  '

app.config["IMAGE_UPLOADS"] = "C:/Users/Abhi/Desktop/Project20/images"
app.config["IMAGE_UPLOADS1"] = "C:/Users/Abhi/Desktop/Project20/imageswithbanner"
app.config["IMAGE_UPLOADS2"] = "C:/Users/Abhi/Desktop/Project20/bannerimages"
app.config["IMAGE_UPLOADS3"] = "C:/Users/Abhi/Desktop/Project20/cert_images"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPG","PNG"]

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'apple@123'
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html')

@app.route('/', methods=['GET', 'POST'])

def index():
	 if request.method == "POST":
	 	details = request.form
	 	name = details['name']
	 	phoneno=details['phoneno']
	 	email=details['email']
	 	message=details['message']
	 	cur=mysql.connection.cursor()
	 	cur.execute("INSERT INTO contact(name,phoneno,email,message) VALUES (%s, %s,%s,%s)", (name,phoneno,email,message))
	 	mysql.connection.commit()
	 	cur.close()

	 return render_template('index.html')

# @app.after_request
# def after_request(response):
#     response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
#     return response

@app.route('/s_signup', methods=['GET', 'POST'])

def s_signup():
	 if request.method == "POST":
	 	details = request.form
	 	studentId = details['ss_id']
	 	firstName = details['s_fname']
	 	lastName = details['s_lname']
	 	email = details['s_email']
	 	password = details['s_password']
	 	image = request.files["image"]
	 	phonenumber= details['s_phone']
	 	filename1 = studentId + '.' + 'jpg'
	 	filename2 = studentId + '.' + 'png'
	 	cur = mysql.connection.cursor()
	 	
	 	
	 
	 	if allowed_image(image.filename) and filename1 == image.filename or filename2 == image.filename :
	 		filename = secure_filename(image.filename)
	 		cur.execute("INSERT INTO student(f_name, l_name,s_id,email_id,phone_number,photo,password) VALUES (%s, %s,%s,%s,%s,%s,%s)", (firstName, lastName,studentId,email,phonenumber,image,password))
	 		image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
	 	else:
	 		return render_template('s_signup.html',a='input is not correct');

	 	mysql.connection.commit()
	 	cur.close()
	 	return  redirect(url_for('s_login',a='You are successfully registered!!'));
	 return render_template('s_signup.html')

@app.route('/s_login', methods=['GET', 'POST'])

def s_login():
	 if request.method == "POST":
	 	details = request.form
	 	studentId = details['s_id']
	 	password1 = 0
	 	session['userid']=studentId;
	 	password = details['s_password']
	 	cur = mysql.connection.cursor()
	 	sql_select_query = """select password,f_name from student where s_id = %s"""
	 	cur.execute(sql_select_query, (studentId,))
	 	# cur.execute("SELECT password FROM `student` WHERE s_id = %s", (studentId))
	 	records = cur.fetchall()
	 	for row in records:
	 		password1 = row[0]
	 		session['name'] = row[1]


	 	if password == password1:
	 		return redirect(url_for('studenthome'))

	 	else:
	 		return render_template('s_login.html',error='id or password did not matched')
	 		

	 	
	 	mysql.connection.commit()
	 	cur.close()
	 return render_template('s_login.html')
	 
	 
@app.route('/studenthome')
def studenthome():
	name2=session['name']	
	return render_template('studenthome.html',user_name=name2)

@app.route('/manual_page')
def manual_page():
	cur = mysql.connection.cursor()
	a=1
	try:
		cur.execute("INSERT INTO manualverification(student_id, status) VALUES (%s,%s)", (session['userid'],a))
		mysql.connection.commit()
		cur.close()
		return render_template('manual_page.html',user_name=session['name'],ab='your record has been submitted')
	except Exception as e:
		return render_template('403.html')



@app.route('/admin', methods=['GET', 'POST'])

def a_login():
	 if request.method == "POST":
	 	details = request.form
	 	adminId = details['a_id']
	 	password = details['a_password']
	 	cur = mysql.connection.cursor()
	 	sql_select_query = """select password from admin where a_id = %s"""
	 	cur.execute(sql_select_query, (adminId,))
	 	# cur.execute("SELECT password FROM `student` WHERE s_id = %s", (studentId))
	 	records = cur.fetchall()
	 	for row in records:
	 		password1 = row[0]
	 	
	 	if password == password1:
	 		return redirect(url_for('adminHome'))

	 	else:
	 		return 'password error'
	 		
	 	mysql.connection.commit()
	 	cur.close()
	 return render_template('admin.html')

@app.route('/adminHome', methods=['GET', 'POST'] )
def adminHome():
	if request.method == "POST":
		
		return redirect(url_for('s_manual'))
	return render_template('adminHome.html')

@app.route('/f_signup', methods=['GET', 'POST'])

def f_signupp():
	 if request.method == "POST":
	 	details = request.form
	 	facultyId = details['f_id']
	 	firstName = details['f_fname']
	 	lastName = details['f_lname']
	 	email = details['f_email']
	 	password = details['f_password']
	 	phonenumber= details['f_phone']
	 	branch = details['branch']
	 	cur = mysql.connection.cursor()
	 	cur.execute("INSERT INTO faculty(f_name, l_name,f_id,email_id,phone_number,password,branch) VALUES (%s, %s,%s,%s,%s,%s,%s)", (firstName, lastName,facultyId,email,phonenumber,password,branch))
	 	mysql.connection.commit()
	 	cur.close()
	 	return render_template('adminHome.html')
	 
	 return render_template('f_signup.html')
	 	


@app.route('/f_login', methods=['GET', 'POST'])

def f_loginn():
	 if request.method == "POST":
	 	details = request.form
	 	facultyId = details['ff_id']
	 	password1=0
	 	password = details['f_password']
	 	cur = mysql.connection.cursor()
	 	sql_select_query = """select password,f_name,f_id from faculty where f_id = %s"""
	 	cur.execute(sql_select_query, (facultyId,))
	 	records = cur.fetchall()
	 	for row in records:
	 		password1 = row[0]
	 		fac_Id = row[2]
	 		session['fname']=row[1]
	 	
	 	if password == password1 and facultyId == fac_Id:
	 		return  redirect(url_for('facultyHome'))

	 	else:
	 		return render_template('f_login.html',error1='id or password did not matched')
	 		
	 	mysql.connection.commit()
	 	cur.close()
	 return render_template('f_login.html')

@app.route('/facultyHome',methods=['GET','POST'])

def facultyHome():
	if request.method == "POST":
		details = request.form
		session['st_id']=details['search']
		cur = mysql.connection.cursor()
		sql_select_query = """select s_id,event_name,event_date,organizer from submission where s_id = %s"""
		cur.execute(sql_select_query, (session['st_id'],))
		data = cur.fetchall()
		return render_template('specific_view.html',record=data)
	return render_template('facultyHome.html',faculty_name=session['fname'])

@app.route('/specific_view')
def specific_view():
	return render_template('specific_view.html')

@app.route('/portfolio')
def portfolioo():
	return render_template('portfolio.html')

@app.route('/view_submission')

def view_submission():
	cur = mysql.connection.cursor()
	cur.execute("select s_id,event_name,event_date,organizer from submission")
	data = cur.fetchall()
	return render_template('view_submission.html',records=data)
	
#submission python code

@app.route('/submission', methods=['GET', 'POST'])

def s_submission():
	 if request.method == "POST":
	 	details = request.form
	 	eventName = details['evnt_name']
	 	session['eventName']= eventName
	 	image1 = request.files["image1"]
	 	image2 = request.files["image2"]
	 	image3 = request.files["image3"]
	 	sid = session['userid']
	 	
	 	
	 	filename1 = sid + '.' + 'jpg'
	 	filename2 = sid + '.' + 'png'
	 	eventDate = details['event_date']
	 	aboutEvent = details['about_event']
	 	weburl = details['web_url']
	 	fbPageId = details['fb_page_id']
	 	organizername = details['organizer_name']
	 	session['organizername']=organizername


	 	cur = mysql.connection.cursor()
	 	
	 	
	 
	 	if allowed_image(image1.filename) and filename1 == image1.filename or filename2 == image1.filename :
	 		if allowed_image(image2.filename) and filename1 == image2.filename or filename2 == image2.filename :
	 			if allowed_image(image3.filename) and filename1 == image3.filename or filename2 == image3.filename :
	 				cur.execute("INSERT INTO submission(event_name, img_banner, banner_img, certificate_image, event_date, s_id, aboutevent,websiteurl,organizer,fb_page_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (eventName, image1, image2,image3,eventDate,sid,aboutEvent,weburl,organizername,fbPageId))
	 				image1.save(os.path.join(app.config["IMAGE_UPLOADS1"], image1.filename))
	 				image2.save(os.path.join(app.config["IMAGE_UPLOADS2"], image2.filename))
	 				image3.save(os.path.join(app.config["IMAGE_UPLOADS3"], image3.filename))
	 			else:
	 				flash('Your image filename did not matched with your id')
	 				return render_template('submission.html',sub_name=session['name'])
	 		else:
	 			flash('Your image filename did not matched with your id')
	 			return render_template('submission.html',sub_name=session['name'])
	 	else:
	 		flash('Your image filename did not matched with your id')
	 		return render_template('submission.html',sub_name=session['name'])
	 	mysql.connection.commit()
	 	cur.close()
	 	s="C:/Users/Abhi/Desktop/Project20/cert_images/"
	 	t=".jpg" 
	 	b="C:/Users/Abhi/Desktop/Project20/bannerimages/"
	 	a=".jpg"
	 	m="C:/Users/Abhi/Desktop/Project20/images/"
	 	ban_img="C:/Users/Abhi/Desktop/Project20/imageswithbanner/"
	 	session['j']=0 
	 	session['g']=0 
	 	session['r']=0 
	 	session['fb']=0 
	 	session['tw']=0
	 	session['fr']=0
	 	faceRecognize.encodeFace(m+sid+t,sid)
	 	session['fr'] = faceRecognize.recognizeFace(ban_img+sid+t,sid)
	 	try:

	 		if session['fr'] == 1:
	 			textextractionfromimage.textFromImage(s+sid+t)
	 			textextractionfromimage.textFromImage1(b+sid+a)
	 			session['j']=textextractionfromimage.searchingKeyWord(aboutEvent)
	 			session['g']=textextractionfromimage.matchTwoFiles()
	 			session['r']=scrap.webScraping(weburl,aboutEvent)
	 			session['fb'] = facebookScrap.facebookScraper(eventName,fbPageId)
	 			session['tw'] = TwitterDataExtraction.TwitterDataExtraction(aboutEvent)
	 			return redirect(url_for('studenthome'))
	 		else:
	 			return render_template('submission.html',c='Image doesnot match')
	 	except Exception as e:
	 		return render_template('500.html')
	 return render_template('submission.html',sub_name=session['name'])	 	

# validation results
@app.route('/validation_results')
def results():

	text_result=session['j']
	bnrcert_result=session['g']
	web_result=session['r']
	sm_result = (session['fb'] + session['tw'])/2
	session['k']=sm_result
	fr_result = session['fr']
	session['total_result'] = ((text_result+bnrcert_result+web_result+sm_result)/4)*100

	return render_template('validation_results.html',j=text_result,b=bnrcert_result,r=web_result,f=sm_result,g=fr_result,t=session['total_result'])

# evaluation
@app.route('/evaluation', methods=['GET', 'POST'])

def eval():
	name2=session['name']
	if session['total_result']>=65:
		if request.method == "POST":
			details = request.form
			eventType = details['type_of_event']
			
			durationEvent = details['duration_of_event']
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO evaluation(type_of_event,name_of_event,duration_of_event,organizer,student_id) VALUES (%s,%s,%s,%s,%s)", (eventType,session['eventName'],durationEvent,session['organizername'],session['userid']))
			grade = evaluation.collegelist(session['organizername'],int(durationEvent),eventType)

			return render_template('eval_results.html',j=session['j'],b=session['g'],r=session['r'],f=session['k'],g=session['fr'],t=session['total_result'],fg=grade,user_name=name2)
	else:
		return render_template('validation_results.html',ab='Your percentage is less than 65%. Please go for resubmission or manual validation',j=session['j'],b=session['g'],r=session['r'],f=session['k'],g=session['fr'],t=session['total_result'])
	return render_template('evaluation.html',user_name=name2)

@app.route('/eval_results')
def e_results():
	
	return render_template('eval_results.html')

@app.route('/s_manual', methods=['GET','POST'])
def s_manual():
	if request.method == "POST":
		button1=1
		cur1 = mysql.connection.cursor()
		sql1="""DELETE FROM manualverification WHERE status = %s"""
		cur1.execute(sql1,(button1,))
		mysql.connection.commit()
		cur1.close()
	cur = mysql.connection.cursor()
	cur.execute("select * from manualverification")
	datas = cur.fetchall()
	return render_template('s_manual.html',manual=datas)

@app.route('/faculty_allocation', methods=['GET','POST'])

def faculty_allocation():

	if request.method == "POST":
		details = request.form
		fact_name=details['f_name']
		st_id=details['s_id']
		date=details['date']
		time=details['time']
		cur1=mysql.connection.cursor()
		sql1="""select email_id from faculty where f_name = %s"""
		cur1.execute(sql1, (fact_name,))
		facultymail=cur1.fetchone()
		# facultymail1 = ''.join(facultymail)
		facultymail1 = functools.reduce(operator.add, (facultymail))
		cur2=mysql.connection.cursor()
		sql2="""select email_id from student where s_id = %s"""
		cur2.execute(sql2, (st_id,))
		studentmail=cur2.fetchone()
		# studentmail1=''.join(studentmail)
		studentmail1 = functools.reduce(operator.add, (studentmail))
		Automate_email.sendEmail( facultymail1,time,date,st_id)
		Automate_email.sendEmail1( studentmail1,time,date,fact_name)
		cur1 = mysql.connection.cursor()
		sql1="""UPDATE faculty set available_status = 0 WHERE f_name = %s"""
		cur1.execute(sql1,(fact_name,))
		mysql.connection.commit()
		cur1.close()
	cur = mysql.connection.cursor()
	b=1
	sql_select_query = """select f_name,branch,available_status from faculty where available_status = %s"""
	cur.execute(sql_select_query, (b,))
	datas = cur.fetchall()
	cur.close()
	 	
	
	return render_template('faculty_allocation.html',records=datas)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)

