##########contact_manager.py: [联系人管理模块] ##################
# 变更记录: [2024-12-19 14:30] @李祥光 [初始创建]########
# 变更记录: [2024-12-19 19:15] @李祥光 [修复wxauto V2 API兼容性，移除GetAllFriends方法，添加手动添加联系人功能]########
# 输入: 联系人信息和标签操作 | 输出: 联系人数据管理结果###############

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Set
from wxauto import WeChat
from .logger import Logger

###########################文件下的所有函数###########################
"""
ContactManager.__init__：初始化联系人管理器
ContactManager.load_contacts：加载联系人数据
ContactManager.save_contacts：保存联系人数据
ContactManager.sync_from_wechat：从微信同步联系人
ContactManager.add_tag：为联系人添加标签
ContactManager.remove_tag：移除联系人标签
ContactManager.get_contacts_by_tag：根据标签获取联系人
ContactManager.list_contacts：列出所有联系人
ContactManager.get_all_tags：获取所有标签
ContactManager.backup_data：备份联系人数据
"""
###########################文件下的所有函数###########################

#########mermaid格式说明所有函数的调用关系说明开始#########
"""
flowchart TD
    A[ContactManager初始化] --> B[load_contacts]
    B --> C{数据文件存在?}
    C -->|是| D[读取JSON数据]
    C -->|否| E[sync_from_wechat]
    E --> F[save_contacts]
    G[add_tag] --> H[更新联系人标签]
    H --> F
    I[get_contacts_by_tag] --> J[筛选标签联系人]
    K[backup_data] --> L[创建备份文件]
"""
#########mermaid格式说明所有函数的调用关系说明结束#########

