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

USER_COUNT = 1000
RECIPE_COUNT = 10**5
COMMENT_COUNT = 10**6


for i in range(1, USER_COUNT + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, RECIPE_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    type_id = random.randint(1, 8)
    db.execute("INSERT INTO recipes (title, sent_at, user_id, type_id) VALUES (?, datetime('now'), ?, ?)",
               ["recipe" + str(i), user_id, type_id])

for i in range(1, COMMENT_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    recipe_id = random.randint(1, RECIPE_COUNT)
    rating = random.randint(0, 5)
    db.execute("""INSERT INTO comments (comment_text, user_id, recipe_id, sent_at, rating)
                  VALUES (?, ?, ?, datetime('now'), ?)""",
               ["comment" + str(i), user_id, recipe_id, rating])

db.commit()
db.close()
