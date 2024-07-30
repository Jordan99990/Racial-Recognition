from flask import Flask, render_template
from flask_htmx import HTMX
from flask_assets import Bundle, Environment

app = Flask(__name__)
htmx = HTMX(app)
assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")

if __name__ == "__main__":
    app.run(debug=True)