from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL,MySQLdb
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, IntegerField, FloatField, DateField, SelectField, SubmitField
from wtforms.validators import Required, InputRequired, DataRequired, Optional, Length, Email, URL,NumberRange, EqualTo, Regexp

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'web'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config["SECRET_KEY"] = "dasdqwf hard to guess string asdqwe"
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

class loginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")

class registerForm(FlaskForm):
    username = StringField("Username")
    email = StringField("Email")
    password = PasswordField("Password")
    truename = StringField("truename")
    mobile = IntegerField("mobile")
    address = StringField("address")
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")

class adminloginForm(FlaskForm):
    ausername = StringField("aname")
    apassword = PasswordField("apassword")
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")

class WTSForm(FlaskForm):
    productname = StringField("Product Name")
    price = IntegerField("Price")
    discription = StringField("Discription")
    nvmofgood = IntegerField("nvmofgood")
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")

class changeForm(FlaskForm):
    username = StringField("Username")
    email = StringField("Email")
    password = PasswordField("Password")
    truename = StringField("truename")
    mobile = IntegerField("mobile")
    address = StringField("address")
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")

class adminchangeForm(FlaskForm):
    username = StringField("Username")
    email = StringField("Email")
    password = PasswordField("Password")
    truename = StringField("truename")
    mobile = IntegerField("mobile")
    address = StringField("address")
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")

class productForm(FlaskForm):
    prodcutname = StringField("productname")
    price = IntegerField("price")
    discription = StringField("Discription")
    nvmfogood = IntegerField("nvmofgood")
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")   

@app.route("/")
def home():
    return render_template ("home.html")

@app.route("/login" , methods=["GET", "POST"])
def login():
    form = loginForm()
    if request.method == 'POST':
        inputusername = request.form['username']
        inputpassword = request.form['password']
        print(inputusername,inputpassword)
        
        curr = mysql.connection.cursor()
        curr.execute("SELECT * FROM users WHERE username=%s", (inputusername,))
        for e in curr.fetchall():
            username1 = (e['username'])

        try: 
            username1 == inputusername
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username=%s", (inputusername,))
            for e in cur.fetchall():
                pw = e['password']
                idd = e['userid']
            if inputpassword == pw :
                flash("login success","success")
                session['idd'] = idd
                session['username'] = username1
                session['logged_in'] = True
                return render_template('home.html')
            else:
                flash("wrong password","error")
                return render_template('login.html', form=form)
        except UnboundLocalError: 
            flash("wrong username","error")
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

@app.route("/adminlogin" , methods=["GET", "POST"])
def adminlogin():
    form = adminloginForm()
    if request.method == 'POST':
        inputausername = request.form['ausername']
        inputapassword = request.form['apassword']
        print(inputausername,inputapassword)
        
        curr = mysql.connection.cursor()
        curr.execute("SELECT * FROM admin WHERE aname=%s", (inputausername,))
        for e in curr.fetchall():
            ausername1 = (e['aname'])

        try: 
            ausername1 == inputausername
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM admin WHERE aname=%s", (inputausername,))
            for e in cur.fetchall():
                pw = e['apassword']
            if inputapassword == pw :
                flash("admin login success","success")
                session['aname'] = ausername1
                session['logged_in'] = True
                return redirect('admin')
            else:
                flash("admin wrong password","error")
                return render_template('adminlogin.html', form=form)
        except UnboundLocalError: 
            flash("wrong admin name","error")
            return render_template('adminlogin.html', form=form)
    else:
        return render_template('adminlogin.html', form=form)

@app.route("/logout")
def logout():
    session.clear()
    return render_template ("home.html")

@app.route("/register" , methods=["GET", "POST"])
def register():
    form = registerForm()
    if request.method == 'POST':
        inputusername = request.form['username']
        inputpassword = request.form['password']
        inputemail = request.form['email']  
        inputtruename = request.form['truename']
        inputmobile = request.form['mobile']
        inputaddress = request.form['address']

        print(inputusername,inputemail,inputtruename,inputpassword,inputmobile,inputaddress)
        print("INSERT INTO users (username,password,email,truename,mobile,address) VALUES ('{n}','{p}','{e},'{t}','{m}','{a}')".format(n=inputusername,p=inputpassword,e=inputemail,t=inputtruename,m=inputmobile,a=inputaddress))
        curr = mysql.connection.cursor()
        curr.execute("INSERT INTO users (username,password,email,truename,mobile,address) VALUES ('{n}','{p}','{e}','{t}','{m}','{a}')".format(n=inputusername,p=inputpassword,e=inputemail,t=inputtruename,m=inputmobile,a=inputaddress))
        mysql.connection.commit()
        return render_template('home.html')
    return render_template('register.html', form=form)
        
        

