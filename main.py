from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    message = 'A message from the backend'
    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
