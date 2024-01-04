import os
import sqlite3
from app import app
from .thumbnail import Thumbnail
from .database import Database
from .printer import Printer
from flask import render_template
from flask import redirect, url_for
from flask import Flask, request, Response, jsonify

database = Database()
app.config['UPLOAD_FOLDER'] = 'app/static/img/pages/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
@app.route('/index')
def index():
    thumbnail_list = database.get_thumbnail_list()
    return render_template('index.html', thumbnail_list=thumbnail_list)

@app.route('/print_image')
def print_image():
    image_hash = request.args.get('img_hash')
    thumbnail = database.get_thumbnail(image_hash)
    return render_template('print_image.html', thumbnail=thumbnail)

@app.route('/printer')
def printer():
    image_path = request.args.get('image_path')
    printer = Printer(True)
    job_id = printer.print_image(image_path)
    print(f"Printing Job Id: {job_id}:")
    return redirect(url_for('index'))

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'GET':
        return render_template('upload_image.html')
    elif request.method == 'POST':
        print("POST!!!")

#        for i in request.args.keys():
#            print(i)

        if 'file' not in request.files:
            error_message = "File not in request.files"
            return render_template('error.html', error_message=error_message)
        file = request.files['file']
        if file.filename == '':
            error_message = "Empty Filename"
            return render_template('error.html', error_message=error_message)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('index'))

@app.route('/search', methods=['GET','POST'])
def search_image():
    if request.method == 'POST':
      # Log the requestor details to file
      search_text = request.form.get('search_text')
      thumbnail_list = database.search_keywords(search_text.strip().lower())
      return render_template('index.html', thumbnail_list=thumbnail_list)
    else:
      return redirect(url_for('index'))

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    print("AUTOCOMPLETE!!")
    search = request.args.get('query')
    print(f"AUTOCOMPLETE SEARCH: {search}")

    if not search:
        # If no query is provided, return an empty list
        return jsonify([])

    print(f"AUTOCOMPLETE {search}")
    results = database.get_autocomplete(search)
    print("RESULTS", results)
    return results
