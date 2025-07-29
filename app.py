from flask import Flask
from flask import render_template, request, redirect
import sqlite3

import db
import all_recipes

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe_info = request.form.get("recipe")
        title = request.form.get("title")
        all_recipes.add_recipe(title, recipe_info)
        return redirect("/added_recipes")
    return render_template("add_recipe.html")

@app.route("/edit_mode/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = all_recipes.get_recipe(recipe_id)

    if request.method == "GET":
        return render_template("edit_recipe.html", recipe=recipe)
    
    if request.method == "POST":
        title = request.form["title"]
        instructions = request.form["instructions"]
        all_recipes.edit_recipe(recipe_id, title, instructions)
        return redirect("/added_recipes")
    return render_template("edit_recipe.html")


@app.route("/added_recipes", methods=["GET", "POST"])
def added_recipes():
    recipes = all_recipes.get_recipes()
    return render_template("added_recipes.html", recipes=recipes)



