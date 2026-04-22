from flask import Flask
from app.routes.datasets import datasets_bp
from app.routes.pipeline import pipeline_bp

app = Flask(__name__)

@app.route("/")
def home():
    return "EEG Platform Lite Running"


app.register_blueprint(datasets_bp)
app.register_blueprint(pipeline_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)