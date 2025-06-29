##########message_sender.py: [消息发送管理器] ##################
# 变更记录: [2024-12-19 14:30] @李祥光 [初始创建]########
# 变更记录: [2025-06-29 09:47] @李祥光 [修复wxauto V2 API兼容性，移除SendTypingText方法]########
# 输入: 标签和消息内容 | 输出: 发送结果状态###############

import time
from datetime import datetime
from typing import List, Dict, Optional, Any
from wxauto import WeChat
from .logger import Logger
from .contact_manager import ContactManager
from config.settings import config

###########################文件下的所有函数###########################
"""
MessageSender.__init__：初始化消息发送器
MessageSender.send_by_tag：按标签发送消息
MessageSender.send_to_contact：发送消息给指定联系人
MessageSender.send_batch_messages：批量发送消息
MessageSender.validate_message：验证消息内容
MessageSender.get_send_statistics：获取发送统计
MessageSender.retry_failed_sends：重试失败的发送
"""
###########################文件下的所有函数###########################

#########mermaid格式说明所有函数的调用关系说明开始#########
"""
flowchart TD
    A[send_by_tag/按标签发送消息] --> B[get_contacts_by_tag/获取标签下的联系人列表]
    B --> C[validate_message/验证消息内容格式]
    C --> D[send_batch_messages/批量发送消息]
    D --> E[send_to_contact/发送消息给单个联系人]
    E --> F[SendMsg/调用微信发送接口]
    F --> G{发送成功?}
    G -->|是| H[Logger.info/记录成功日志]
    G -->|否| I[retry_failed_sends/重试失败的发送]
    I --> E
"""
#########mermaid格式说明所有函数的调用关系说明结束#########

