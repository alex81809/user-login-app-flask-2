from flask import Flask, render_template, request, redirect, session 
import mysql.connector

app = Flask(__name__)

app.secret_key = "mysecretkey"

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    msg = ""

    if request.method == "POST" and "username" in request.form and "password" in request.form:

        username = request.form["username"]
        password = request.form["password"]

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_MYSQL_PASSWORD",
            database="flask_login"
        )

        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password)
        )

        account = mycursor.fetchone()

        mycursor.close()
        mydb.close()

        if account:

            print("Login successful!")

            id = account[0]
            name = account[1]

            session["username"] = name
            session["id"] = id

            msg = "Logged in successfully"

            return render_template(
                "index.html",
                msg=msg,
                name=name,
                id=id
            )

        else:

            msg = "Incorrect credientials. Kindly check"

            return render_template(
                "login.html",
                msg=msg
            )

        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    msg = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_MYSQL_PASSWORD",
            database="flask_login"
        )

        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT * FROM users WHERE username = %s OR email = %s",
            (username, email)
        )

        account = mycursor.fetchone()

        if account:

            msg = "Username or email already exists"

            mycursor.close()
            mydb.close()

            return render_template(
                "register.html",
                msg=msg
            )

        mycursor.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            (username,password,email)
        )

        mydb.commit()

        mycursor.close()
        mydb.close()

        msg = "Registration successful! Please login."

        return render_template(
            "login.html",
            msg=msg
        )

    return render_template("register.html")

@app.route("/index")
def index():

    if "username" in session:

        name = session["username"]

        return render_template(
            "index.html",
            name=name,
            msg="You are logged in"
        )

    return redirect("/login")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
