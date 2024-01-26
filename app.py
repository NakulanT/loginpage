from flask import Flask, render_template,request
from pymongo import MongoClient

connection_string = "mongodb+srv://username:pass@cluster0.gewqhp0.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client.get_database('USER')
collection = db.users


app = Flask(__name__)

#Mongo functions

def register_user(username, password):
    user_data_to_insert = {"username": username, "password": password}
    insert_result = collection.insert_one(user_data_to_insert)
    print(f"Registered user with username: {username}, ID: {insert_result.inserted_id}")


def login_user(username, password):
    user_data = collection.find_one({"username": username, "password": password})
    if user_data:
        print(f"User {username} logged in successfully")
        return True
    else:
        print("Invalid username or password")
        return False
        

#Flask functions

@app.route('/', methods=['GET' , 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if collection.find_one({"username": username}):
             return render_template("signup.html" ,message = True)
        register_user(username,password)
        return render_template("home.html")
            
    return render_template("signup.html" ,message = False)

@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username,password):
            return render_template("home.html")
        else:
            return render_template("signin.html" , error = True)
        
    return render_template("signin.html" , error = False)

if __name__ == '__main__':
    app.run(debug=True)