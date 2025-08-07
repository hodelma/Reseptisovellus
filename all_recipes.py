import db


def get_recipes():
    sql = """SELECT recipes.id,
                    recipes.title,
                    recipes.instructions,
                    types.title type,
                    diets.title diet,
                    users.id user_id,
                    users.username
            FROM recipes
            JOIN types ON recipes.type_id = types.id
            JOIN diets ON recipes.diet_id = diets.id
            JOIN users ON recipes.user_id = users.id
            ORDER BY recipes.id"""
    return db.query(sql)


def get_recipe(recipe_id):
    sql = """SELECT recipes.id, 
                    recipes.title, 
                    recipes.instructions,
                    types.title type,
                    diets.title diet,
                    users.id user_id, 
                    users.username
            FROM recipes
            JOIN types ON recipes.type_id = types.id
            JOIN diets ON recipes.diet_id = diets.id
            JOIN users ON recipes.user_id = users.id
            WHERE recipes.id = ?"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None


def add_recipe(title, instructions, type_id, diet_id, user_id):
    sql = """INSERT INTO recipes (title, instructions, type_id, diet_id, user_id) VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, (title, instructions, type_id, diet_id, user_id))


def edit_recipe(recipe_id, title, instructions):
    sql = """UPDATE recipes SET title = ?, instructions = ? WHERE id = ?"""
    db.execute(sql, [title, instructions, recipe_id])


def remove_recipe(recipe_id):
    sql = """DELETE FROM recipes WHERE id = ?"""
    db.execute(sql, [recipe_id])


def search_recipe(recipe_query):
    sql = """SELECT id, title FROM recipes WHERE title LIKE ?"""
    return db.query(sql, ["%" + recipe_query + "%"])