class MessageSender:
    """
    MessageSender 功能说明:
    消息发送类，负责按标签批量发送消息给联系人
    输入: 标签名和消息内容 | 输出: 发送结果统计
    """
    
    def __init__(self):
        """
        __init__ 功能说明:
        初始化消息发送器
        输入: 无 | 输出: 无
        """
        self.wx = None
        self.contact_manager = ContactManager()
        self.send_interval = config.get('wechat.send_interval', 1.0)
        self.max_retry = config.get('wechat.max_retry', 3)
        self.send_statistics = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'start_time': None,
            'end_time': None,
            'failed_contacts': []
        }
    
    def _init_wechat(self) -> bool:
        """
        _init_wechat 功能说明:
        初始化微信客户端连接
        输入: 无 | 输出: bool 初始化是否成功
        """
        try:
            if self.wx is None:
                Logger.info("正在连接微信客户端...")
                self.wx = WeChat()
                Logger.info("微信客户端连接成功")
            return True
        except Exception as e:
            Logger.error(f"连接微信客户端失败: {str(e)}")
            return False
    
    def validate_message(self, message: str) -> Dict[str, Any]:
        """
        validate_message 功能说明:
        验证消息内容的有效性
        输入: message (str) 消息内容 | 输出: Dict[str, Any] 验证结果
        """
        result = {
            'valid': True,
            'message': '',
            'warnings': []
        }
        
        # 检查消息是否为空
        if not message or not message.strip():
            result['valid'] = False
            result['message'] = '消息内容不能为空'
            return result
        
        # 检查消息长度
        if len(message) > 1000:
            result['warnings'].append('消息内容较长，可能影响发送效果')
        
        # 检查特殊字符
        if any(char in message for char in ['@', '#']):
            result['warnings'].append('消息包含特殊字符，请确认是否正确')
        
        return result
    
    def send_to_contact(self, contact_name: str, message: str) -> Dict[str, Any]:
        """
        send_to_contact 功能说明:
        发送消息给指定联系人
        输入: contact_name (str) 联系人姓名, message (str) 消息内容 | 输出: Dict[str, Any] 发送结果
        """
        result = {
            'success': False,
            'contact': contact_name,
            'message': '',
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            if not self._init_wechat():
                result['message'] = '微信客户端连接失败'
                return result
            
            # 发送消息
            Logger.info(f"正在发送消息给: {contact_name}")
            
            ###########################修改开始 2025-06-29 李祥光  #######################
            # 原代码使用了已废弃的SendTypingText方法：
            # if config.get('message.enable_typing_mode', False):
            #     send_result = self.wx.SendTypingText(message, contact_name, exact=True)
            # else:
            #     send_result = self.wx.SendMsg(message, contact_name, exact=True)
            ###########################修改结束 2025-06-29 李祥光  #######################
            # wxauto V2版本统一使用SendMsg方法发送消息
            send_result = self.wx.SendMsg(message, contact_name, exact=True)
            
            if send_result:
                result['success'] = True
                result['message'] = '发送成功'
                Logger.info(f"消息发送成功: {contact_name}")
            else:
                result['message'] = '微信发送接口返回失败'
                Logger.warning(f"消息发送失败: {contact_name}")
            
        except Exception as e:
            result['message'] = f'发送异常: {str(e)}'
            Logger.error(f"发送消息给 {contact_name} 时出现异常: {str(e)}")
        
        return result
    
    def send_batch_messages(self, contacts: List[Dict], message: str) -> Dict[str, Any]:
        """
        send_batch_messages 功能说明:
        批量发送消息给联系人列表
        输入: contacts (List[Dict]) 联系人列表, message (str) 消息内容 | 输出: Dict[str, Any] 批量发送结果
        """
        self.send_statistics = {
            'total': len(contacts),
            'success': 0,
            'failed': 0,
            'start_time': datetime.now(),
            'end_time': None,
            'failed_contacts': []
        }
        
        Logger.info(f"开始批量发送消息，目标联系人数: {len(contacts)}")
        
        for i, contact in enumerate(contacts, 1):
            contact_name = contact['name']
            
            # 显示进度
            print(f"\r📤 发送进度: {i}/{len(contacts)} - {contact_name}", end='', flush=True)
            
            # 发送消息
            send_result = self.send_to_contact(contact_name, message)
            
            if send_result['success']:
                self.send_statistics['success'] += 1
            else:
                self.send_statistics['failed'] += 1
                self.send_statistics['failed_contacts'].append({
                    'name': contact_name,
                    'error': send_result['message'],
                    'timestamp': send_result['timestamp']
                })
            
            # 发送间隔
            if i < len(contacts):  # 最后一个不需要等待
                time.sleep(self.send_interval)
        
        print()  # 换行
        self.send_statistics['end_time'] = datetime.now()
        
        # 记录统计信息
        duration = (self.send_statistics['end_time'] - self.send_statistics['start_time']).total_seconds()
        Logger.info(f"批量发送完成 - 成功: {self.send_statistics['success']}, 失败: {self.send_statistics['failed']}, 耗时: {duration:.1f}秒")
        
        return {
            'success': self.send_statistics['failed'] == 0,
            'total': self.send_statistics['total'],
            'success_count': self.send_statistics['success'],
            'failed_count': self.send_statistics['failed'],
            'failed_contacts': self.send_statistics['failed_contacts'],
            'duration': duration
        }
    
    def send_by_tag(self, tag: str, message: str) -> Dict[str, Any]:
        """
        send_by_tag 功能说明:
        按标签发送消息给所有匹配的联系人
        输入: tag (str) 标签名, message (str) 消息内容 | 输出: Dict[str, Any] 发送结果
        """
        try:
            # 验证消息内容
            validation = self.validate_message(message)
            if not validation['valid']:
                return {
                    'success': False,
                    'error': validation['message'],
                    'count': 0
                }
            
            # 显示警告信息
            for warning in validation['warnings']:
                Logger.warning(warning)
            
            # 获取标签对应的联系人
            contacts = self.contact_manager.get_contacts_by_tag(tag)
            
            if not contacts:
                return {
                    'success': False,
                    'error': f'标签 "{tag}" 没有匹配的联系人',
                    'count': 0
                }
            
            # 确认发送（如果配置启用）
            if config.get('message.confirm_before_send', True):
                print(f"\n📋 即将发送消息给标签 '{tag}' 的 {len(contacts)} 个联系人:")
                for contact in contacts:
                    print(f"  • {contact['name']}")
                
                print(f"\n📝 消息内容:\n{message}\n")
                
                confirm = input("确认发送吗？(y/N): ").strip().lower()
                if confirm not in ['y', 'yes', '是']:
                    Logger.info("用户取消发送操作")
                    return {
                        'success': False,
                        'error': '用户取消发送',
                        'count': 0
                    }
            
            # 批量发送
            result = self.send_batch_messages(contacts, message)
            
            return {
                'success': result['success'],
                'count': result['success_count'],
                'total': result['total'],
                'failed_count': result['failed_count'],
                'failed_contacts': result['failed_contacts'],
                'duration': result['duration']
            }
            
        except Exception as e:
            Logger.error(f"按标签发送消息失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'count': 0
            }
    
    def retry_failed_sends(self) -> Dict[str, Any]:
        """
        retry_failed_sends 功能说明:
        重试失败的消息发送
        输入: 无 | 输出: Dict[str, Any] 重试结果
        """
        if not self.send_statistics['failed_contacts']:
            return {
                'success': True,
                'message': '没有需要重试的失败发送',
                'retry_count': 0
            }
        
        Logger.info(f"开始重试 {len(self.send_statistics['failed_contacts'])} 个失败的发送")
        
        retry_success = 0
        still_failed = []
        
        for failed_contact in self.send_statistics['failed_contacts']:
            contact_name = failed_contact['name']
            
            # 这里需要重新获取消息内容，实际使用时可能需要传入参数
            # 暂时跳过重试逻辑的具体实现
            Logger.info(f"重试发送给: {contact_name}")
            
            # TODO: 实现具体的重试逻辑
            
        return {
            'success': len(still_failed) == 0,
            'retry_count': retry_success,
            'still_failed': still_failed
        }
    
    def get_send_statistics(self) -> Dict[str, Any]:
        """
        get_send_statistics 功能说明:
        获取发送统计信息
        输入: 无 | 输出: Dict[str, Any] 统计信息
        """
        return self.send_statistics.copy()
    
    def send_test_message(self, test_contact: str = "文件传输助手") -> bool:
        """
        send_test_message 功能说明:
        发送测试消息验证功能
        输入: test_contact (str) 测试联系人 | 输出: bool 测试是否成功
        """
        try:
            test_message = f"标签联系人消息发送器测试\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            result = self.send_to_contact(test_contact, test_message)
            
            if result['success']:
                Logger.info("测试消息发送成功")
                return True
            else:
                Logger.error(f"测试消息发送失败: {result['message']}")
                return False
                
        except Exception as e:
            Logger.error(f"发送测试消息异常: {str(e)}")
            return False