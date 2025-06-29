##########test_basic.py: 基础功能测试模块 ##################
# 变更记录: [2024-12-19 14:30] @李祥光 [初始创建]########
# 输入: 测试用例 | 输出: 测试结果###############

import unittest
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import Config
from utils.logger import Logger
from utils.contact_manager import ContactManager
from utils.message_sender import MessageSender

###########################文件下的所有函数###########################
"""
TestConfig.test_config_creation：测试配置创建
TestConfig.test_config_get_set：测试配置读写
TestLogger.test_logger_creation：测试日志创建
TestContactManager.test_contact_manager_init：测试联系人管理器初始化
TestMessageSender.test_message_validation：测试消息验证
"""
###########################文件下的所有函数###########################

#########mermaid格式说明所有函数的调用关系说明开始#########
"""
flowchart TD
    A[unittest.main] --> B[TestConfig]
    A --> C[TestLogger]
    A --> D[TestContactManager]
    A --> E[TestMessageSender]
    B --> F[test_config_creation]
    B --> G[test_config_get_set]
    C --> H[test_logger_creation]
    D --> I[test_contact_manager_init]
    E --> J[test_message_validation]
"""
#########mermaid格式说明所有函数的调用关系说明结束#########

class TestConfig(unittest.TestCase):
    """
    TestConfig 功能说明:
    测试配置管理模块的基础功能
    输入: 测试用例 | 输出: 测试结果
    """
    
    def test_config_creation(self):
        """
        test_config_creation 功能说明:
        测试配置对象的创建
        输入: 无 | 输出: 断言结果
        """
        config = Config()
        self.assertIsNotNone(config)
        self.assertIsInstance(config.config_data, dict)
    
    def test_config_get_set(self):
        """
        test_config_get_set 功能说明:
        测试配置的读取和设置功能
        输入: 无 | 输出: 断言结果
        """
        config = Config()
        
        # 测试默认值获取
        app_name = config.get('app.name', 'default')
        self.assertIsNotNone(app_name)
        
        # 测试设置和获取
        test_key = 'test.key'
        test_value = 'test_value'
        config.set(test_key, test_value)
        retrieved_value = config.get(test_key)
        self.assertEqual(retrieved_value, test_value)

class TestLogger(unittest.TestCase):
    """
    TestLogger 功能说明:
    测试日志管理模块的基础功能
    输入: 测试用例 | 输出: 测试结果
    """
    
    def test_logger_creation(self):
        """
        test_logger_creation 功能说明:
        测试日志对象的创建
        输入: 无 | 输出: 断言结果
        """
        logger = Logger()
        self.assertIsNotNone(logger)
        
        # 测试日志方法存在
        self.assertTrue(hasattr(Logger, 'info'))
        self.assertTrue(hasattr(Logger, 'error'))
        self.assertTrue(hasattr(Logger, 'warning'))
        self.assertTrue(hasattr(Logger, 'debug'))

class TestContactManager(unittest.TestCase):
    """
    TestContactManager 功能说明:
    测试联系人管理模块的基础功能
    输入: 测试用例 | 输出: 测试结果
    """
    
    def test_contact_manager_init(self):
        """
        test_contact_manager_init 功能说明:
        测试联系人管理器的初始化
        输入: 无 | 输出: 断言结果
        """
        # 使用测试数据文件路径
        test_data_file = "tests/test_contacts.json"
        manager = ContactManager(test_data_file)
        
        self.assertIsNotNone(manager)
        self.assertIsInstance(manager.contacts, list)
        
        # 测试方法存在
        self.assertTrue(hasattr(manager, 'add_tag'))
        self.assertTrue(hasattr(manager, 'remove_tag'))
        self.assertTrue(hasattr(manager, 'get_contacts_by_tag'))

class TestMessageSender(unittest.TestCase):
    """
    TestMessageSender 功能说明:
    测试消息发送模块的基础功能
    输入: 测试用例 | 输出: 测试结果
    """
    
    def test_message_validation(self):
        """
        test_message_validation 功能说明:
        测试消息内容验证功能
        输入: 无 | 输出: 断言结果
        """
        sender = MessageSender()
        
        # 测试空消息
        result = sender.validate_message("")
        self.assertFalse(result['valid'])
        
        # 测试正常消息
        result = sender.validate_message("这是一条测试消息")
        self.assertTrue(result['valid'])
        
        # 测试过长消息
        long_message = "测试" * 500  # 1000个字符
        result = sender.validate_message(long_message)
        self.assertTrue(result['valid'])  # 应该有效但有警告
        self.assertGreater(len(result['warnings']), 0)

class TestIntegration(unittest.TestCase):
    """
    TestIntegration 功能说明:
    集成测试，测试模块间的协作
    输入: 测试用例 | 输出: 测试结果
    """
    
    def test_modules_import(self):
        """
        test_modules_import 功能说明:
        测试所有模块能否正常导入
        输入: 无 | 输出: 断言结果
        """
        try:
            from config.settings import config
            from utils.logger import Logger
            from utils.contact_manager import ContactManager
            from utils.message_sender import MessageSender
            
            # 如果能执行到这里说明导入成功
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"模块导入失败: {str(e)}")
    
    def test_basic_workflow(self):
        """
        test_basic_workflow 功能说明:
        测试基本工作流程
        输入: 无 | 输出: 断言结果
        """
        try:
            # 初始化组件
            Logger.info("开始集成测试")
            
            # 测试联系人管理器
            manager = ContactManager("tests/test_contacts.json")
            self.assertIsNotNone(manager)
            
            # 测试消息发送器
            sender = MessageSender()
            self.assertIsNotNone(sender)
            
            # 测试消息验证
            validation = sender.validate_message("测试消息")
            self.assertTrue(validation['valid'])
            
            Logger.info("集成测试完成")
            
        except Exception as e:
            self.fail(f"集成测试失败: {str(e)}")

if __name__ == '__main__':
    # 创建测试目录
    test_dir = Path('tests')
    test_dir.mkdir(exist_ok=True)
    
    # 运行测试
    unittest.main(verbosity=2)