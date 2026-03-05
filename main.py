import sys
import os
import math
import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
import webbrowser
from PIL import Image, ImageTk

# --- 开启 Windows 高分屏 (DPI) 适配，让字体和界面彻底清晰 ---
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

import node_graph
from contents import get_node_content


class MindMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("电气控制与PLC应用")
        self.root.geometry("1100x900") # 稍微加宽一点，适应高清屏

        # 设置现代化主题
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.nodes = node_graph.NODES
        self.draw_map()

    def draw_map(self):
        node_dict = {n[0]: (n[2], n[3]) for n in self.nodes}
        r = 40

        for node in self.nodes:
            _, _, x, y, _, parent_id = node
            if parent_id and parent_id in node_dict:
                px, py = node_dict[parent_id]
                dx, dy = x - px, y - py
                dist = math.hypot(dx, dy)
                if dist == 0:
                    continue

                cos_a, sin_a = dx / dist, dy / dist
                start_x, start_y = px + r * cos_a, py + r * sin_a
                end_x, end_y = x - r * cos_a, y - r * sin_a

                self.canvas.create_line(
                    start_x, start_y, end_x, end_y,
                    fill="#aaaaaa", width=2,
                    arrow=tk.LAST, arrowshape=(10, 12, 4)
                )

        for node in self.nodes:
            node_id, text, x, y, color, _ = node
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                outline=color, width=2, fill="white", tags=node_id
            )
            self.canvas.create_text(x, y, text=text, justify="center", font=("Microsoft YaHei", 9), tags=node_id)

            self.canvas.tag_bind(
                node_id, "<Button-1>",
                lambda e, nid=node_id, t=text, c=color: self.open_popup(nid, t, c)
            )
            self.canvas.tag_bind(node_id, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(node_id, "<Leave>", lambda e: self.canvas.config(cursor=""))

    def open_popup(self, node_id, text, color):
        top = Toplevel(self.root)
        top.title(text.replace("\n", ""))
        top.geometry("1200x850")

        header = tk.Frame(top, bg=color, height=50)
        header.pack(fill="x")
        tk.Label(header, text=text.replace("\n", ""), bg=color, fg="white", font=("Microsoft YaHei", 14, "bold")).pack(pady=10)

        data = get_node_content(node_id)

        if data:
            self.render_content(top, data)
        else:
            tk.Label(top, text=f"暂无【{text.replace(chr(10), '')}】的详细内容。", font=("Microsoft YaHei", 12), fg="gray").pack(pady=50)

    def render_content(self, parent, data):
        # === 1. 创建滚动容器 ===
        main_frame = tk.Frame(parent)
        main_frame.pack(fill="both", expand=True)

        cv = tk.Canvas(main_frame)
        sb = tk.Scrollbar(main_frame, orient="vertical", command=cv.yview)

        frm = tk.Frame(cv)

        def update_scrollregion(event=None):
            cv.configure(scrollregion=cv.bbox("all"))

        frm.bind("<Configure>", update_scrollregion)
        frm_id = cv.create_window((0, 0), window=frm, anchor="nw")

        def _on_canvas_configure(event):
            cv.itemconfig(frm_id, width=event.width)
            update_scrollregion()

        cv.bind("<Configure>", _on_canvas_configure)
        cv.configure(yscrollcommand=sb.set)

        cv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def _on_mousewheel(event):
            cv.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind(event):
            cv.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind(event):
            cv.unbind_all("<MouseWheel>")

        cv.bind('<Enter>', _bind)
        cv.bind('<Leave>', _unbind)

        # === 2. 辅助函数 ===
        
        # --- 优化版：最稳妥的资源路径处理 ---
        def resource_path(relative_path):
            """ 获取绝对路径，无论开发环境、打包环境还是通过不同终端路径执行都能准确定位 """
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS # PyInstaller 打包后的路径
            else:
                # 获取当前脚本所在目录，最稳健的做法
                base_path = os.path.dirname(os.path.abspath(__file__)) 
            return os.path.join(base_path, relative_path)

        def create_img_widget(container, path, caption, max_w=800):
            full_path = resource_path(path)

            if not os.path.exists(full_path):
                tk.Label(container, text=f"[图片缺失] {full_path}", fg="red").pack()
                return
            try:
                pil_img = Image.open(full_path)
                if pil_img.width > max_w:
                    ratio = max_w / float(pil_img.width)
                    h_size = int((float(pil_img.height) * float(ratio)))
                    pil_img = pil_img.resize((max_w, h_size), Image.Resampling.LANCZOS)

                tk_img = ImageTk.PhotoImage(pil_img)
                lbl = tk.Label(container, image=tk_img, bg="white", bd=1, relief="solid")
                lbl.image = tk_img
                lbl.pack(pady=5)
                if caption:
                    tk.Label(container, text=caption, fg="gray", font=("Microsoft YaHei", 9)).pack(pady=(0, 10))
            except Exception as e:
                tk.Label(container, text=f"图片加载错误: {e}", fg="red").pack()

        def create_fluid_label(container, text_content, font_size=11):
            lbl = tk.Label(
                container,
                text=text_content,
                justify="left",
                anchor="w",
                font=("Microsoft YaHei", font_size),
                bg=parent.cget("bg")
            )
            lbl.pack(padx=30, pady=10, fill="x")
            lbl.bind("<Configure>", lambda e: e.widget.config(wraplength=e.width))
            return lbl

        # === 核心：Grid 表格渲染 ===
        def create_table_widget(container, title, columns, widths, table_data, header_rows=None):
            if title:
                tk.Label(container, text=title, font=("Microsoft YaHei", 11, "bold")).pack(pady=(20, 5))

            table_frame = tk.Frame(container, bd=1, relief="solid", bg="#aaaaaa")
            table_frame.pack(fill="x", padx=30, pady=5)

            candidates = []
            if columns: candidates.append(len(columns))
            if header_rows: candidates.extend([len(r) for r in header_rows if r is not None])
            if table_data: candidates.extend([len(r) for r in table_data if r is not None])
            ncols = max(candidates) if candidates else 0

            col_widths = []
            for i in range(ncols):
                w_px = widths[i] if widths and i < len(widths) else 110
                col_widths.append(w_px)
                table_frame.grid_columnconfigure(i, weight=1, minsize=w_px)

            def cell_text_at(grid_rows, r, c):
                if r < 0 or r >= len(grid_rows): return ""
                row = grid_rows[r]
                return row[c] if (row is not None and c < len(row)) else ""

            def compute_rowspan_map(grid_rows):
                rowspan_map = {}
                R = len(grid_rows)
                for r in range(R):
                    for c in range(ncols):
                        if cell_text_at(grid_rows, r, c) == "^^^": continue
                        span, rr = 1, r + 1
                        while rr < R and cell_text_at(grid_rows, rr, c) == "^^^":
                            span += 1; rr += 1
                        rowspan_map[(r, c)] = span
                return rowspan_map

            def render_grid(start_row, grid_rows, is_header=False, zebra_base=0):
                rowspan_map = compute_rowspan_map(grid_rows)
                row0 = start_row

                for r, row_data in enumerate(grid_rows):
                    real_r = row0 + r
                    bg_color = "#d9d9d9" if is_header else ("#ffffff" if (zebra_base + r) % 2 != 0 else "#f0f0f0")
                    c = 0
                    while c < ncols:
                        cell = row_data[c] if (row_data and c < len(row_data)) else ""
                        if cell == "^^^":
                            c += 1; continue

                        colspan = 1
                        while (c + colspan < len(row_data)) and row_data[c + colspan] == "<<<":
                            colspan += 1

                        rowspan = rowspan_map.get((r, c), 1)
                        approx_w = sum(col_widths[c:c + colspan]) - 20
                        
                        lbl = tk.Label(
                            table_frame, text=cell,
                            font=('Microsoft YaHei', 10, 'bold' if is_header else 'normal'),
                            bg=bg_color, relief="solid", bd=1,
                            pady=6 if is_header else 5, padx=6,
                            wraplength=max(120, approx_w),
                            justify="center" if is_header else "left",
                            anchor="center" if is_header else "w"
                        )
                        lbl.grid(row=real_r, column=c, columnspan=colspan, rowspan=rowspan, sticky="nsew")
                        c += colspan
                return start_row + len(grid_rows)

            current_row = 0
            if header_rows:
                current_row = render_grid(current_row, [list(r) for r in header_rows], is_header=True)
            elif columns:
                current_row = render_grid(current_row, [list(columns)], is_header=True)

            if table_data:
                render_grid(current_row, [list(r) for r in table_data], is_header=False, zebra_base=0)

        # === 3. 渲染 Layout 内容 ===
        if "layout" in data:
            for item in data["layout"]:
                if item["type"] == "text":
                    create_fluid_label(frm, item["content"])

                elif item["type"] == "image_row":
                    row_frame = tk.Frame(frm)
                    row_frame.pack(pady=10, fill="x", padx=20)
                    images = item["images"]
                    w_limit = 900 // len(images) if images else 800
                    for img_info in images:
                        box = tk.Frame(row_frame)
                        box.pack(side="left", expand=True, fill="x", padx=5)
                        create_img_widget(box, img_info["path"], img_info.get("caption"), max_w=w_limit)

                elif item["type"] == "split_row":
                    split_frame = tk.Frame(frm)
                    split_frame.pack(pady=10, fill="x", padx=20)
                    left_frame = tk.Frame(split_frame)
                    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
                    right_frame = tk.Frame(split_frame)
                    right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

                    if item["left"]["type"] == "text":
                        lbl = tk.Label(left_frame, text=item["left"]["content"], justify="left", anchor="nw", font=("Microsoft YaHei", 11))
                        lbl.pack(fill="x", anchor="n")
                        lbl.bind("<Configure>", lambda e: e.widget.config(wraplength=e.width))
                    if item["right"]["type"] == "image":
                        create_img_widget(right_frame, item["right"]["path"], item["right"].get("caption"), max_w=400)

                elif item["type"] == "table":
                    create_table_widget(
                        frm, item.get("title"), item.get("columns"), item.get("widths"),
                        item.get("data"), header_rows=item.get("header_rows")
                    )

        else:
            if "intro" in data: create_fluid_label(frm, data["intro"])
            if "image_paths" in data:
                for p in data["image_paths"]: create_img_widget(frm, p, f"图示: {os.path.basename(p)}")

        # === 4. 渲染底部全局表格 ===
        if data.get("has_table"):
            create_table_widget(
                frm, data.get("table_title"), data.get("table_columns"), data.get("table_widths"),
                data.get("table_data"), header_rows=data.get("table_header_rows")
            )

        # === 5. 后续内容 ===
        if "layout_append" in data:
            for item in data["layout_append"]:
                if item["type"] == "text": create_fluid_label(frm, item["content"])

        # === 6. 视频按钮 ===
        videos = data.get("video_list", [])
        if not videos and data.get("video_url"):
            videos = [{"title": data.get("video_button_text", "▶ 点击观看 Bilibili 视频讲解"), "url": data["video_url"]}]

        if videos:
            btn_container = tk.Frame(frm, pady=20)
            btn_container.pack(fill="x", padx=30)
            tk.Label(btn_container, text="--- 视频教程资源 ---", fg="#888", font=("Microsoft YaHei", 10)).pack(pady=(0, 10))
            for v in videos:
                tk.Button(
                    btn_container, text=f"▶ {v['title']}", bg="#FB7299", fg="white", font=("Microsoft YaHei", 11),
                    cursor="hand2", command=lambda u=v['url']: webbrowser.open(u)
                ).pack(pady=4, fill="x", ipadx=10)

        tk.Frame(frm, height=50).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = MindMapApp(root)
    root.mainloop()