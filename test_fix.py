##########test_fix.py: [API修复验证测试] ##################
# 变更记录: [2024-12-19 19:20] @李祥光 [创建API修复验证测试]########
# 输入: 无 | 输出: 测试结果###############

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.contact_manager import ContactManager
from utils.logger import Logger

def test_contact_manager_fix():
    """
    test_contact_manager_fix 功能说明:
    测试ContactManager修复后的功能
    输入: 无 | 输出: 测试结果
    """
    print("🧪 开始测试ContactManager修复后的功能...")
    
    try:
        # 测试ContactManager初始化
        manager = ContactManager()
        print("✅ ContactManager初始化成功")
        
        # 测试手动添加联系人
        result = manager.add_contact("测试联系人", "friend", ["测试标签"])
        if result:
            print("✅ 手动添加联系人功能正常")
        else:
            print("❌ 手动添加联系人功能异常")
        
        # 测试同步功能（应该不会报错，但会提示替代方案）
        print("\n🔄 测试同步功能...")
        sync_result = manager.sync_from_wechat()
        if sync_result:
            print("✅ 同步功能运行正常（提供了替代方案）")
        else:
            print("❌ 同步功能运行异常")
        
        # 测试联系人列表
        contacts = manager.list_contacts()
        print(f"📋 当前联系人数量: {len(contacts)}")
        
        # 显示联系人信息
        for contact in contacts:
            print(f"👤 {contact['name']} | 类型: {contact['type']} | 标签: {contact.get('tags', [])}")
        
        print("\n🎉 所有测试完成！")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        Logger.error(f"测试异常: {str(e)}")

if __name__ == "__main__":
    test_contact_manager_fix()