from flask import Flask, render_template
from app.routes.datasets import datasets_bp
from app.routes.pipeline import pipeline_bp

app = Flask(__name__)
app.json.indent = 4  # Pretty-print JSON responses

@app.route("/")
def home():
    return "Home page of Backend Project"

@app.route("/ui")
def ui():
    return render_template("index.html")


app.register_blueprint(datasets_bp)
app.register_blueprint(pipeline_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)