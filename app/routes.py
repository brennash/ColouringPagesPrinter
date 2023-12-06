import os
import sqlite3
from app import app
from .thumbnail import Thumbnail
from .database import Database
from flask import render_template
from flask import Flask, request, Response


database = Database()
print(os.getcwd())
@app.route('/')
@app.route('/index')
def index():
    thumbnail_list = database.get_thumbnail_list()
    print(len(thumbnail_list))
    return render_template('index.html', thumbnail_list=thumbnail_list)

@app.route('/print_image')
def print_image():
    image_path = request.args.get('image_path')
    return render_template('print_image.html', image_path=image_path)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
  search = request.args.get('q')
  results = ['page1','page2']
  return jsonify(matching_results=results)
