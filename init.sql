docker exec -it db psql -U postgres
\c app;

INSERT INTO users (email,name,password) VALUES
    ('temp@mail.pl','Kamil','haslo1'),
    ('bartek@mail.pl','Bartek','haslo123'),
    ('tomek@mail.pl','Tomek','password');

INSERT INTO continents (name,alias) VALUES
    ('Europa','EU'),
    ('Ameryka Północna','NA'),
    ('Azja','AS');

INSERT INTO countries (name,inhabitants,language,area,pkb,continent_id,user_id) VALUES
    ('Polska',37,'polski',312,811,1,(SELECT id FROM users WHERE name = 'Kamil')),
    ('Niemcy',84,'niemiecki',357,4456,1,(SELECT id FROM users WHERE name = 'Kamil')),
    ('USA',334,'angielski',9834,27360,2,(SELECT id FROM users WHERE name = 'Kamil')),
    ('Chiny',1440,'chiński',9597,16642,3,(SELECT id FROM users WHERE name = 'Bartek'));

INSERT INTO visited (country_name,user_id) VALUES
    ('Włochy',(SELECT id FROM users WHERE name = 'Kamil')),
    ('Austria',(SELECT id FROM users WHERE name = 'Kamil')),
    ('Austria',(SELECT id FROM users WHERE name = 'Bartek')),
    ( 'Polska',(SELECT id FROM users WHERE name = 'Tomek'));


INSERT INTO favourite (country_name,user_id) VALUES
    ('Włochy',(SELECT id FROM users WHERE name = 'Kamil')),
    ('Austria',(SELECT id FROM users WHERE name = 'Bartek')),
    ('Polska',(SELECT id FROM users WHERE name = 'Tomek')),
    ( 'Włochy',(SELECT id FROM users WHERE name = 'Tomek'));