/*
Navicat MySQL Data Transfer

Source Server         : Vagrant M2
Source Server Version : 50544
Source Host           : localhost:3306
Source Database       : pibot

Target Server Type    : MYSQL
Target Server Version : 50544
File Encoding         : 65001

Date: 2015-09-01 14:34:18
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `record`
-- ----------------------------
DROP TABLE IF EXISTS `record`;
CREATE TABLE `record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `term_01` float DEFAULT NULL,
  `term_02` float DEFAULT NULL,
  `term_03` float DEFAULT NULL,
  `term_04` float DEFAULT NULL,
  `term_05` float DEFAULT NULL,
  `water_sensor` tinyint(1) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of record
-- ----------------------------
