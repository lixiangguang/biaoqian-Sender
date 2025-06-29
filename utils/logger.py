##########logger.py: [日志管理模块] ##################
# 变更记录: [2024-12-19 14:30] @李祥光 [初始创建]########
# 输入: 无 | 输出: 日志记录器###############

import os
import logging
import coloredlogs
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler

###########################文件下的所有函数###########################
"""
Logger.setup：设置日志记录器
Logger.get_logger：获取日志记录器
Logger.debug：记录调试信息
Logger.info：记录一般信息
Logger.warning：记录警告信息
Logger.error：记录错误信息
Logger.critical：记录严重错误信息
"""
###########################文件下的所有函数###########################

#########mermaid格式说明所有函数的调用关系说明开始#########
"""
flowchart TD
    A[Logger.setup] --> B[创建日志目录]
    B --> C[配置日志格式]
    C --> D[添加文件处理器]
    D --> E[添加控制台处理器]
    F[Logger.info/error等] --> G[_logger.info/error等]
"""
#########mermaid格式说明所有函数的调用关系说明结束#########

class Logger:
    """
    Logger 功能说明:
    日志管理类，提供统一的日志记录接口
    输入: 无 | 输出: 日志记录器
    """
    
    _logger = None
    
    @classmethod
    def setup(cls, log_file="logs/app.log", level="INFO", max_size=10*1024*1024, backup_count=5):
        """
        setup 功能说明:
        设置日志记录器
        输入: log_file (str) 日志文件路径, level (str) 日志级别, max_size (int) 最大文件大小, backup_count (int) 备份文件数量 | 输出: logging.Logger 日志记录器
        """
        # 确保日志目录存在
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建日志记录器
        logger = logging.getLogger("biaoqian-sender")
        logger.setLevel(getattr(logging, level))
        
        # 清除已有的处理器
        if logger.handlers:
            logger.handlers.clear()
        
        # 创建文件处理器
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        
        # 创建格式化器
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # 设置文件处理器格式
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # 设置控制台彩色日志
        coloredlogs.install(
            level=level,
            logger=logger,
            fmt="[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # 记录启动信息
        logger.info("日志系统初始化完成")
        
        cls._logger = logger
        return logger
    
    @classmethod
    def get_logger(cls):
        """
        get_logger 功能说明:
        获取日志记录器，如果未初始化则自动初始化
        输入: 无 | 输出: logging.Logger 日志记录器
        """
        if cls._logger is None:
            cls.setup()
        return cls._logger
    
    @classmethod
    def debug(cls, message):
        """
        debug 功能说明:
        记录调试信息
        输入: message (str) 日志消息 | 输出: 无
        """
        logger = cls.get_logger()
        logger.debug(message)
    
    @classmethod
    def info(cls, message):
        """
        info 功能说明:
        记录一般信息
        输入: message (str) 日志消息 | 输出: 无
        """
        logger = cls.get_logger()
        logger.info(message)
    
    @classmethod
    def warning(cls, message):
        """
        warning 功能说明:
        记录警告信息
        输入: message (str) 日志消息 | 输出: 无
        """
        logger = cls.get_logger()
        logger.warning(message)
    
    @classmethod
    def error(cls, message):
        """
        error 功能说明:
        记录错误信息
        输入: message (str) 日志消息 | 输出: 无
        """
        logger = cls.get_logger()
        logger.error(message)
    
    @classmethod
    def critical(cls, message):
        """
        critical 功能说明:
        记录严重错误信息
        输入: message (str) 日志消息 | 输出: 无
        """
        logger = cls.get_logger()
        logger.critical(message)