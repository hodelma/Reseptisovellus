import time
import math
import secrets
import sqlite3
from flask import Flask
from flask import render_template, request, redirect, session, flash, abort, g
import markupsafe

import config
import all_recipes
import users


app = Flask(__name__)
app.secret_key = config.secret_key


@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response


@app.template_filter()
def show_lines(recipe_content):
    recipe_content = str(markupsafe.escape(recipe_content))
    recipe_content = recipe_content.replace("\n", "<br />")
    return markupsafe.Markup(recipe_content)


@app.route("/")
def index():
    top_recipes = all_recipes.get_top_recipes()
    return render_template("index.html", top_recipes=top_recipes)


def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)

    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if "user_id" not in session:
        flash("You need to log in to add a recipe")
        return redirect("/")

    types = all_recipes.get_types()
    diets = all_recipes.get_diets()

    if request.method == "POST":
        check_csrf()
        instructions = request.form.get("instructions", "").strip()
        title = request.form.get("title", "").strip()
        type = int(request.form.get("type"))
        diets_id = request.form.getlist("diet")

        errors = []

        if not title or len(title) > 100:
            errors.append("ERROR: Title cannot be empty or over 100 characters")

        if not instructions or len(instructions) > 4500:
            errors.append("ERROR: Instructions cannot be empty or over 4500 characters")

        if not type:
            errors.append("ERROR: Recipe type is required")

        if errors:

            for error in errors:
                flash(error)

            return render_template("add_recipe.html", title=title, instructions=instructions,
            type=type, types=types, diets=diets, diets_id=diets_id)

        user_id = session["user_id"]

        all_recipes.add_recipe(title, instructions, type, diets_id, user_id)
        flash("Recipe added successfully!")
        return redirect("/recipes")

    return render_template("add_recipe.html", types=types, diets=diets)


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)

    if not user:
        abort(404)

    recipes = users.get_recipes(user_id)
    return render_template("show_user.html", user=user, recipes=recipes)


