import db

def get_recipes():
    sql = """SELECT id, title FROM recipes ORDER BY id"""
    
    return db.query(sql)

def add_recipe(title, instructions):
    sql = """INSERT INTO recipes (title, instructions) VALUES (?, ?)"""
    db.execute(sql, (title, instructions))