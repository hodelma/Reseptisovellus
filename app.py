from flask import Flask
from flask import render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_recipe")
def add_recipe():
    return render_template("add_recipe.html")

@app.route("/added_recipes", methods=["POST"])
def added_recipes():
    recipes = request.form.getlist("recipe")
    recipe = request.form["recipe"]
    return render_template("/added_recipes.html",recipe=recipe, recipes=recipes)



