import sqlite3
from flask import Flask
from flask import render_template, request, redirect, session, flash, abort
import markupsafe

import config
import all_recipes
import users


app = Flask(__name__)
app.secret_key = config.secret_key


@app.template_filter()
def show_lines(recipe_content):
    recipe_content = str(markupsafe.escape(recipe_content))
    recipe_content = recipe_content.replace("\n", "<br />")
    return markupsafe.Markup(recipe_content)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if "user_id" not in session:
        flash("You need to log in to add a recipe")
        return redirect("/")

    if request.method == "POST":
        instructions = request.form.get("instructions")
        title = request.form.get("title")

        if not title or len(title) > 100 or len(instructions) > 4500:
            abort(403)

        user_id = session["user_id"]
        all_recipes.add_recipe(title, instructions, user_id)

        return redirect("/added_recipes")

    return render_template("add_recipe.html")


@app.route("/edit_mode/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if "user_id" not in session:
        abort(403)

    recipe = all_recipes.get_recipe(recipe_id)

    if recipe["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_recipe.html", recipe=recipe)

    if request.method == "POST":
        title = request.form["title"]
        instructions = request.form["instructions"]

        if not title or len(title) > 100 or len(instructions) > 4500:
            abort(403)

        all_recipes.edit_recipe(recipe_id, title, instructions)

        return redirect("/added_recipes")

    return render_template("edit_recipe.html")


@app.route("/remove_mode/<int:recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    if "user_id" not in session:
        abort(403)

    recipe = all_recipes.get_recipe(recipe_id)

    if recipe["user_id"] != session["user_id"]:
        abort(403)

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


@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = all_recipes.get_recipe(recipe_id)

    if not recipe:
        abort(404)

    recipes = all_recipes.get_recipes()
    return render_template("added_recipes.html", recipe=recipe, recipes=recipes)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username.strip():
        flash("ERROR: Empty username")
        return render_template("register.html", username=username)

    if len(username) > 15:
        abort(403)

    if password1 != password2:
        flash("ERROR: Passwords do not match")
        return render_template("register.html", username=username)

    try:
        users.create_user(username, password1)
        flash("You have registered successfully!")

    except sqlite3.IntegrityError:
        flash("ERROR: Username is already taken")
        return render_template("register.html", username=username)

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

        flash("ERROR: Invalid username or password")
        return render_template("login.html", username=username)


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        flash("Successfully logged out")
    return redirect("/")


@app.route("/search_recipe")
def search():
    recipe_query = request.args.get("recipe_query")
    recipes = all_recipes.get_recipes()
    results = all_recipes.search_recipe(recipe_query) if recipe_query else []
    return render_template("added_recipes.html", recipe_query=recipe_query,
                           results=results, recipes=recipes)
