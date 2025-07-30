from flask import Flask
from flask import render_template, request, redirect, session, flash
import sqlite3

import db
import config
import all_recipes
import users

app = Flask(__name__)
app.secret_key = config.secret_key

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
def create_account():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    
    if password1 != password2:
        flash("ERROR: Passwords do not match")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("ERROR: Username is already taken")
        return redirect("/register")

    return redirect("/")


@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
        user_id = users.check_login_credentials(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
       
        else:
            flash("ERROR: Invalid username or password")
            return render_template("login.html", username=username)
        

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        flash("Successfully logged out")
    return redirect("/")
