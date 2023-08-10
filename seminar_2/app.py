from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/process', methods=['POST'])
def process():
    username = request.form['username'] 

    # валидация данных

    resp = make_response(redirect('/welcome'))
    resp.set_cookie('username', username)

    return resp

@app.route('/welcome')
def welcome():
    username = request.cookies.get('username')  
    return render_template('welcome.html', username=username)
    
@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('username')

    return resp

if __name__ == '__main__':
    app.run()