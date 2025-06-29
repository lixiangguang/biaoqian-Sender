##########friend_details.py: [微信好友详细信息获取模块] ##################
# 变更记录: [2025-06-30 10:15] @李祥光 [初始创建]########
# 输入: 无 | 输出: 好友详细信息列表###############

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from wxautox import WeChat
from .logger import Logger
from .contact_manager import ContactManager

###########################文件下的所有函数###########################
"""
FriendDetailsManager.__init__：初始化好友详细信息管理器
FriendDetailsManager.get_friend_details：获取好友详细信息
FriendDetailsManager.save_friend_details：保存好友详细信息到文件
FriendDetailsManager.load_friend_details：从文件加载好友详细信息
FriendDetailsManager.sync_to_contacts：将好友详细信息同步到联系人管理器
FriendDetailsManager.get_friend_by_name：根据名称获取好友详细信息
"""
###########################文件下的所有函数###########################

#########mermaid格式说明所有函数的调用关系说明开始#########
"""
flowchart TD
    A[FriendDetailsManager初始化] --> B[load_friend_details]
    B --> C{数据文件存在?}
    C -->|是| D[读取JSON数据]
    C -->|否| E[get_friend_details]
    E --> F[save_friend_details]
    G[sync_to_contacts] --> H[更新联系人数据]
    H --> I[ContactManager.add_contact]
"""
#########mermaid格式说明所有函数的调用关系说明结束#########

class FriendDetailsManager:
    """
    FriendDetailsManager 功能说明:
    微信好友详细信息管理类，负责获取、存储和管理微信好友的详细信息
    输入: 无 | 输出: 好友详细信息列表
    """
    
    def __init__(self, data_file: str = "data/friend_details.json"):
        """
        __init__ 功能说明:
        初始化好友详细信息管理器
        输入: data_file (str) 数据文件路径 | 输出: 无
        """
        self.data_file = Path(data_file)
        self.friend_details: List[Dict] = []
        self.load_friend_details()
    
    def get_friend_details(self, max_count: int = None, timeout: int = 0xFFFFF) -> List[Dict]:
        """
        get_friend_details 功能说明:
        从微信客户端获取好友详细信息
        输入: max_count (int) 最大获取数量, timeout (int) 超时时间 | 输出: List[Dict] 好友详细信息列表
        """
        try:
            Logger.info("开始从微信获取好友详细信息...")
            
            # 初始化微信客户端
            wx = WeChat()
            
            # 调用wxauto的GetFriendDetails方法获取好友详细信息
            friend_details = wx.GetFriendDetails(n=max_count, timeout=timeout)
            
            if not friend_details:
                Logger.warning("未获取到好友详细信息")
                return []
            
            # 添加时间戳
            for friend in friend_details:
                friend['updated_at'] = datetime.now().isoformat()
            
            self.friend_details = friend_details
            self.save_friend_details()
            
            Logger.info(f"成功获取 {len(friend_details)} 个好友详细信息")
            return friend_details
            
        except Exception as e:
            Logger.error(f"获取好友详细信息失败: {str(e)}")
            return []
    
    def save_friend_details(self) -> bool:
        """
        save_friend_details 功能说明:
        保存好友详细信息到文件
        输入: 无 | 输出: bool 保存是否成功
        """
        try:
            # 确保目录存在
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'friend_details': self.friend_details,
                'last_updated': datetime.now().isoformat(),
                'count': len(self.friend_details)
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            Logger.info(f"好友详细信息已保存到 {self.data_file}")
            return True
            
        except Exception as e:
            Logger.error(f"保存好友详细信息失败: {str(e)}")
            return False
    
    def load_friend_details(self) -> List[Dict]:
        """
        load_friend_details 功能说明:
        从文件加载好友详细信息
        输入: 无 | 输出: List[Dict] 好友详细信息列表
        """
        try:
            if not self.data_file.exists():
                Logger.warning(f"好友详细信息文件不存在: {self.data_file}")
                return []
                
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.friend_details = data.get('friend_details', [])
            Logger.info(f"已从 {self.data_file} 加载 {len(self.friend_details)} 个好友详细信息")
            return self.friend_details
            
        except Exception as e:
            Logger.error(f"加载好友详细信息失败: {str(e)}")
            return []
    
    def sync_to_contacts(self) -> Dict:
        """
        sync_to_contacts 功能说明:
        将好友详细信息同步到联系人管理器
        输入: 无 | 输出: Dict 同步结果统计
        """
        try:
            if not self.friend_details:
                Logger.warning("没有好友详细信息可同步")
                return {'success': False, 'error': '没有好友详细信息可同步'}
                
            contact_manager = ContactManager()
            count = 0
            
            for friend in self.friend_details:
                # 提取必要信息
                name = friend.get('NickName', '')
                if not name:
                    continue
                    
                # 添加到联系人管理器
                result = contact_manager.add_contact(name, tags=['微信好友'])
                if result['success']:
                    count += 1
                    
            Logger.info(f"已将 {count} 个好友详细信息同步到联系人管理器")
            return {'success': True, 'count': count}
            
        except Exception as e:
            Logger.error(f"同步好友详细信息失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_friend_by_name(self, name: str) -> Optional[Dict]:
        """
        get_friend_by_name 功能说明:
        根据名称获取好友详细信息
        输入: name (str) 好友名称 | 输出: Optional[Dict] 好友详细信息
        """
        if not self.friend_details:
            return None
            
        for friend in self.friend_details:
            if friend.get('NickName') == name:
                return friend
                
        return None