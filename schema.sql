CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    instructions TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    type_id INTEGER REFERENCES types
);

CREATE TABLE types (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE
);

CREATE TABLE diets (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE 
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes,
    sent_at TEXT,
    comment_text TEXT,
    rating INTEGER
);

CREATE TABLE connect_recipe_diets (
    recipe_id INTEGER REFERENCES recipes,
    diet_id INTEGER REFERENCES diets
);

CREATE INDEX idx_recipes_sent_at ON recipes(sent_at);
CREATE INDEX idx_comments_recipe ON comments(recipe_id);
CREATE INDEX idx_recipe_diets_recipe ON connect_recipe_diets(recipe_id);
CREATE INDEX idx_recipes_user ON recipes(user_id);