import db


def get_recipes():
    sql = """SELECT id, title, instructions, user_id FROM recipes ORDER BY id"""
    return db.query(sql)


def get_recipe(recipe_id):
    sql = "SELECT id, title, instructions, user_id FROM recipes WHERE id = ?"
    return db.query(sql, [recipe_id])[0]


def add_recipe(title, instructions, user_id):
    sql = """INSERT INTO recipes (title, instructions, user_id) VALUES (?, ?, ?)"""
    db.execute(sql, (title, instructions, user_id))


def edit_recipe(recipe_id, title, instructions):
    sql = """UPDATE recipes SET title = ?, instructions = ? WHERE id = ?"""
    db.execute(sql, [title, instructions, recipe_id])


def remove_recipe(recipe_id):
    sql = """DELETE FROM recipes WHERE id = ?"""
    db.execute(sql, [recipe_id])


def search_recipe(recipe_query):
    sql = """SELECT id, title FROM recipes WHERE title LIKE ?"""
    return db.query(sql, ["%" + recipe_query + "%"])