from flask import Flask, render_template, session, redirect, url_for, request
import pymysql.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
app = Flask(__name__)


#connection
#     with connection.cursor() as cursor:
#             sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
#             cursor.execute(sql, ('arif', 'asd@gmial.com','patatoes'))
    # connection.commit()
app.secret_key = 'THIS_IS_BAD'

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Root',
                             database='aisec',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



@app.route("/")
def index():
    username = session.get("username", None)
    error = session.get("is_error" , False)
    is_used = session.get("is_used", False)
    user_info = None
    account_info = None
    #fetch user information
    if username != None : 
        connection 
        with connection.cursor() as cursor :
            cursor.execute(" SELECT * FROM users WHERE username= (%s)",(username,))
            user_info= cursor.fetchone() 
        print(user_info)
        with connection.cursor() as cursor :
            cursor.execute(" SELECT balance FROM account_info WHERE user_id=(SELECT user_id FROM users WHERE username =(%s))",(username,))
            account_info = cursor.fetchone() 

    is_wrong = session.get("is_wrong", False)
    return render_template("index.html", user_info=user_info, account_info = account_info ,is_error=error, is_used=is_used, is_wrong=is_wrong)


@app.route("/signup", methods=['POST'])
def signUp():
    session["is_used"] = False
    try:
        connection 
        with connection.cursor() as cursor :

            username = request.form.get("username").strip().casefold()
            mail = request.form.get("email").strip()
            password = request.form.get("password").strip()
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, mail, hashed_password))
            session["is_used"] = False
            cursor.execute("INSERT INTO account_info (user_id,balance) VALUES ((SELECT user_id FROM users WHERE username=(%s)),100)",(username,))
        
        connection.commit()
        print("kayıt olundu")
        return redirect(url_for('index'))

    except:
        print("kayıt olunamadı")

        session["is_used"] = True
        return redirect(url_for('index'))


@app.route("/login", methods=['POST'])
def login():
    try:
        connection 
        with connection.cursor() as cursor :

            username = request.form.get("username").strip().casefold()
            password = request.form.get("password").strip()
            cursor.execute(
                "SELECT password FROM users WHERE username=(%s)", (username,))
            result = cursor.fetchone()
        if result is None:  # kullanıcı adı bulunamadı
            session["is_wrong"] = True
            return redirect(url_for("index"))

        if check_password_hash(result["password"], password):
            print("şifre doğru :", username)
            session["is_used"] = False
            session["is_wrong"] = False
            session["username"] = username
            return redirect(url_for("index"))

        else:
            session["is_wrong"] = True
            cursor.close()
            return redirect(url_for("index"))
    except:
        session["is_error"] = True
        return redirect(url_for("index"))


@app.route("/send_message", methods=["POST"])
def sendMessage():
    
    session['username'] = 'Arif'
    prompt = request.get_json()
    message = prompt["message"]

    connection
    with connection.cursor() as cursor : 
        cursor.execute("INSERT INTO messages (userid,content,role) VALUES (1,(%s),'user')",(message,))
        cursor.execute('SELECT role,content FROM messages WHERE userid = ( SELECT id from users WHERE username=(%s))',(session['username'],))
        result = cursor.fetchall()

    data = {
        "model": "llama3.1:8b",
        "stream": False,
        "messages": result
    }
        
    response = requests.post("http://localhost:11434/api/chat", json=data)
    with connection : 
        with connection.cursor as cursor :
            cursor.execute('INSERT INTO messages (userid,content,role) VALUES (1,(%s),user)',(message,))
            data = json.loads(response.text)
            cursor.execute('INSERT INTO messages (userid,content,role) VALUES (1,(%s),asistant)',(data.message.content,))
        connection.commit()
    rp = json.dumps(response.text)
    return rp

@app.route("/logout")
def logout():
    session["username"] = None 
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.debug = True
    
    app.run()
