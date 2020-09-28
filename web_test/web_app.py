from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('bar_graph.html')

@app.route('/test01')
def test01():
    return render_template('bar_test01.html')

@app.route('/test02')
def test02():
    return render_template('bar_test02.html')

@app.route('/test03')
def test03():
    return render_template('javascript.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="7070", debug="True")