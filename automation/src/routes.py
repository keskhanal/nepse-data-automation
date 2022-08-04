import os
from flask import render_template, request, send_from_directory, url_for, redirect

from src import app
from .automation import automate

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        scripts = request.form.get("scripts")
        try:
            final_df = automate(scripts)

            file_name = scripts +".csv"
            final_df.to_csv("data/" + file_name, encoding='utf-8', index=False)
            return redirect(url_for("download"))
            
        except:
            return redirect(url_for("index"))

    return render_template("home.html")


@app.route("/download")
def download():
    return render_template("download.html", files=os.listdir('data'))


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory("../data", filename, as_attachment=True)