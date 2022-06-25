from flask import Flask, render_template,request
import psycopg2
import psycopg2.extras
from flask import jsonify

app = Flask(__name__)

DB_name='Data'
DB_host='localhost'
DB_port='5555'
DB_user='WEB'
DB_password='qwerty228'

class user():
    def __init__(self, user_id, login):
        user_id = user_id
        login = login

you = user(-1,'')

your_jokes=[]

def connect_to_DB():
    try:
        print("done")
        return psycopg2.connect(dbname=DB_name,user=DB_user,password=DB_password,host=DB_host,port=DB_port)
    except:
        print('Failed Connection')

conn=connect_to_DB()





@app.route('/')
def index():
    return render_template('JokeF.html',message='')

@app.route('/redirerct')
def index_register():
    return render_template('index-register.html')

@app.route('/submit',methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        try:
            conn = connect_to_DB()
            cur=conn.cursor()

            get_query = "SELECT pass FROM users WHERE login=\'{}\'"
            cur.execute(get_query.format(str(login)))
            conn.commit()
            user_password=cur.fetchall()

            if len(user_password[0][0])<8:
                return render_template('index.html', message='There no such login. Try another')
            elif user_password[0][0]!=password:
                return render_template('index.html', message='Wrong password. Try another')
            update_query = "UPDATE users SET last_login = NOW() WHERE login=\'{}\';"
            cur.execute(update_query.format(login))
            conn.commit()
            cur.execute("SELECT user_id FROM users WHERE login=\'{}\' LIMIT 1;".format(login))

            you.mail = request.form['login']
            you.user_id = cur.fetchall()[0][0]

            return render_template('JokeF.html',message='')

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)
            return render_template('index.html',message='Something went wrong. Try again')

        finally:
            if conn:
                cur.close()
                print("PostgreSQL connection is closed")
    if request.method == 'GET':
        try:
            conn = connect_to_DB()
            cur = conn.cursor()
            insert_query = "SELECT joke_content FROM jokes;"


            print(insert_query)
            cur.execute(insert_query)
            conn.commit()
            all = cur.fetchall()
            print(all)
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)

        finally:
            if conn:
                cur.close()
                print("PostgreSQL connection is closed")
        """
        joke = request.form['joke']
        
        try:
            conn = connect_to_DB()
            cur = conn.cursor()
            insert_query = "INSERT INTO jokes(joke_content) VALUES(\'{\"text\":\"%s\",\"author\":%s}\');" % (
            str(joke), you.user_id)
            print(insert_query)
            cur.execute(insert_query)
            conn.commit()

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)

        finally:
            if conn:
                cur.close()
                print("PostgreSQL connection is closed")
        """

    return str(all)

@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        repeat = request.form['repeat']
        if(len(password)<8):
            return render_template('index-register.html', message='Passwords is less than 8 characters. Try again')
        elif(password!=repeat):
            return render_template('index-register.html', message='Passwords are not same. Try again')

        try:
            conn = connect_to_DB()
            cur=conn.cursor()
            insert_query = "INSERT INTO users(login,pass,user_role,created_time) VALUES(\'{}\',\'{}\',\'{}\',NOW());"
            cur.execute(insert_query.format(str(login),str(password),"user"))
            conn.commit()
            return render_template('index.html')
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)
            return render_template('index-register.html',message='Login is used. Try another')
        finally:
            if conn:
                cur.close()
                print("PostgreSQL connection is closed")

@app.route('/exit')
def exit():
    global you
    you = user(-1, '')
    return render_template('index.html',message='')

"""
@app.route('/commit_joke',methods=['POST'])
def joke():
    if request.method == 'POST':

        joke = request.form['joke']

        try:
            conn = connect_to_DB()
            cur=conn.cursor()
            insert_query = "INSERT INTO jokes(joke_content) VALUES(\'{\"text\":\"%s\",\"author\":%s}\');"% (str(joke),you.user_id)
            print(insert_query)
            cur.execute(insert_query)
            conn.commit()

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)

        finally:
            if conn:
                cur.close()
                print("PostgreSQL connection is closed")
    return jsonify(msg='success')
"""




if __name__=="__main__":
    app.run(debug=True)