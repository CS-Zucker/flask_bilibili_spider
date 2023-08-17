# HOST = '127.0.0.1'
# USER = 'root'
# PASSWORD = '1234'
# PORT = 10306
# DATABASE = 'bilibili'
# CHAREST = 'utf8'


DROP DATABASE IF EXISTS `bilibili`;
DROP DATABASE IF EXISTS `stopword`;

CREATE DATABASE `bilibili`;
CREATE DATABASE `stopword`;


USE `bilibili`;

DROP TABLE IF EXISTS `video`;
CREATE TABLE `video` (
  `video_bv_num` varchar(255) NOT NULL,
  `video_name` varchar(255) DEFAULT NULL,
  `video_up_uid` varchar(255) DEFAULT NULL,
  `video_pub_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`video_bv_num`)
) ENGINE=InnoDB AUTO_INCREMENT=414 DEFAULT CHARSET=utf8;




