# PLC Teaching App
电气控制与 PLC 应用交互教学系统

一个基于 **Python + Tkinter** 开发的交互式 PLC 教学软件。  
系统通过 **思维导图方式展示 PLC 知识结构**，支持图文内容、教学视频以及模块化扩展。

---

# 项目特点

- 可视化 **PLC知识思维导图**
- 图文 + 视频教学
- Python 跨平台开发
- 模块化内容扩展
- 一键打包 Windows EXE

---

# 技术栈

语言

- Python 3.x

第三方库

- Pillow
- PyInstaller

Python 标准库

- tkinter
- ttk
- os
- sys
- math
- webbrowser

安装依赖：

```bash
pip install Pillow pyinstaller
项目结构
PLC_Teaching_App/
│
├── main.py              # 主程序入口
├── node_graph.py        # 思维导图节点结构
│
├── contents/            # 教学内容模块
│   ├── __init__.py
│   ├── plc_soft_relay.py
│   └── training.py
│
└── images/              # 教学图片资源
    ├── 18.png
    └── 23.png
添加新的教学章节

系统采用 数据驱动设计，新增章节无需修改主程序。

1 准备图片

将图片放入

images/

例如

images/timer_01.png
2 创建内容文件

在 contents/ 中创建

timer.py

示例

data = {
    "title": "PLC 定时器应用",
    "layout": [
        {
            "type": "text",
            "content": "这里是定时器的工作原理说明..."
        },
        {
            "type": "image_row",
            "images": [
                {
                    "path": "images/timer_01.png",
                    "caption": "定时器原理图"
                }
            ]
        }
    ]
}
3 注册内容

修改

contents/__init__.py
from . import timer

def get_node_content(node_id):
    if node_id == "node_timer":
        return timer.data
4 添加思维导图节点

修改

node_graph.py
("node_timer", "定时器应用", 800, 450, "#3399ff", "root")

格式

(node_id, 显示文本, X坐标, Y坐标, 节点颜色, 父节点ID)
打包为 EXE

进入项目目录

main.py 所在目录

执行

pyinstaller --noconfirm --onedir --windowed \
--add-data "images;images" \
--add-data "contents;contents" \
--name "PLC交互教学系统" main.py
发布程序

打包完成后

dist/
└── PLC交互教学系统/
    ├── PLC交互教学系统.exe
    ├── images/
    └── contents/

用户只需运行

PLC交互教学系统.exe
