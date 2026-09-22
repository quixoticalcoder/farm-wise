from flask import Flask, request, jsonify, render_template
from model import model_predict,optimization


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/feature_screen')
def feature_screen():
    return render_template('feature_screen.html')

@app.route('/nutrition')
def nutrition():
    return render_template('nutrition.html')

@app.route('/fruits')
def fruits():
    return render_template('fruits.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/detection_screen')
def detection_screen():
    return render_template('detection_screen.html')

@app.route('/model_insight')
def model_insight():
    return render_template('model_insight.html')

@app.route('/predict/<string:type>', methods=['POST'])
def predict(type):
    form = request.form.to_dict()
    details,form = model_predict(form,type)
    time = 0
    newDetails,time = optimization(type,[details],form,time)
    print(time)
    data = {"data": newDetails,'time':time}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)