class ContactManager:
    """
    ContactManager 功能说明:
    联系人管理类，负责联系人数据的存储、标签管理和微信同步
    输入: 联系人操作请求 | 输出: 联系人数据管理结果
    """
    
    def __init__(self, data_file: str = "data/contacts.json"):
        """
        __init__ 功能说明:
        初始化联系人管理器
        输入: data_file (str) 数据文件路径 | 输出: 无
        """
        self.data_file = Path(data_file)
        self.contacts: List[Dict] = []
        self.load_contacts()
    
    def load_contacts(self) -> None:
        """
        load_contacts 功能说明:
        从文件加载联系人数据，如果文件不存在则尝试从微信同步
        输入: 无 | 输出: 无
        """
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.contacts = data.get('contacts', [])
                Logger.info(f"成功加载 {len(self.contacts)} 个联系人数据")
            else:
                Logger.info("联系人数据文件不存在，尝试从微信同步")
                self.sync_from_wechat()
        except Exception as e:
            Logger.error(f"加载联系人数据失败: {str(e)}")
            self.contacts = []
    
    def save_contacts(self) -> bool:
        """
        save_contacts 功能说明:
        保存联系人数据到文件
        输入: 无 | 输出: bool 保存是否成功
        """
        try:
            # 确保目录存在
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 备份现有数据
            if self.data_file.exists():
                self.backup_data()
            
            data = {
                'contacts': self.contacts,
                'last_updated': datetime.now().isoformat(),
                'version': '1.0.0'
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            Logger.info(f"成功保存 {len(self.contacts)} 个联系人数据")
            return True
        except Exception as e:
            Logger.error(f"保存联系人数据失败: {str(e)}")
            return False
    
    def sync_from_wechat(self) -> bool:
        """
        sync_from_wechat 功能说明:
        从微信客户端同步联系人信息 (wxauto V2版本暂不支持直接获取好友列表)
        输入: 无 | 输出: bool 同步是否成功
        """
        try:
            Logger.info("开始从微信同步联系人...")
            
            ###########################修改开始 2024-12-19 李祥光  #######################
            # wxauto V2版本移除了GetAllFriends方法，暂时无法直接获取好友列表
            # 作为替代方案，提示用户手动添加联系人或使用其他方式
            ###########################修改结束 2024-12-19 李祥光  #######################
            
            Logger.warning("wxauto V2版本暂不支持直接获取好友列表")
            Logger.info("建议使用以下替代方案:")
            Logger.info("1. 手动添加联系人: 使用 add_contact() 方法")
            Logger.info("2. 从聊天记录中提取: 通过聊天窗口获取联系人")
            Logger.info("3. 导入联系人列表: 从外部文件导入")
            
            # 如果没有现有联系人，创建一个示例联系人
            if not self.contacts:
                sample_contact = {
                    'name': '文件传输助手',
                    'type': 'system',
                    'tags': ['系统'],
                    'last_contact': None,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                self.contacts.append(sample_contact)
                self.save_contacts()
                Logger.info("已添加示例联系人: 文件传输助手")
            
            return True
            
        except Exception as e:
            Logger.error(f"从微信同步联系人失败: {str(e)}")
            Logger.info("请使用手动添加联系人的方式: add_contact(name, contact_type='friend')")
            return False
    
    def add_tag(self, contact_name: str, tag: str) -> bool:
        """
        add_tag 功能说明:
        为指定联系人添加标签
        输入: contact_name (str) 联系人姓名, tag (str) 标签名 | 输出: bool 添加是否成功
        """
        try:
            for contact in self.contacts:
                if contact['name'] == contact_name:
                    if 'tags' not in contact:
                        contact['tags'] = []
                    
                    if tag not in contact['tags']:
                        contact['tags'].append(tag)
                        contact['updated_at'] = datetime.now().isoformat()
                        self.save_contacts()
                        Logger.info(f"为联系人 '{contact_name}' 添加标签 '{tag}'")
                        return True
                    else:
                        Logger.warning(f"联系人 '{contact_name}' 已有标签 '{tag}'")
                        return True
            
            Logger.warning(f"未找到联系人 '{contact_name}'")
            return False
            
        except Exception as e:
            Logger.error(f"添加标签失败: {str(e)}")
            return False
    
    def remove_tag(self, contact_name: str, tag: str) -> bool:
        """
        remove_tag 功能说明:
        移除指定联系人的标签
        输入: contact_name (str) 联系人姓名, tag (str) 标签名 | 输出: bool 移除是否成功
        """
        try:
            for contact in self.contacts:
                if contact['name'] == contact_name:
                    if 'tags' in contact and tag in contact['tags']:
                        contact['tags'].remove(tag)
                        contact['updated_at'] = datetime.now().isoformat()
                        self.save_contacts()
                        Logger.info(f"为联系人 '{contact_name}' 移除标签 '{tag}'")
                        return True
                    else:
                        Logger.warning(f"联系人 '{contact_name}' 没有标签 '{tag}'")
                        return False
            
            Logger.warning(f"未找到联系人 '{contact_name}'")
            return False
            
        except Exception as e:
            Logger.error(f"移除标签失败: {str(e)}")
            return False
    
    def get_contacts_by_tag(self, tag: str) -> List[Dict]:
        """
        get_contacts_by_tag 功能说明:
        根据标签获取联系人列表
        输入: tag (str) 标签名 | 输出: List[Dict] 联系人列表
        """
        try:
            result = []
            for contact in self.contacts:
                if 'tags' in contact and tag in contact['tags']:
                    result.append(contact)
            
            Logger.info(f"标签 '{tag}' 匹配到 {len(result)} 个联系人")
            return result
            
        except Exception as e:
            Logger.error(f"根据标签获取联系人失败: {str(e)}")
            return []
    
    def list_contacts(self) -> List[Dict]:
        """
        list_contacts 功能说明:
        获取所有联系人列表
        输入: 无 | 输出: List[Dict] 联系人列表
        """
        return self.contacts.copy()
    
    def get_all_tags(self) -> Set[str]:
        """
        get_all_tags 功能说明:
        获取所有使用过的标签
        输入: 无 | 输出: Set[str] 标签集合
        """
        tags = set()
        for contact in self.contacts:
            if 'tags' in contact:
                tags.update(contact['tags'])
        return tags
    
    def backup_data(self) -> bool:
        """
        backup_data 功能说明:
        备份当前联系人数据
        输入: 无 | 输出: bool 备份是否成功
        """
        try:
            if not self.data_file.exists():
                return True
            
            backup_dir = self.data_file.parent / 'backups'
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = backup_dir / f"contacts_backup_{timestamp}.json"
            
            # 复制当前文件到备份目录
            import shutil
            shutil.copy2(self.data_file, backup_file)
            
            Logger.info(f"联系人数据已备份到: {backup_file}")
            return True
            
        except Exception as e:
            Logger.error(f"备份联系人数据失败: {str(e)}")
            return False
    
    def get_contact_count(self) -> int:
        """
        get_contact_count 功能说明:
        获取联系人总数
        输入: 无 | 输出: int 联系人总数
        """
        return len(self.contacts)
    
    def add_contact(self, name: str, contact_type: str = 'friend', tags: List[str] = None) -> bool:
        """
        add_contact 功能说明:
        手动添加联系人
        输入: name(联系人姓名), contact_type(联系人类型), tags(标签列表) | 输出: bool 添加是否成功
        """
        try:
            # 检查联系人是否已存在
            for contact in self.contacts:
                if contact['name'] == name:
                    Logger.warning(f"联系人 {name} 已存在")
                    return False
            
            # 创建新联系人
            new_contact = {
                'name': name,
                'type': contact_type,
                'tags': tags or [],
                'last_contact': None,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            self.contacts.append(new_contact)
            self.save_contacts()
            
            Logger.info(f"成功添加联系人: {name}")
            return True
            
        except Exception as e:
            Logger.error(f"添加联系人失败: {str(e)}")
            return False
    
    def search_contacts(self, keyword: str) -> List[Dict]:
        """
        search_contacts 功能说明:
        根据关键词搜索联系人
        输入: keyword (str) 搜索关键词 | 输出: List[Dict] 匹配的联系人列表
        """
        try:
            result = []
            keyword_lower = keyword.lower()
            
            for contact in self.contacts:
                # 搜索姓名
                if keyword_lower in contact['name'].lower():
                    result.append(contact)
                    continue
                
                # 搜索标签
                if 'tags' in contact:
                    for tag in contact['tags']:
                        if keyword_lower in tag.lower():
                            result.append(contact)
                            break
            
            Logger.info(f"关键词 '{keyword}' 搜索到 {len(result)} 个联系人")
            return result
            
        except Exception as e:
            Logger.error(f"搜索联系人失败: {str(e)}")
            return []