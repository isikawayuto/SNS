CREATE TABLE snsaccount2 (
    id serial,
    userid VARCHAR(16),
    name VARCHAR(64),
    birthday VARCHAR(16),
    filename VARCHAR(64),
    mail VARCHAR(256) unique,
    salt VARCHAR(32),
    password VARCHAR(64),
    PRIMARY KEY(id)
);
CREATE TABLE snspost2 (
    id serial,
    mail VARCHAR(256),
    name VARCHAR(64),
    body text,
    filename VARCHAR(64),
    created_at  date,
    PRIMARY KEY(id),
    FOREIGN KEY(mail)
    REFERENCES snsaccount2(mail)
);