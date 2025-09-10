from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensaje": "Bienvenido a mi primera API con Flask"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