@app.route("/edit_mode/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if "user_id" not in session:
        abort(403)

    recipe = all_recipes.get_recipe(recipe_id)

    if recipe["user_id"] != session["user_id"]:
        abort(403)

    types = all_recipes.get_types()
    diets = all_recipes.get_diets()

    type = recipe["type_id"]
    diets_id = []
    if recipe["diet_id"]:
        diets_id = [int(diet) for diet in recipe["diet_id"].split(",")]

    if request.method == "GET":
        return render_template("edit_recipe.html", recipe=recipe, types=types, diets=diets,
        type=type, diets_id=diets_id)

    if request.method == "POST":
        check_csrf()
        title = request.form.get("title", "").strip()
        instructions = request.form.get("instructions", "").strip()
        type = int(request.form.get("type"))
        diets_id = [int(diet) for diet in request.form.getlist("diet")]

        errors = []

        if not title or len(title) > 100:
            errors.append("ERROR: Title cannot be empty or over 100 characters")

        if not instructions or len(instructions) > 4500:
            errors.append("ERROR: Instructions cannot be empty or over 4500 characters")

        if not type:
            errors.append("ERROR: Recipe type is required")

        if errors:

            for error in errors:
                flash(error)

            return render_template("edit_recipe.html", recipe=recipe, title=title,
            instructions=instructions, types=types, diets_id=diets_id, type=type, diets=diets)

        all_recipes.edit_recipe(recipe_id, title, instructions, type, diets_id)
        flash("Recipe edited successfully!")
        return redirect(f"/recipe/{recipe_id}")

    return render_template("edit_recipe.html", recipe=recipe, types=types, diets=diets)


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
        check_csrf()

        if "continue" in request.form:
            all_recipes.remove_recipe(recipe_id)
            flash("Recipe removed successfully!")
            return redirect("/recipes")

        if "cancel" in request.form:
            return redirect(f"/recipe/{recipe_id}")


    return render_template("remove_recipe.html")


@app.route("/recipes", methods=["GET", "POST"])
@app.route("/recipes/<int:page>", methods=["GET", "POST"])
def recipes(page=0):
    page_size = 10
    recipe_count = all_recipes.recipe_count()
    page_count = math.ceil(recipe_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/recipes/1")

    if page > page_count:
        return redirect(f"/recipes/{page_count}")

    recipes = all_recipes.get_recipes(page, page_size)
    return render_template("recipes.html", recipes=recipes, page=page, page_count=page_count)


@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id, page=1):
    recipe = all_recipes.get_recipe(recipe_id)

    if not recipe:
        abort(404)

    page_size = 10
    recipe_count = all_recipes.recipe_count()
    page_count = math.ceil(recipe_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect(f"/recipe/{recipe_id}/1")

    if page > page_count:
        return redirect(f"/recipe/{recipe_id}/{page_count}")

    recipes = all_recipes.get_recipes(page, page_size)
    average_rating, ratings_amount = all_recipes.rating_data(recipe_id)

    return render_template("recipes.html", recipe=recipe, recipes=recipes,
    average_rating=average_rating, ratings_amount=ratings_amount, page=page, page_count=page_count)

@app.route("/register")
def register():
    if "user_id" in session:
        flash("ERROR: You must log out first in order to register")
        return redirect("/")
    return render_template("register.html")


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if "user_id" in session:
        flash("ERROR: You must log out first in order to register")
        return redirect("/")

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password1 = request.form.get("password1", "")
        password2 = request.form.get("password2", "")

        errors = []

        if not username:
            errors.append("ERROR: Empty username")

        if len(username) > 15:
            errors.append("ERROR: Username too long (max 15 characters)")

        if not password1 or len(password1) > 50 or len(password1) < 8:
            errors.append("ERROR: Password must be 8-50 characters")

        if not password2 or len(password2) > 50 or len(password2) < 8:
            errors.append("ERROR: Password confirmation must be 8-50 characters")

        if password1 != password2:
            errors.append("ERROR: Passwords do not match")

        if errors:

            for error in errors:
                flash(error)

            return render_template("register.html", username=username)

        try:
            users.create_user(username, password1)
            flash("You have registered successfully! You can now log in.")
            return redirect("/")

        except sqlite3.IntegrityError:
            flash("ERROR: Username is already taken")
            return render_template("register.html", username=username)

    return render_template("register.html")

@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    if "user_id" in session:
        flash("ERROR: You must log out first in order to log in")
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login_credentials(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
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
@app.route("/search_recipe/<int:page>")
def search(page=1):
    recipe_query = request.args.get("recipe_query", "").strip()
    page_size = 10

    if not recipe_query:
        flash("Entry can't be empty")
        return redirect(f"/recipes/{page}")

    search_count = all_recipes.search_count(recipe_query)
    page_count = math.ceil(search_count["count"] / page_size)
    page_count = max(page_count, 1)
    results = all_recipes.search_recipe(recipe_query, page, page_size)

    if page < 1:
        return redirect("/search_recipe/1")

    if page > page_count:
        return redirect(f"/search_recipe/{page_count}")


    return render_template("recipes.html", recipe_query=recipe_query,
                           results=results, page=page, page_count=page_count)


@app.route("/add_comment", methods=["POST"])
def add_comment():
    if "user_id" not in session:
        flash("You need to log in to add a comment")
        return redirect("/")

    check_csrf()
    comment = request.form.get("comment", "").strip()
    recipe_id = request.form.get("recipe_id")
    rating = int(request.form.get("rating"))

    recipe = all_recipes.get_recipe(recipe_id)
    average_rating, ratings_amount = all_recipes.rating_data(recipe_id)

    errors = []

    if not comment or len(comment) > 2000 or len(comment) < 10:
        errors.append("ERROR: Comment can't be empty and must be between 10 and 2000 characters")

    if rating is None or rating < 0 or rating > 5:
        errors.append("ERROR: Rating must be between 0 and 5")

    if errors:

        for error in errors:
            flash(error)

        return render_template("recipes.html", recipe=recipe, average_rating=average_rating,
        ratings_amount=ratings_amount, comment=comment, rating=rating)

    user_id = session["user_id"]
    all_recipes.add_comment(comment, recipe_id, user_id, rating)
    flash("Comment added successfully!")
    return redirect(f"/show_comments/{recipe_id}")


@app.route("/show_comments/<int:recipe_id>")
@app.route("/show_comments/<int:recipe_id>/<int:page>")
def show_comments(recipe_id, page=0):
    recipe = all_recipes.get_recipe(recipe_id)

    if not recipe:
        abort(404)

    page_size = 10
    comment_count = all_recipes.comment_count(recipe_id)
    page_count = math.ceil(comment_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect(f"/show_comments/{recipe_id}/1")

    if page > page_count:
        return redirect(f"/show_comments/{recipe_id}/{page_count}")

    comments = all_recipes.get_comments(recipe_id, page, page_size)

    return render_template("show_comments.html", recipe=recipe, comments=comments,
    page=page, page_count=page_count)


@app.route("/edit_comment/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    if "user_id" not in session:
        abort(403)

    comment = all_recipes.get_comment(comment_id)

    if comment["user_id"] != session["user_id"]:
        abort(403)

    recipe_id = comment["recipe_id"]

    if request.method == "GET":
        return render_template("edit_comment.html", comment=comment, recipe_id=recipe_id)

    if request.method == "POST":
        check_csrf()
        text = request.form.get("comment", "").strip()
        rating = int(request.form.get("rating"))

        errors = []

        if not text or len(text) > 2000 or len(text) < 10:
            errors.append("ERROR: Comment must be 10-2000 characters")

        if rating is None or rating < 0 or rating > 5:
            errors.append("ERROR: Rating must be between 0 and 5")

        if errors:
            for error in errors:
                flash(error)
                return render_template("edit_comment.html", comment=comment, recipe_id=recipe_id)

        all_recipes.edit_comment(comment_id, text, rating)
        flash("Comment edited successfully")

        return redirect(f"/show_comments/{recipe_id}")


@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def delete_comment(comment_id):
    if "user_id" not in session:
        abort(403)

    comment = all_recipes.get_comment(comment_id)

    if comment["user_id"] != session["user_id"]:
        abort(403)

    recipe_id = comment["recipe_id"]

    if request.method == "GET":
        return render_template("remove_comment.html", comment=comment)

    if request.method == "POST":
        check_csrf()

        if "continue" in request.form:
            all_recipes.remove_comment(comment_id)
            flash("Comment removed successfully")

        return redirect(f"/show_comments/{recipe_id}")

    return render_template("remove_comment.html")
