
create table if not exists `newsurl`(
    `id` int(16) auto_increment,
    `url` varchar(255) default null unique,
    `tag1` varchar(20) default null,
    `tag2` varchar(20) default null,
    `flag` char(2) default null,
    `gaintime` datetime,
		primary key(`id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


create table if not exists `newscontent`(
    `id` int(16),
    `url` varchar(255) default null unique,
    `title` varchar(255) default null,
    `keywords` text default null,
    `description` text default null,
    `h1` text default null,
    `strong` text default null,
    `pcontent` text default null,
    `gaintime` datetime,
		primary key(`id`)
)ENGINE=InnoDB  DEFAULT CHARSET=utf8;

select * from newsurl where url LIKE '%video%'


