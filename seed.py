import random
import sqlite3

db = sqlite3.connect("database.db")


db.execute("DELETE FROM users")
db.execute("DELETE FROM recipes")
db.execute("DELETE FROM comments")
db.execute("DELETE FROM types")
db.execute("DELETE FROM diets")

with open("init.sql", "r", encoding="utf-8") as file:
    insert_commands = file.read()

db.executescript(insert_commands)

user_count = 1000
recipe_count = 10**5
comment_count = 10**6


for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, recipe_count + 1):
    user_id = random.randint(1, user_count)
    type_id = random.randint(1, 8)
    diet_id = random.randint(1, 8)
    db.execute("INSERT INTO recipes (title, user_id, type_id, diet_id) VALUES (?, ?, ?, ?)",
               ["recipe" + str(i), user_id, type_id, diet_id])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    recipe_id = random.randint(1, recipe_count)
    db.execute("""INSERT INTO comments (comment_text, user_id, recipe_id)
                  VALUES (?, ?, ?)""",
               ["comment" + str(i), user_id, recipe_id])

db.commit()
db.close()