@app.route("/WTS" , methods=["GET", "POST"])
def WTS():
    form = WTSForm()
    if request.method == 'POST':
        inputproductname = request.form['productname']
        inputprice = request.form['price']
        inputdiscription = request.form['discription']  
        inputnvmofgood = request.form['nvmofgood']

        print(inputproductname,inputprice,inputdiscription,inputnvmofgood)
        print("INSERT INTO wts (productname,price,discription,nvmofgood) VALUES ('{pn}','{p}','{d}','{nog}')".format(pn=inputproductname,p=inputprice,d=inputdiscription,nog=inputnvmofgood))
        curr = mysql.connection.cursor()
        curr.execute("INSERT INTO wts (`Product name`,price,discription,nvmofgood) VALUES ('{pn}','{p}','{d}','{nog}')".format(pn=inputproductname,p=inputprice,d=inputdiscription,nog=inputnvmofgood))
        mysql.connection.commit()
        return render_template('home.html')
    return render_template('WTS.html', form=form)

@app.route("/WTB")
def WTB():
    form = productForm() 
    curr = mysql.connection.cursor()
    curr.execute("SELECT * FROM wtb")
    wtbdata = curr.fetchall()
    print(wtbdata)
    
    return render_template ("WTB.html", data=wtbdata, form=form)


@app.route("/aboutus")
def aboutus():
    return render_template ("aboutus.html")

@app.route("/personal")
def personal():
    form = changeForm()
    curr = mysql.connection.cursor()
    curr.execute("SELECT * FROM users WHERE username='%s'"%session['username'])
    userdata = curr.fetchone()
    print(userdata)
    
    return render_template ("personal.html",data=userdata, form=form)

@app.route("/change", methods=["GET", "POST"])
def change():
    
    if request.method == 'POST':
        inputpassword = request.form['password']
        inputemail = request.form['email']  
        inputtruename = request.form['truename']
        inputmobile = request.form['mobile']
        inputaddress = request.form['address']
        userid = session['idd']


        curr = mysql.connection.cursor()

        curr.execute("Update users SET password = '%s' where userid = '%s'"%(inputpassword,userid))
        
        curr.execute("Update users SET email = '%s' where userid = '%s'"%(inputemail,userid))
        
        curr.execute("Update users SET truename = '%s' where userid = '%s'"%(inputtruename,userid))
        
        curr.execute("Update users SET mobile = '%s' where userid = '%s'"%(inputmobile,userid))
        
        curr.execute("Update users SET address = '%s' where userid = '%s'"%(inputaddress,userid))
        

        mysql.connection.commit()
    return redirect(url_for('personal'))



@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    if request.method == 'POST':
        productname = request.form["productname"]
        price = request.form["price"]
        userid = int(session['idd'])
        
        curr = mysql.connection.cursor()

        print("INSERT INTO purchase (userid,Product_Name,Price) VALUES ('{uid}','{pn}','{p}')".format(uid = userid,pn = productname,p = price,))
        curr.execute("INSERT INTO purchase (userid,Product_Name,Price) VALUES ('{uid}','{pn}','{p}')".format(uid = userid,pn = productname,p = price))

        mysql.connection.commit()
    return redirect(url_for('WTB'))    

@app.route("/admin")
def admin():
    form = productForm() 
    curr = mysql.connection.cursor()
    curr.execute("SELECT * FROM users")
    usersdata = curr.fetchall()
    curr.execute("SELECT * FROM purchase")
    purchasedata = curr.fetchall()
    
    
    return render_template ("admin.html", data=usersdata,data1= purchasedata, form=form)







if __name__ == "__main__":
    app.run(debug=True)