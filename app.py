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
        type = request.form.get("type")
        diet = request.form.get("diet")

        if not title or len(title) > 100 or len(instructions) > 4500:
            abort(403)

        user_id = session["user_id"]
        all_recipes.add_recipe(title, instructions, type, diet, user_id)

        return redirect("/added_recipes")

    return render_template("add_recipe.html")


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
    average_rating, ratings_amount = all_recipes.rating_data(recipe_id)

    return render_template("added_recipes.html", recipe=recipe, recipes=recipes,
    average_rating=average_rating, ratings_amount=ratings_amount)

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


@app.route("/add_comment", methods=["POST"])
def add_comment():
    if "user_id" not in session:
        flash("You need to log in to add a comment")
        return redirect("/")

    if request.method == "POST":
        comment = request.form.get("comment")
        recipe_id = request.form.get("recipe_id")
        rating = int(request.form.get("rating"))

        if not comment or len(comment) > 2000 or len(comment) < 10:
            abort(403)

        if rating is None or rating < 0 or rating > 5:
            abort(400)

        user_id = session["user_id"]
        all_recipes.add_comment(comment, recipe_id, user_id, rating)

        return redirect(f"/show_comments/{recipe_id}")

    return render_template("show_comments.html")


@app.route("/show_comments/<int:recipe_id>")
def show_comments(recipe_id):
    recipe = all_recipes.get_recipe(recipe_id)
    comments = all_recipes.get_comments(recipe_id)

    if not recipe:
        abort(404)

    return render_template("show_comments.html", recipe=recipe, comments=comments)


@app.route("/edit_comment/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    if "user_id" not in session:
        abort(403)

    comment = all_recipes.get_comment(comment_id)

    if comment["user_id"] != session["user_id"]:
        abort(403)

    recipe_id = comment["recipe_id"]

    if request.method == "GET":
        return render_template("edit_comment.html", comment=comment)

    if request.method == "POST":
        text = request.form["comment"]
        rating = int(request.form["rating"])

        if not text or len(text) > 2000 or len(text) < 10:
            abort(403)

        if rating is None or rating < 0 or rating > 5:
            abort(403)

        all_recipes.edit_comment(comment_id, text, rating)

        return redirect(f"/show_comments/{recipe_id}")

    return render_template("edit_comment.html")


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

        if "continue" in request.form:
            all_recipes.remove_comment(comment_id)

        return redirect(f"/show_comments/{recipe_id}")

    return render_template("remove_comment.html")
