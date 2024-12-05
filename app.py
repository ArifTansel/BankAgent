from flask import Flask, render_template, session, redirect, url_for, request
import pymysql.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
from datetime import datetime
from sqlAgent import MySQLAgent

app = Flask(__name__)
#missions : 
# send message daki user id kısmını ayarla
# llm modeline isim bilgisini seessiondan alıp gönder 
# chati temizleme butonu ekle
# mesajları userid ye göre ver 



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
        
        if user_info is not None :
            session["user_information"] = user_info
             
            with connection.cursor() as cursor :
                cursor.execute(" SELECT balance FROM account_info WHERE user_id=(%s)",(user_info["id"],))
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
            cursor.execute("INSERT INTO account_info (user_id,balance) VALUES ((SELECT id FROM users WHERE username=(%s)),100)",(username,))
        
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






@app.route("/transform" , methods=["POST"])
def transform() : 
    userInfo = session.get("user_information",None)
    print("userinfo -------->" , userInfo)
    if userInfo is None :
        raise AssertionError
        
    data = request.get_json()
    # prompt  {'receiver_name': 'asd', 'amount': 'asd'} -> dict 
    # make transition 
    receiverName = data["receiver_name"]
    amount = data["amount"]
    connection 
    with connection.cursor() as cursor : 
        cursor.execute("SELECT id FROM users WHERE username=(%s)",(receiverName,))
        receiverId = cursor.fetchone()
        receiverId =receiverId["id"]
        print(receiverId)
        if receiverId == None :
            # user cannot find 
            return "can't"
        #update money receiver and sender accounts
        #update sender
        cursor.execute("UPDATE account_info SET balance = balance - (%s) WHERE user_id = (%s)",(amount,userInfo["id"]))
        #update receiver
        cursor.execute("UPDATE account_info SET balance = balance + (%s) WHERE user_id = (%s)",(amount,receiverId))
        #log the transformation 
        cursor.execute("INSERT INTO transformation_log (receiver_user_id,sender_user_id,transform_time,amount) VALUES((%s),(%s),(%s),(%s))",(receiverId,userInfo["id"],datetime.now(),amount))
    
    connection.commit()
    return "done" #return new balance 






@app.route("/send_message", methods=["POST"])
def sendMessage():
    prompt = request.get_json()
    message = prompt["message"]
    user_info = session.get("user_information",None)

    agent = MySQLAgent()
    
    rp = json.dumps(agent.ask_sql_agent(message,user_info))
    return rp
    # connection
    # with connection.cursor() as cursor : 
    #     cursor.execute("INSERT INTO messages (user_id,content,role) VALUES (1,(%s),'user')",(message,))
    #     cursor.execute('SELECT role,content FROM messages WHERE user_id = 1') # düzelt
    #     result = cursor.fetchall()

    # data = {
    #     "model": "llama3.1:8b",
    #     "stream": False,
    #     "messages": result
    # }  
    # print("----------------------->" ,data)
        
    # response = requests.post("http://localhost:11434/api/chat", json=data)
    # connection 
    # with connection.cursor() as cursor :
    #     data = json.loads(response.text)
    #     cursor.execute('INSERT INTO messages (user_id,content,role) VALUES (1,(%s),(%s))',(data["message"]["content"],"assistant"))
    # connection.commit()
    # 
    
    # return rp
@app.route("/delete_messages",methods=["POST"])
def delete() :
    connection
    with connection.cursor() as cursor : 
        cursor.execute("DELETE FROM messages ")
    connection.commit()
    return "asd"
@app.route("/logout")
def logout():
    session["username"] = None 
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.debug = True
    
    app.run()
