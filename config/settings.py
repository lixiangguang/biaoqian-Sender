##########settings.py: [配置管理模块] ##################
# 变更记录: [2024-12-19 14:30] @李祥光 [初始创建]########
# 输入: 无 | 输出: 配置对象###############

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

###########################文件下的所有函数###########################
"""
Config.load：加载配置文件
Config.save：保存配置文件
Config.get：获取配置项
Config.set：设置配置项
"""
###########################文件下的所有函数###########################

#########mermaid格式说明所有函数的调用关系说明开始#########
"""
flowchart TD
    A[Config初始化] --> B[load方法]
    B --> C{配置文件存在?}
    C -->|是| D[读取JSON配置]
    C -->|否| E[创建默认配置]
    E --> F[save方法]
    G[get方法] --> H{配置项存在?}
    H -->|是| I[返回配置值]
    H -->|否| J[返回默认值]
    K[set方法] --> L[更新配置项]
    L --> M[save方法]
"""
#########mermaid格式说明所有函数的调用关系说明结束#########

class Config:
    """
    Config 功能说明:
    配置管理类，负责加载、保存和管理应用配置
    输入: 无 | 输出: 配置对象
    """
    
    _instance = None
    _config_data = {}
    _config_file = "config/app_config.json"
    
    def __new__(cls):
        """
        __new__ 功能说明:
        单例模式实现，确保全局只有一个配置实例
        输入: 无 | 输出: Config实例
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load()
        return cls._instance
    
    def load(self, config_file: Optional[str] = None) -> Dict:
        """
        load 功能说明:
        加载配置文件，如果文件不存在则创建默认配置
        输入: config_file (str, 可选) 配置文件路径 | 输出: Dict 配置数据
        """
        if config_file:
            self._config_file = config_file
            
        config_path = Path(self._config_file)
        
        # 如果配置文件存在，则加载
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self._config_data = json.load(f)
                print(f"已加载配置文件: {config_path}")
            except Exception as e:
                print(f"加载配置文件失败: {str(e)}，将使用默认配置")
                self._create_default_config()
        else:
            print(f"配置文件不存在: {config_path}，将创建默认配置")
            self._create_default_config()
            
        return self._config_data
    
    def _create_default_config(self) -> None:
        """
        _create_default_config 功能说明:
        创建默认配置
        输入: 无 | 输出: 无
        """
        self._config_data = {
            "app": {
                "name": "微信标签联系人消息发送器",
                "version": "1.0.0"
            },
            "message": {
                "send_interval": 2,  # 发送间隔（秒）
                "retry_count": 3,    # 失败重试次数
                "confirm_send": True  # 发送前确认
            },
            "contacts": {
                "data_file": "data/contacts.json",
                "backup_dir": "data/backups",
                "auto_backup": True
            },
            "friend_details": {
                "data_file": "data/friend_details.json"
            },
            "logging": {
                "level": "INFO",
                "file": "logs/app.log",
                "max_size": 10485760,  # 10MB
                "backup_count": 5
            }
        }
        
        # 保存默认配置
        self.save()
    
    def save(self) -> bool:
        """
        save 功能说明:
        保存配置到文件
        输入: 无 | 输出: bool 保存是否成功
        """
        config_path = Path(self._config_file)
        
        # 确保目录存在
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config_data, f, ensure_ascii=False, indent=2)
            print(f"配置已保存到: {config_path}")
            return True
        except Exception as e:
            print(f"保存配置失败: {str(e)}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        get 功能说明:
        获取配置项，支持使用点号分隔的路径
        输入: key (str) 配置键, default (Any) 默认值 | 输出: Any 配置值
        """
        # 支持使用点号分隔的路径，如 "app.name"
        parts = key.split('.')
        config = self._config_data
        
        for part in parts:
            if part in config:
                config = config[part]
            else:
                return default
                
        return config
    
    def set(self, key: str, value: Any) -> bool:
        """
        set 功能说明:
        设置配置项，支持使用点号分隔的路径
        输入: key (str) 配置键, value (Any) 配置值 | 输出: bool 设置是否成功
        """
        # 支持使用点号分隔的路径，如 "app.name"
        parts = key.split('.')
        config = self._config_data
        
        # 遍历路径，直到最后一个部分
        for i, part in enumerate(parts[:-1]):
            if part not in config:
                config[part] = {}
            config = config[part]
        
        # 设置最后一个部分的值
        config[parts[-1]] = value
        
        # 保存配置
        return self.save()