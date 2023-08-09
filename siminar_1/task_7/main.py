

from flask import Flask, render_template
app = Flask(__name__)

news = [
    {
        'title': 'Новость 1',
        'description': 'Краткое описание новости 1',
        'date': '09.08.2023'
    },
    {
        'title': 'Новость 2',
        'description': 'Краткое описание новости 2',
        'date': '09.08.2023'  
    },
    {
        'title': 'Новость 3', 
        'description': 'Краткое описание новости 3',
        'date': '09.08.2023'
    }
]

@app.route('/')
def index():
    return render_template('news.html', news=news)

if __name__ == '__main__':
    app.run()