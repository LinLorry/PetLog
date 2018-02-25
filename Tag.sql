CREATE TABLE IF NOT EXISTS Tags(
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO Tags
(name)
VALUE
("可爱"),
("狗狗"),
("猫咪"),
("小鸟"),
("玩耍"),
("调皮"),
("高冷"),
("活泼"),
("别开玩笑了！");