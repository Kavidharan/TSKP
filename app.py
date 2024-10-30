#moduls imports
import os
from flask import Flask,render_template,request,flash,redirect,g
import MySQLdb as mysql

#My sql connecton
con=mysql.Connection(host="localhost",user="root",password="Lskp1kavi*",db="tsko")
cor=mysql.cursors.DictCursor(con)


#apps
app=Flask(__name__)

app.secret_key="123"

#create tabel
cor.execute("create table if not exists users (sno integer auto_increment primary key, name text, age integer,gender text ,date_of_birth date, address text, branch text, aadhar text, email text, mobile text, username text, password text)")
cor.execute("create table if not exists admin (sno integer auto_increment primary key, name text, age integer,gender text ,date_of_birth date, address text, aadhar text, email text, mobile text, username text, password text)")
cor.execute("create table if not exists branch (sno integer auto_increment primary key, branch text, branch_address text)")
app.config["images"]="static/img"
app.config["data"]=""

@app.route("/",methods=["GET","POST"])
def home():
    if request.method =="POST":
        data=request.form["branch"]
        value=(data,)
        cor.execute("select * from branch where branch=%s",value)
        branch=cor.fetchall()
        return render_template("home.html",branch=branch)
    cor.execute("select * from branch")
    branch=cor.fetchall()
    return render_template("home.html",branch=branch)

"""@app.route("/index/<string:id>")
def index(id):
    cor.execute("select * from branch where=%s",(id))
    branch = cor.fetchall()
    return render_template("home.html", branch=branch)"""

@app.route("/login",methods=["GET","POST"])
def login():
    cor.execute("select * from branch")
    branches = cor.fetchall()
    if request.method == "POST":
        uname=request.form.get("uname")
        pas=request.form.get("pass")

        cor.execute("select * from users where username=%s",[uname])
        data=cor.fetchall()
        app.config["data"]=data
        cor.execute("select username from users")
        cn=cor.fetchall()
        image=dim(uname)
        for i in cn:
            if i["username"] in uname:
                cor.execute("select password from users where username= %s",[uname])
                userpas=cor.fetchall()
                if userpas[0]["password"] in pas:
                    return render_template("user.html",data=data,image=image,branch=branches)
                else:
                    flash("Username and password is not mach","danger")
                    return render_template("login.html")
            else:
                flash("This username is not register","danger")
                return render_template("login.html")
    return render_template("login.html")
def dim(uname):
    p1 = os.path.join(app.config["images"],uname+".JPG")
    p2 = os.path.join(app.config["images"],uname+".PNG")
    p3 = os.path.join(app.config["images"], uname+".JPEG")
    imc1=os.path.lexists(p1)
    imc2=os.path.lexists(p2)
    imc3=os.path.lexists(p3)
    image="static/img/default.jpg"
    if imc1 == True:
        image=p1
    elif imc2 == True:
        image=p2
    elif imc3 == True:
        image=p3
    return image

