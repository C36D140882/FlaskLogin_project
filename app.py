from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from mongodb import collection

app = Flask(__name__)

# --- Register
@app.route('/', methods=['GET', 'POST'])  
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        compassd = request.form.get('Compassword')
        existing_user=collection.find_one({'$or':[{"username": username},{'email':email},{'password':password}]}) 
        if existing_user:
            if existing_user.get('username') == username:
                message='Username already exists!'
            elif existing_user.get('email') == email:
                message='Email already exists!'
            elif existing_user.get('password') == password:
                message='Password already exists!'     
            else:
                message='User already exists!'       
            return render_template('register.html',message=message)
        if password == compassd:
            collection.insert_one({
                "username": username,
                "email": email,
                "password": password,
                "Created at": datetime.now()
            })
            return redirect(url_for('login')) 
        else:
            return render_template('register.html', message="Password do not match!")
    return render_template('register.html')

# ----Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST': 
        username = request.form.get('username')
        password = request.form.get('password')
        user = collection.find_one({'username': username})
        if not user:
            return render_template('login.html', message='user not found!')
        if user and user['password'] == password:
            return render_template('dashboard.html',user=username)
        return render_template('login.html', messsage="password is incorrect!")
    return render_template('login.html')

# --Forget Password 
@app.route('/forget', methods=['GET','POST'])
def forget():
    if request.method == 'POST':
        old_passd=request.form.get('oldpassword')
        new_passd=request.form.get('newpassword')
        com_passd=request.form.get('compassword')
        user=collection.find_one({'password':old_passd})
        if user:
            if new_passd == com_passd:
                collection.update_one(
                    {'password':old_passd,},
                    {'$set':{'password':new_passd}}
                )
                return redirect(url_for('login'))             
            else:
                return render_template('forget.html',message='new password do not match!')
        else:
            return render_template('forget.html',message='old password is incorrect!')    
    return render_template('forget.html')

if __name__ == '__main__':
    app.run(debug=True,port=4999,host='0.0.0.0')    