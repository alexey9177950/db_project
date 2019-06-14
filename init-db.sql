PRAGMA foreign_keys=on;

DROP TABLE IF EXISTS threads;

CREATE TABLE threads (
    thread_id INTEGER PRIMARY KEY,
    op_text VARCHAR,
    header VARCHAR
);

INSERT INTO threads (thread_id, op_text, header)
VALUES (0, 'sample text 1', 'sample header 1'),
       (1, 'sample text 2', 'sample header 2');

DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    thread_id INTEGER,
    text VARCHAR,
    FOREIGN KEY (thread_id) REFERENCES threads(thread_id)
);

INSERT INTO posts (thread_id, text)
VALUES (0, 't1 sample post 1'),
       (0, 't1 sample post 2'),
       (1, 't2 sample post 1'),
       (1, 't2 sample post 2');
