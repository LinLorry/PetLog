USE PetShow

CREATE TABLE users
{
user_id CHAR(16) NOT NULL,
user_name VARCHAR(20) NOT NULL,
user_nickname VARCHAR(20) NOT NULL,
password_hash CHAR(128) NOT NULL,
phonenumber CHAR(11) NULL,
gender CHAR(1) NULL,
head_portrait_path VARCHAR(128) NULL,
motto VARCHAR(256) NULL,
address VARCHAR(128) NULL,
joined_time datetime NOT NULL,
grade TINYINT NOT NULL,

PRIMARY KEY ('user_id')
};ENGINE=InnoDB

CREATE TABLE tags
{
tag_id CHAR(16) NOT NULL,
tag_name VARCHAR(32) NOT NULL,

PRIMARY KEY('tag_id')
};ENGINE=InnoDB

CREATE TABLE cards
{
card_id CHAR(16) NOT NULL,
user_id CHAR(16) NOT NULL,
card_content text NULL,
card_image_path VARCHAR(128) NULL,
card_time datetime NOT NULL,

PRIMARY KEY (card_id),
CONSTRAINT u_id FREIGN KEY (user_id) REFERENCES users(user_id)
};ENGINE=InnoDB

CREATE TABLE card_with_tag
{
card_id CHAR(16) NOT NULL,
tag_id CHAR(16) NOT NULL,

PRIMARY KEY (tag_id),
CONSTRAINT c_id FREIGN KEY (card_id) REFERENCES cards(card_id)
};ENGINE=InnoDB

CREATE TABLE comments
{
comments_id CHAR(16) NOT NULL,
card_id CHAR(16) NOT NULL,
to_user_id CHAR(16) NULL,
comment_content text NOT NULL,

PRIMARY KEY ('comments_id'),
CONSTRAINT t_u_id FREIGN KEY (to_user_id) REFERENCES users(user_id),
};ENGINE=InnoDB

CREATE TABLE praise
{
card_id CHAR(16) NOT NULL,
user_id CHAR(16) NOT NULL
CONSTRAINT c_id FREIGN KEY (card_id) REFERENCES cards(card_id),
CONSTRAINT u_id FREIGN KEY (user_id) REFERENCES users(user_id)
};ENGINE=InnoDB

CREATE TABLE share_card
{
card_id CHAR(16) NOT NULL,
CONSTRAINT c_id FREIGN KEY (card_id) REFERENCES cards(card_id)
};ENGINE=InnoDB

CREATE TABLE pets
{
pet_id CHAR(16) NOT NULL,
category VARCHAR(32) NOT NULL,
detailed_category VARCHAR(64) NULL,
pet_name VARCHAR(20) NOT NULL,
user_id CHAR(16) NOT NULL,
time datetime NOT NULL,
gender CHAR(1) NOT NULL,

PRIMARY KEY ('pet_id'),
CONSTRAINT u_id FREIGN KEY (user_id) REFERENCES users(user_id)
};ENGINE=InnoDB










