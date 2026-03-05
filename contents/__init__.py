# contents/__init__.py

from . import common_low
from . import mag_mech
from . import contact_sys
from . import arc_ext
from . import control_draw 
from . import elec_principle # <--- 确保导入了这个文件
from . import elec_wiring
from . import elec_layout
from . import elec_circuit
from . import plc_gen
from . import plc_struct
from . import plc_def
from . import plc_soft_relay
from . import basic_logic
from . import func_instr
from . import step_instr

from . import ladder
from . import func_block

from . import  seq_func
from . import instr_list
from . import  training

content_map = {
    # 1. 之前做好的模块
    "common_low": common_low.data,
    "mag_mech": mag_mech.data,
    "contact_sys": contact_sys.data,
    "arc_ext": arc_ext.data,
    
    # 2. 关键点：为了防止 ID 对不上，我们将两个可能的名字都指向同一个数据
    "control_draw": control_draw.data,     # 新名字
    "control_circuit": control_draw.data,  # 旧名字 (以防 node_graph.py 里用的是这个)
    "elec_principle": elec_principle.data,
    "elec_wiring": elec_wiring.data,
    "elec_layout": elec_layout.data,
    "elec_circuit": elec_circuit.data,
    "plc_gen": plc_gen.data,
    "plc_def": plc_def.data,
    "plc_struct": plc_struct.data,
    "plc_soft_relay": plc_soft_relay.data,
    "basic_logic": basic_logic.data,
    "func_instr":func_instr.data,
    "step_instr":step_instr.data,
    "ladder":ladder.data,
    "func_block":func_block.data,
    "seq_func": seq_func.data,
    "instr_list":instr_list.data,
    "training": training.data,


}

def get_node_content(node_id):
    return content_map.get(node_id)