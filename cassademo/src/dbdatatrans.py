# encoding: UTF-8
import threading

import logging.config

logging.config.fileConfig("../conf/cassademolog.conf")
md_logger = logging.getLogger("core.aop.dbdatatrans")


md_logger.debug("debug message")
md_logger.info("info message")
md_logger.warn("warn message")
md_logger.error("error message")
md_logger.critical("critical message")

class DataTransfer():
    def __init__(self):
        self.logger = logging.getLogger("core.aop.dbdatatrans.DataTransfer")
        self.logger.debug("debug message")
        self.logger.info("info message")
        self.logger.warn("warn message")
        self.logger.error("error message")
        self.logger.critical("critical message")
		
dt = DataTransfer()
