import db


def recipe_count():
    sql = "SELECT COUNT(*) FROM recipes"
    return db.query(sql)[0][0]


def comment_count(recipe_id):
    sql = "SELECT COUNT(*) FROM comments WHERE recipe_id = ?"
    return db.query(sql, [recipe_id])[0][0]


def search_count(recipe_query):
    sql = """SELECT COUNT(*) count FROM recipes WHERE title LIKE ?"""
    return db.query(sql, ["%" + recipe_query + "%"])[0]


def get_recipes(page, page_size):
    sql = """SELECT recipes.id,
                    recipes.title,
                    MAX(recipes.sent_at) sent_at,
                    recipes.instructions,
                    types.title type,
                    diets.title diet,
                    users.id user_id,
                    users.username,
                    GROUP_CONCAT(diets.title, ", ") diets
            FROM recipes
            JOIN types ON recipes.type_id = types.id
            JOIN users ON recipes.user_id = users.id
            LEFT JOIN connect_recipe_diets ON recipes.id = connect_recipe_diets.recipe_id
            LEFT JOIN diets ON connect_recipe_diets.diet_id = diets.id
            GROUP BY recipes.id
            ORDER BY recipes.id
            LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])


def get_top_recipes():
    sql = """SELECT recipes.id,
            recipes.title,
            users.username,
            users.id user_id,
            sub.average_rating
        FROM recipes
        JOIN users ON recipes.user_id = users.id
        JOIN (SELECT recipe_id,
            AVG(rating) average_rating
            FROM comments
            GROUP BY recipe_id) sub ON recipes.id = sub.recipe_id
        ORDER BY sub.average_rating DESC
        LIMIT 5"""
    return db.query(sql)


def get_types():
    sql = "SELECT id, title FROM types ORDER BY id"
    return db.query(sql)


def get_diets():
    sql = "SELECT id, title FROM diets ORDER BY id"
    return db.query(sql)


def get_recipe(recipe_id):
    sql = """SELECT recipes.id,
                    recipes.title,
                    recipes.instructions,
                    recipes.sent_at,
                    types.id type_id,
                    types.title type_title,
                    diets.id diet,
                    users.id user_id,
                    users.username,
                    GROUP_CONCAT(diets.id) diet_id,
                    GROUP_CONCAT(diets.title, ", ") AS diets
            FROM recipes
            JOIN types ON recipes.type_id = types.id
            JOIN users ON recipes.user_id = users.id
            LEFT JOIN connect_recipe_diets ON recipes.id = connect_recipe_diets.recipe_id
            LEFT JOIN diets ON diets.id = connect_recipe_diets.diet_id
            WHERE recipes.id = ?
            GROUP BY recipes.id"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None


def get_comment(comment_id):
    sql = """SELECT comments.id,
                    comments.comment_text,
                    comments.rating,
                    users.id user_id,
                    users.username,
                    comments.recipe_id
            FROM comments
            JOIN users ON comments.user_id = users.id
            WHERE comments.id = ?"""
    result = db.query(sql, [comment_id])
    return result[0] if result else None


def get_comments(recipe_id, page, page_size):
    sql = """SELECT comments.id,
                    comments.comment_text,
                    comments.sent_at,
                    comments.rating,
                    comments.user_id,
                    users.username
            FROM comments
            JOIN users ON comments.user_id = users.id
            WHERE comments.recipe_id = ?
            LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    result = db.query(sql, [recipe_id, limit, offset])
    return result


def add_recipe(title, instructions, type_id, diets, user_id):
    sql = """INSERT INTO recipes (title, instructions, sent_at, type_id, user_id)
            VALUES (?, ?, datetime('now', 'localtime'), ?, ?)"""
    db.execute(sql, (title, instructions, type_id, user_id))

    recipe_id = db.last_insert_id()

    sql= """INSERT INTO connect_recipe_diets (recipe_id, diet_id) VALUES (?, ?)"""

    for diet_id in diets:
        db.execute(sql, (recipe_id, diet_id))


def edit_recipe(recipe_id, title, instructions, type_id, diets):
    sql = """UPDATE recipes SET title = ?, instructions = ?, type_id = ? WHERE id = ?"""
    db.execute(sql, [title, instructions, type_id, recipe_id])

    sql = """DELETE FROM connect_recipe_diets WHERE recipe_id = ?"""
    db.execute(sql, [recipe_id])

    if diets:
        sql = """INSERT INTO connect_recipe_diets (recipe_id, diet_id) VALUES (?, ?)"""
        for diet_id in diets:
            db.execute(sql, [recipe_id, diet_id])


def remove_recipe(recipe_id):
    sql = """DELETE FROM connect_recipe_diets WHERE recipe_id = ?"""
    db.execute(sql, [recipe_id])

    sql = """DELETE FROM comments WHERE recipe_id = ?"""
    db.execute(sql, [recipe_id])

    sql = """DELETE FROM recipes WHERE id = ?"""
    db.execute(sql, [recipe_id])


def search_recipe(recipe_query, page, page_size):
    sql = """SELECT recipes.id,
                    recipes.title,
                    recipes.sent_at,
                    users.username,
                    recipes.user_id
            FROM recipes
            JOIN users ON recipes.user_id = users.id
            WHERE recipes.title LIKE ? OR users.username LIKE ?
            ORDER BY recipes.id ASC
            LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, ["%" + recipe_query + "%", "%" + recipe_query + "%", limit, offset])


def add_comment(comment, recipe_id, user_id, rating):
    sql = """INSERT INTO comments (comment_text, recipe_id, sent_at, user_id, rating)
    VALUES (?, ?, datetime('now', 'localtime'), ?, ?)"""
    db.execute(sql, (comment, recipe_id, user_id, rating))


def edit_comment(comment_id, comment, rating):
    sql = """UPDATE comments SET comment_text = ?, rating = ? WHERE id = ?"""
    db.execute(sql, [comment, rating, comment_id])


def remove_comment(comment_id):
    sql = """DELETE FROM comments WHERE id = ?"""
    db.execute(sql, [comment_id])


def rating_data(recipe_id):
    sql = """SELECT AVG(rating) average_rating,
             COUNT(rating) ratings_amount
             FROM comments
             WHERE recipe_id = ?"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None
