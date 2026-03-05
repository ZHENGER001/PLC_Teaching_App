# PLC Teaching App

电气控制与 PLC 应用交互教学系统。

这是一个基于 **Python + Tkinter** 开发的交互式教学软件，通过思维导图形式展示 PLC 知识点，并提供图文说明和教学视频链接。

---

## 技术栈

- Python 3.x  
- Tkinter (GUI)  
- Pillow (图像处理)  
- PyInstaller (程序打包)

安装依赖：

```bash
pip install Pillow pyinstaller
项目结构
PLC_Teaching_App/
│
├── main.py              # 主程序入口
├── node_graph.py        # 思维导图结构
│
├── contents/            # 教学内容
│   ├── __init__.py
│   ├── plc_soft_relay.py
│   └── training.py
│
└── images/              # 图片资源
运行程序

进入项目目录后运行：

python main.py
打包为 EXE

使用 PyInstaller 打包：

pyinstaller --noconfirm --onedir --windowed \
--add-data "images;images" \
--add-data "contents;contents" \
--name "PLC教学系统" main.py

生成的程序位于：

dist/PLC教学系统/
