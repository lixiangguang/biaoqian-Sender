##########main.py: [微信标签联系人消息发送器主程序] ##################
# 变更记录: [2024-12-19 14:30] @李祥光 [初始创建]########
# 变更记录: [2024-12-19 19:15] @李祥光 [修复wxauto V2 API兼容性，添加手动添加联系人功能]########
# 变更记录: [2025-06-30 10:30] @李祥光 [添加获取好友详细信息功能]########
# 输入: 命令行参数或交互式输入 | 输出: 发送结果状态###############

import sys
import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from wxautox import WeChat
from config.settings import Config
from utils.logger import Logger
from utils.contact_manager import ContactManager
from utils.message_sender import MessageSender
from utils.friend_details import FriendDetailsManager

###########################文件下的所有函数###########################
"""
main：程序主入口函数
show_menu：显示交互菜单
handle_send_by_tag：处理按标签发送消息
handle_list_contacts：处理列出联系人
handle_manage_tags：处理标签管理
handle_add_contact：处理手动添加联系人
handle_sync_contacts：处理从微信同步联系人
handle_get_friend_details：处理获取好友详细信息
send_to_file_helper：文件助手发送功能
"""
###########################文件下的所有函数###########################

#########mermaid格式说明所有函数的调用关系说明开始#########
"""
https://www.processon.com/
flowchart TD
    A[程序启动] --> B[main函数]
    B --> C{检查命令行参数}
    C -->|有参数 'helper'| D[send_to_file_helper函数]
    C -->|无参数| E[显示交互菜单]
    E --> F{用户选择}
    F -->|1| G[handle_send_by_tag]
    F -->|2| H[handle_list_contacts]
    F -->|3| I[handle_manage_tags]
    F -->|4| N[handle_add_contact]
    F -->|5| O[handle_sync_contacts]
    F -->|6| P[handle_get_friend_details]
    F -->|0| J[退出程序]
    G --> K[MessageSender.send_by_tag]
    H --> L[ContactManager.list_contacts]
    I --> M[ContactManager.manage_tags]
    P --> Q[FriendDetailsManager.get_friend_details]
"""
#########mermaid格式说明所有函数的调用关系说明结束#########

def show_menu():
    """
    show_menu 功能说明:
    显示程序主菜单选项
    输入: 无 | 输出: 无，直接打印菜单
    """
    print("\n=== 微信标签联系人消息发送器 ===")
    print("1. 按标签发送消息")
    print("2. 查看联系人列表")
    print("3. 管理联系人标签")
    print("4. 手动添加联系人")
    print("5. 从微信同步联系人")
    print("6. 获取好友详细信息")
    print("0. 退出程序")
    print("=" * 35)

def handle_send_by_tag():
    """
    handle_send_by_tag 功能说明:
    处理按标签发送消息的业务逻辑
    输入: 用户交互输入 | 输出: 发送结果状态
    """
    try:
        tag = input("请输入要发送的标签名: ").strip()
        if not tag:
            print("标签名不能为空！")
            return
        
        message = input("请输入要发送的消息内容: ").strip()
        if not message:
            print("消息内容不能为空！")
            return
        
        sender = MessageSender()
        result = sender.send_by_tag(tag, message)
        
        if result['success']:
            print(f"✅ 消息发送成功！共发送给 {result['count']} 个联系人")
            Logger.info(f"按标签'{tag}'发送消息成功，发送数量: {result['count']}")
        else:
            print(f"❌ 消息发送失败: {result['error']}")
            Logger.error(f"按标签'{tag}'发送消息失败: {result['error']}")
            
    except Exception as e:
        print(f"❌ 发送过程中出现错误: {str(e)}")
