import db

def get_recipes():
    sql = """SELECT id, title FROM recipes ORDER BY id"""
    
    return db.query(sql)

def get_recipe(recipe_id):
    sql = "SELECT id, title, instructions FROM recipes WHERE id = ?"
    return db.query(sql, [recipe_id])[0]

def add_recipe(title, instructions):
    sql = """INSERT INTO recipes (title, instructions) VALUES (?, ?)"""
    db.execute(sql, (title, instructions))

def edit_recipe(recipe_id, title, instructions):
    sql = """UPDATE recipes SET title = ?, instructions = ? WHERE id = ?"""
    db.execute(sql, [title, instructions, recipe_id])
    