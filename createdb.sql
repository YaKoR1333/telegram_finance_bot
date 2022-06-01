CREATE TABLE budget(
    codename VARCHAR(255) PRIMARY KEY,
    daily_limit INTEGER
);

CREATE TABLE category(
    codename VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    is_base_expense bolean,
    aliases text
);

CREATE TABLE expense(
    id INTEGER PRIMARY KEY ,
    amount INTEGER ,
    created datetime,
    category_codename INTEGER ,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

INSERT INTO category (codename, name, is_base_expense, aliases)
VALUES
    ("products", "продукты", true, "еда"),
    ("coffee", "кофе", true, ""),
    ("dinner", "обед", true, "столовая, ланч, бизнес-ланч, бизнес ланч"),
    ("cafe", "кафе", true, "ресторан, рест, мак, макдональдс, макдак, kfc, ilpatio, il patio"),
    ("transport", "общ. транспорт", false, "метро, автобус, metro"),
    ("taxi", "такси", false, "яндекс такси, yandex taxi"),
    ("phone", "телефон", false, "теле2, связь"),
    ("books", "книги", false, "литература, литра, лит-ра"),
    ("internet", "интернет", false, "инет, inet"),
    ("subscriptions", "подписки", false, "подписка"),
    ("other", "прочее", true, "");

INSERT INTO budget(codename, daily_limit) values ('base', 500);