# node_graph.py

# 这里的列表定义了思维导图的结构
# 格式: (ID, 显示文本, x坐标, y坐标, 颜色, 父节点ID)

NODES = [
    # === 核心根节点 ===
    ("root", "电气控制\n与plc应用", 500, 450, "#00ced1", None),

    # ==============================
    # === 右侧：电气控制模块 (蓝色系) ===
    # ==============================
    ("elec_mod", "电气控制\n模块", 700, 400, "#4682b4", "root"),
    
    ("elec_circuit", "典型控\n制线路", 750, 250, "#4169e1", "elec_mod"),
    
    ("control_draw", "控制线\n路绘制", 850, 380, "#4169e1", "elec_mod"),
        ("elec_principle", "电气原\n理图", 920, 280, "#4169e1", "control_draw"),
        ("elec_wiring", "电气接\n线图", 950, 350, "#4169e1", "control_draw"),
        ("elec_layout", "电器\n布置", 950, 450, "#4169e1", "control_draw"),
    
    # 注意：下面这两个 ID (low_volt, mag_mech) 对应了 contents 文件夹里的脚本
    ("low_volt", "认识低\n压电器", 780, 550, "#4169e1", "elec_mod"),
        ("common_low", "常见低\n压电路", 700, 680, "#4169e1", "low_volt"),
        ("arc_ext", "灭弧\n装置", 900, 550, "#4169e1", "low_volt"),
        ("contact_sys", "触头\n系统", 900, 650, "#4169e1", "low_volt"),
        ("mag_mech", "电磁\n机构", 830, 720, "#4169e1", "low_volt"),

    # ==============================
    # === 左侧：PLC模块 (红色系) ===
    # ==============================
    ("plc_mod", "Plc 模\n块", 350, 400, "#dc143c", "root"),
    
    ("plc_basic", "Plc 基\n础知识", 280, 280, "#dc143c", "plc_mod"),
        ("plc_gen", "Plc 的产\n生和特点", 280, 150, "#dc143c", "plc_basic"),
        ("plc_struct", "Plc 的结\n构和原理", 400, 180, "#dc143c", "plc_basic"),
        ("plc_def", "Plc 的定\n义与分类", 150, 200, "#dc143c", "plc_basic"),
        
        # --- 新增节点：PLC软继电器 ---
        ("plc_soft_relay", "PLC软\n继电器", 420, 260, "#dc143c", "plc_basic"), 

    ("plc_prog", "Plc 的\n编程", 280, 500, "#dc143c", "plc_mod"),
        ("plc_lang", "Plc 的编\n程语言", 250, 650, "#dc143c", "plc_prog"),
            ("seq_func", "顺序功\n能图", 150, 750, "#dc143c", "plc_lang"),
            ("func_block", "功能\n块图", 250, 800, "#dc143c", "plc_lang"),
            ("ladder", "梯形图", 350, 800, "#dc143c", "plc_lang"),
            ("instr_list", "指令语\n句表", 450, 750, "#dc143c", "plc_lang"),
            
    ("plc_instr", "Plc 基\n本指令", 180, 450, "#dc143c", "plc_mod"),
        ("basic_logic", "基本逻\n辑指令", 80, 450, "#dc143c", "plc_instr"),
        ("step_instr", "步进\n指令", 80, 550, "#dc143c", "plc_instr"),
        ("func_instr", "功能\n指令", 80, 350, "#dc143c", "plc_instr"),

    # === 中间上方：实训项目 (橙色系) ===
    ("training", "实训\n项目", 500, 300, "#ff8c00", "root"),
]