@app.route("/admin_login",methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        uname=request.form["uname"]
        pas=request.form["pass"]
        value=(uname,)
        cor.execute("select * from admin where username=%s",value)
        data=cor.fetchall()
        app.config["data"]=data
        cor.execute("select username from admin")
        cn=cor.fetchall()
        image=adim(uname)
        for i in cn:
            if i["username"] in uname:
                cor.execute("select password from admin where username= %s",[uname])
                userpas=cor.fetchall()
                if userpas[0]["password"] in pas:
                    return render_template("admin.html",data=data,image=image)
                else:
                    flash("Username and password is not mach","danger")
                    return render_template("admin_login.html")
            else:
                flash("This username is not register","danger")
                return render_template("admin_login.html")
    return render_template("admin_login.html")

@app.route("/admin_very",methods=["GET","POST"])
def very():
    if request.method =="POST":
        dcode="lskproot"
        code=request.form["code"]
        if code == dcode:
            return redirect("admin_create")
        else:
            flash("code is not mach","danger")
            return render_template("admin_very.html")

    return render_template("admin_very.html")


@app.route("/admin_create",methods=["GET","POST"])
def admin_create():
    if request.method == "POST":
        #get values
        name=request.form["name"]
        age=request.form["age"]
        gender=request.form["gender"]
        date_of_birth=request.form["date"]
        address=request.form["address"]
        aadhar=request.form["aadhar"]
        email=request.form["email"]
        mobil=request.form["mobil"]
        username=request.form["uname"]
        password=request.form["pass"]
        #contisons
        cor.execute("select * from admin")
        contison = cor.fetchall()

        for i in contison:
            if i["username"] == username:
                flash("This Username is already used","danger")
                return render_template("admin_create.html")
            elif i["password"] == password:
                flash("This Password is already used","danger")
                return render_template("admin_create.html")
        #stor databash
        try:
            values=(name,age,gender,date_of_birth,address,aadhar,email,mobil,username,password)
            cor.execute("insert into admin(name,age,gender,date_of_birth,address,aadhar,email,mobile,username,password) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",values)
            con.commit()
            flash("New Admin Account Create Successful","success")
            return render_template("home.html")
        except:
            flash("sorye reenter data","danger")
            return render_template("home.html")
    return render_template("admin_create.html")


@app.route("/create",methods=["GET","POST"])
def create():
    cor.execute("select * from branch")
    branches = cor.fetchall()
    if request.method == "POST":
        #get values
        name=request.form["name"]
        age=request.form["age"]
        gender=request.form["gender"]
        date_of_birth=request.form["date"]
        address=request.form["address"]
        branch=request.form["branch"]
        aadhar=request.form["aadhar"]
        email=request.form["email"]
        mobil=request.form["mobil"]
        username=request.form["uname"]
        password=request.form["pass"]
        #contisons
        cor.execute("select * from users")
        contison = cor.fetchall()

        for i in contison:
            if i["username"] == username:
                flash("This Username is already used","danger")
                return render_template("create.html",branch=branches)
            elif i["password"] == password:
                flash("This Password is already used","danger")
                return render_template("create.html",branch=branches)
        #stor databash
        try:
            values=(name,age,gender,date_of_birth,address,branch,aadhar,email,mobil,username,password)
            cor.execute("insert into users(name,age,gender,date_of_birth,address,branch,aadhar,email,mobile,username,password) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",values)
            con.commit()
            flash("New Account Create Successful","success")
            return render_template("home.html")
        except:
            flash("sorye reenter data","danger")
            return render_template("home.html")
    return render_template("create.html",branch=branches)


@app.route("/forget",methods=["GET","POST"])
def forget():
    if request.method =="POST":
        very_name=request.form["very_name"]
        cor.execute("select email from users where username=%s",[very_name])
        vmail=cor.fetchall()
        return "This is devepde"
    return render_template("forget.html")

@app.route("/cimage",methods=["GET","POST"])
def cimage():
    if request.method == "POST":
        uname=request.form["name"]
        image=request.files['image']
        if image.filename!="":
            ex=image.filename.split(".")[1]
            filepath=os.path.join(app.config["images"],uname+"."+ex)
            remove=os.path.lexists(filepath)

            if remove == True:
                os.remove(filepath)

            image.save(filepath)
            g.data=app.config["data"]
            g.img=dim(uname)
            return render_template("user.html", data=g.data, image=g.img)
        else:
            flash("Choose image","danger")
            return render_template("user.html",data=g.data,image=g.img)
    return render_template("user.html",data=g.data,image=g.img)


@app.route("/acimage",methods=["GET","POST"])
def acimage():
    if request.method == "POST":
        uname=request.form["name"]
        image=request.files['image']
        if image.filename!="":
            ex=image.filename.split(".")[1]
            filepath=os.path.join(app.config["images"],uname+"_admin."+ex)
            remove=os.path.lexists(filepath)

            if remove == True:
                os.remove(filepath)

            image.save(filepath)
            g.data=app.config["data"]
            g.img=adim(uname)
            return render_template("admin.html", data=g.data, image=g.img)
        else:
            flash("Choose image", "danger")
            return render_template("admin.html", data=g.data, image=g.img)
    return render_template("admin.html",data=g.data,image=g.img)

def adim(uname):
    p1 = os.path.join(app.config["images"],uname+"_admin.JPG")
    p2 = os.path.join(app.config["images"],uname+"_admin.PNG")
    p3 = os.path.join(app.config["images"], uname+"_admin.JPEG")
    imc1=os.path.lexists(p1)
    imc2=os.path.lexists(p2)
    imc3=os.path.lexists(p3)
    image="static/img/default.jpg"
    if imc1 == True:
        image=p1
    elif imc2 == True:
        image=p2
    elif imc3 == True:
        image=p3
    return image

@app.route("/edit",methods=["GET","POST"])
def edit():
    if request.method == "POST":
        name=request.form["name"]
        age=request.form["age"]
        gender=request.form["gender"]
        date_fo_birth=request.form["date_of_birth"]
        branch=request.form["branch"]
        aadhar=request.form["aadhar"]
        mobile=request.form["mobile"]
        email=request.form["email"]
        address=request.form["address"]

        uname=request.form["uname"]

        query="update users set name = %s where username=%s"
        cor.execute(query,[name,uname])
        query = "update users set age = %s where username=%s"
        cor.execute(query,[age,uname])
        query = "update users set gender = %s where username=%s"
        cor.execute(query, [gender, uname])
        query = "update users set date_of_birth = %s where username=%s"
        cor.execute(query, [date_fo_birth,uname])
        query = "update users set branch = %s where username=%s"
        cor.execute(query, [branch, uname])
        query = "update users set aadhar = %s where username=%s"
        cor.execute(query, [aadhar,uname])
        query = "update users set mobile = %s where username=%s"
        cor.execute(query, [mobile,uname])
        query = "update users set email = %s where username=%s"
        cor.execute(query, [email,uname])
        query = "update users set address = %s where username=%s"
        cor.execute(query, [address, uname])
        con.commit()
        flash("Data update successful","success")
        return render_template("home.html")
    return render_template("user.html")


@app.route("/admin_edit",methods=["GET","POST"])
def admin_edit():
    if request.method == "POST":
        name=request.form["name"]
        age=request.form["age"]
        gender=request.form["gender"]
        date_fo_birth=request.form["date_of_birth"]
        aadhar=request.form["aadhar"]
        mobile=request.form["mobile"]
        email=request.form["email"]
        address=request.form["address"]

        uname=request.form["uname"]

        query="update admin set name = %s where username=%s"
        cor.execute(query,[name,uname])
        query = "update admin set age = %s where username=%s"
        cor.execute(query,[age,uname])
        query = "update admin set gender = %s where username=%s"
        cor.execute(query, [gender, uname])
        query = "update admin set date_of_birth = %s where username=%s"
        cor.execute(query, [date_fo_birth,uname])
        query = "update admin set aadhar = %s where username=%s"
        cor.execute(query, [aadhar,uname])
        query = "update admin set mobile = %s where username=%s"
        cor.execute(query, [mobile,uname])
        query = "update admin set email = %s where username=%s"
        cor.execute(query, [email,uname])
        query = "update admin set address = %s where username=%s"
        cor.execute(query, [address, uname])
        con.commit()
        flash("Data update successful","success")
        return render_template("home.html")
    return render_template("admin.html")



@app.route("/add_branch",methods=["GET","POST"])
def add_branch():
    cor.execute("select * from branch")
    branches=cor.fetchall()
    if request.method == "POST":
        branch=request.form["branch"]
        branch_address=request.form["branch_address"]
        cor.execute("select branch from  branch")
        contison=cor.fetchall()
        values=(branch,branch_address)

        for datas in contison:
            if datas["branch"] == branch:
                flash("This branch is already register","danger")
                return render_template("add_branch.html",data=branches)
        try:
            cor.execute("insert into branch (branch,branch_address) value(%s,%s)",values)
            con.commit()
            flash("Branch register successful","success")
            cor.execute("select * from branch")
            branches = cor.fetchall()
            return render_template("add_branch.html",data=branches)
        except:
            return render_template("add_branch.html",data=branches)

    return render_template("add_branch.html",data=branches)

@app.route("/branch_delete/<string:id>",methods=["GET","POST"])
def branch_delete(id):
    cor.execute("delete from branch where sno=%s",(id))
    con.commit()
    cor.execute("select * from branch")
    branches = cor.fetchall()
    flash("The branch is delete","danger")
    return render_template("add_branch.html",data=branches)



@app.route("/user_delete/<string:id>",methods=["GET","POST"])
def user_delete(id):
    cor.execute("delete from users where sno=%s",(id))
    con.commit()
    cor.execute("select * from users")
    users=cor.fetchall()
    flash("data is removed","danger")
    return render_template("view_user.html",users=users)


@app.route("/user_check/<string:id>",methods=["GET","POST"])
def user_check(id):
    cor.execute("select * from users where sno=%s",(id))
    users = cor.fetchall()
    cor.execute("select * from branch")
    branches = cor.fetchall()
    uname=users[0]['username']
    image=dim(uname)
    return render_template("user_check.html",data=users,image=image,branch=branches)


@app.route("/view_user",methods=["GET","POST"])
def view_user():
    cor.execute("select * from users")
    users = cor.fetchall()
    return render_template("view_user.html",users=users)



if __name__ == '__main__':
    app.run(debug=True)
