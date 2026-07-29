from flask import Flask

app = Flask(__name__)

@app.route("/")
def Welcome():
    return "<h1>HELLO WORLD!!</h1>"

if __name__ == "__main__":
    app.run(port=5000, debug=True)