from flask import Flask, render_template, request, redirect, url_for
import pyrebase

config = {
  "apiKey": "YOUR_API_KEY",
  "authDomain": "AUTH_DOMAIN",
  "projectId": "PROJECT_ID",
  "storageBucket": "STORAGE_BUCKET",
  "messagingSenderId": "MESSAGING_SENDER_ID",
  "appId": "APP_ID",
  "databaseURL": "",
}

auth = pyrebase.initialize_app(config)

auth = auth.auth()

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            token = user['idToken']
            return redirect(url_for('profile', token=token))
        except:
            message = 'Invalid credentials. Please try again.'
            return render_template('login.html', message=message)
    else:
        return render_template('login.html')


@app.route('/profile/<token>')
def profile(token):
    try:
        user_info = auth.get_account_info(token)
        email = user_info['users'][0]['email']
        return f'Welcome {email}!'
    except:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
