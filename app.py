from flask import Flask
from flask import render_template, request, redirect
from werkzeug.security import generate_password_hash
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
        instructions = request.form.get("instructions")
        title = request.form.get("title")
        all_recipes.add_recipe(title, instructions)
        
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


@app.route("/remove_mode/<int:recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    recipe = all_recipes.get_recipe(recipe_id)

    if request.method == "GET":
        return render_template("remove_recipe.html", recipe=recipe)

    if request.method == "POST":
        if "continue" in request.form:
            all_recipes.remove_recipe(recipe_id)

        return redirect("/added_recipes")
    return render_template("remove_recipe.html")


@app.route("/added_recipes", methods=["GET", "POST"])
def added_recipes():
    recipes = all_recipes.get_recipes()
    return render_template("added_recipes.html", recipes=recipes)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create_account", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "ERROR: Passwords do not match"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])

    except sqlite3.IntegrityError:
        return "ERROR: Credential is already taken"

    return "You have succesfully registered!"


