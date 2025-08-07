CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    instructions TEXT,
    user_id INTEGER REFERENCES users,
    type_id INTEGER REFERENCES types,
    diet_id INTEGER REFERENCES diets
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
    comment_text TEXT,
    rating INTEGER
);

CREATE TABLE connect_recipe_diets (
    recipe_id INTEGER REFERENCES recipes,
    diet_id INTEGER REFERENCES diets
);

CREATE TABLE connect_recipe_types (
    recipe_id INTEGER REFERENCES recipes,
    type_id INTEGER REFERENCES types
);

