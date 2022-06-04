CREATE TABLE budget(
    codename VARCHAR(255) PRIMARY KEY,
    month_limit INTEGER
);

CREATE TABLE category(
    codename VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
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

INSERT INTO category (codename, name, aliases)
VALUES
    ("products", "продукты", "еда, пятёрочка, пятерочка, магнит, спар"),
    ("health", "здоровье", "больница, зубной"),
    ("Clothing", "одежда", "шмотки, обувь, тапки, шопинг"),
    ("Pets", "домашние животные", "корм, ветеринарка, коты"),
    ("cafe", "кафе", "ресторан, рест, мак, макдональдс, макдак, kfc, додо, пицца, бургер-кинг, суши"),
    ("transport", "общ. транспорт", "метро, автобус, metro, троллейбус, маршрутка"),
    ("taxi", "такси", "яндекс такси, yandex taxi"),
    ("phone", "телефон", "теле2, связь, билайн, мтс, йота"),
    ("books", "книги", "литература, литра, лит-ра"),
    ("internet", "интернет", "инет, inet"),
    ("subscriptions", "подписки", "подписка"),
    ("Apartment", "Кварплата", "ЖКХ, газ, электричество, вода"),
    ("Lunch", "обед", "столовая, ланч, бизнес ланч, бизнес-ланч"),
    ("Medications", "Лекарства", "аптека, таблетки"),
    ("Entertainment", "Развлечения", "кино, театр, квест, самокаты"),
    ("Poker", "покер", ""),
    ("other", "прочее", "");

INSERT INTO budget(codename, month_limit) values ('base', 10000);