INSERT INTO genders (name)
VALUES ('male'), ('female');

INSERT INTO users (name, email, password, age, gender_id)
VALUES ('Maksym', 'maksym@test.com', 'password', 23, 1),
('Olga', 'olga2023@test.com', 'password', 32, 2),
('Oleksandr', 'maksim@test.com', 'password', 40, 1);

INSERT INTO contacts (name, email, phone, favorite, user_id)
VALUES ('Allen Raymond', 'nulla.ante@vestibul.co.uk', '(992) 914-3792', 0, 1),
('Chaim Lewis', 'dui.in@egetlacus.ca', '(294) 840-6685', 1, 1),
('Kennedy Lane', 'mattis.Cras@nonenimMauris.net', '(542) 451-7038', 1, 2),
('Wylie Pope', 'est@utquamvel.net', '(692) 802-2949', 0, 2),
('Cyrus Jackson', 'nibh@semsempererat.com', '(501) 472-5218', 0, null);

INSERT INTO contacts (name, email, phone, favorite, user_id)
VALUES ('Boris Jonson next', 'boris@vestibul.co.uk', '(992) 914-3792', 0, 2);

SELECT id, name, email 
FROM contacts 
WHERE favorite <> TRUE 
ORDER BY name DESC;

SELECT id, name, email 
FROM users 
WHERE age NOT IN (23, 32, 35, 37)
ORDER BY name DESC;


SELECT id, name, email 
FROM contacts 
WHERE created_at  BETWEEN '2023-02-14 18:19:36' AND '2023-02-14 18:23:05'  
ORDER BY name DESC;

SELECT name, email
FROM contacts
WHERE name LIKE '%n'
ORDER BY name;

SELECT COUNT(*)
FROM contacts;

SELECT avg(age) as minAge
FROM users;

SELECT COUNT(user_id) as total_contacts, user_id
FROM contacts
GROUP BY user_id;

SELECT *
FROM contacts
WHERE user_id IN (SELECT id
    FROM users
    WHERE age < 30);
   
SELECT *
FROM contacts c
JOIN users u ON u.id = c.user_id 
WHERE u.age < 36;


UPDATE contacts SET user_id = 3 WHERE id = 5;

ALTER TABLE contacts ADD telegram VARCHAR(30);

CREATE INDEX contacts_email_idx ON contacts (email);
--CREATE INDEX contacts_name_idx ON contacts USING btree (name);


