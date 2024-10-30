from flask import Flask, render_template, session, redirect, url_for, request
from flask_mysql_connector import MySQL
from werkzeug.security import generate_password_hash ,check_password_hash
app = Flask(__name__)

app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = 'patatoes'
app.config['MYSQL_DATABASE'] = "aisec"
mysql = MySQL(app)

app.secret_key = 'THIS_IS_BAD'


@app.route("/")
def index():
    username = session.get("username", None)
    error = session.get("is_error", False)
    is_used = session.get("is_used", False)
    is_wrong = session.get("is_wrong", False)
    return render_template("index.html", username=username, is_error=error, is_used=is_used, is_wrong=is_wrong)


@app.route("/signup", methods=['POST'])
def signUp():
    session["is_used"] = False
    cursor = mysql.connection.cursor()
    username = request.form.get("username").strip().casefold()
    mail = request.form.get("email").strip()
    password = request.form.get("password").strip()
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, mail, hashed_password))
    mysql.connection.commit()
    cursor.close()
    session["is_used"] = False

    # except:
    #     session["is_used"] = True
    return redirect(url_for('index'))


@app.route("/login", methods=['POST'])
def login():
    try :
        cursor = mysql.connection.cursor()
        username = request.form.get("username").strip().casefold()
        password = request.form.get("password").strip()
        cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
        result = cursor.fetchone()
        cursor.close()
        if result is None:  # kullanıcı adı bulunamadı
            session["is_wrong"] = True
            return redirect(url_for("index"))

        if check_password_hash(result[0],password):
            print("şifre doğru :" , username)
            session["username"] = username
            return redirect(url_for("index"))

        else:
            session["is_wrong"] = True
            cursor.close()
            return redirect(url_for("index"))
    except:
        print("hata")
        session["is_error"] = True
        return redirect(url_for("index"))
@app.route("/send_message",methods=["POST"])
def sendMessage() : 
    return redirect(url_for(index))

if __name__ == "__main__":
    app.debug = True
    app.run()

# cursor = mysql.connection.cursor()
# cursor.execute("INSERT INTO users (username,email,password) VALUES ('asdasd','blabla','patates')")
# mysql.connection.commit()
# cursor.close()
