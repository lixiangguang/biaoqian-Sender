@echo off
REM ##########run.bat: Windows启动脚本 ##################
REM # 变更记录: [2024-12-19 14:30] @李祥光 [初始创建]########
REM # 输入: 无 | 输出: 启动程序###############

echo ========================================
echo 微信标签联系人消息发送器
echo 作者: 李祥光
echo 版本: 1.0.0
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查是否在正确目录
if not exist "main.py" (
    echo ❌ 错误: 未找到main.py文件，请确保在项目根目录运行此脚本
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 🔍 检查依赖包...
python -c "import wxauto" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  警告: 未安装wxauto包，正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 错误: 依赖安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
)

REM 启动程序
echo 🚀 启动程序...
echo.
python main.py

REM 程序结束后暂停
echo.
echo 程序已退出
pause