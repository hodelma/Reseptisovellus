CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    instructions TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE types (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE
);

CREATE TABLE diets (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE 
);

CREATE TABLE connect_recipe_diets (
    recipe_id INTEGER
    diet_id INTEGER
);

CREATE TABLE connect_recipe_types (
    recipe_id INTEGER
    type_id INTEGER
);

