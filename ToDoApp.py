import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QLabel, QGridLayout, QTextEdit, QAbstractItemView, QMessageBox
from PyQt5.QtCore import Qt, QSize,QModelIndex,pyqtSignal
from PyQt5.QtGui import QColor,QIcon
import datetime
import json

from flask.config import T


class ImportWidget(QWidget):
    # 自定义信号
    import_finished = pyqtSignal(dict)
    def __init__(self,parent):
        super().__init__(parent)
        self.setFixedSize(500,500)
        self.setWindowFlags(Qt.Window)  # 关键：强制为独立窗口
        self.input_field = QTextEdit()
        self.main_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()
        self.confirm_button = QPushButton("导入")
        self.cancel_button = QPushButton("取消")
        self.btn_layout.addWidget(self.confirm_button)
        self.btn_layout.addWidget(self.cancel_button)

        self.confirm_button.clicked.connect(self.read_json_data)
        self.cancel_button.clicked.connect(self.cancel_import)

        self.main_layout.addLayout(self.btn_layout)
        self.main_layout.addWidget(self.input_field)
        self.setLayout(self.main_layout)

    def read_json_data(self):
        text = self.input_field.toPlainText()  # 获取输入框的文本
        # print(f"原始文本内容: {text}")  # 调试：打印原始文本内容
        try:
            # 将输入的文本解析为 JSON 数据
            json_data = json.loads(text.strip())  # 使用 strip() 去除首尾空白字符
            # print(f"解析后的 JSON 数据: {json_data}")   
            self.import_finished.emit(json_data)
        except json.JSONDecodeError as e:
            # 如果 JSON 格式不正确，打印错误信息
            print(f"JSON 解析失败: {e}")
            QMessageBox.warning(self, "错误", "JSON 格式不正确")
            self.input_field.clear()

    def cancel_import(self):
        QMessageBox.information(self, "提示", "已取消导入")
        self.close()
        

class ToDoItem:
    def __init__(self, title, description,deadline_time=None,is_completed=False):
        self.title = title
        self.description = description
        self.deadline_time = deadline_time
        self.is_completed = is_completed



class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口属性
        self.setWindowTitle("Daily To Do List")
        self.setGeometry(100, 100, 400, 400)

        # 排序方式
        self.sort_value = None

        # 初始化主布局
        self.main_layout = QVBoxLayout()

        # 创建输入和添加按钮
        self.input_layout = QGridLayout()

        # 标题输入
        self.title_label = QLabel("标题:")
        self.title_input = QLineEdit()
        self.input_layout.addWidget(self.title_label, 0, 0)
        self.input_layout.addWidget(self.title_input, 0, 1)

        # 描述输入
        self.description_label = QLabel("描述:")
        self.description_input = QLineEdit()
        self.input_layout.addWidget(self.description_label, 1, 0)
        self.input_layout.addWidget(self.description_input, 1, 1)

        # ddl输入
        self.deadline_label = QLabel("DDL:")
        self.deadline_input = QLineEdit()
        self.input_layout.addWidget(self.deadline_label, 2, 0)
        self.input_layout.addWidget(self.deadline_input, 2, 1)

        # 水平按钮布局
        self.add_layout = QHBoxLayout()
        self.add_layout.setSpacing(20)

        # 导入
        self.batch_import_button = QPushButton('批量导入')
        self.batch_import_button.clicked.connect(self.showAndWait)
        self.add_layout.addWidget(self.batch_import_button)

        # 导出到剪切板
        self.export_button = QPushButton("导出")
        self.export_button.clicked.connect(self.export_to_clipboard)
        self.add_layout.addWidget(self.export_button)

        self.add_button = QPushButton("添加")
        self.add_button.clicked.connect(lambda : self.add_item())
        self.add_layout.addWidget(self.add_button)

        # 任务列表带标题
        self.to_do_title_layout = QHBoxLayout()
        self.to_do_title_layout.setContentsMargins(20, 10, 25, 10)

        self.to_do_title_label = QLabel("待办事项:")
        self.to_do_title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.to_do_ddl_label = QLabel("DDL:")
        self.to_do_ddl_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.sort_by_ddl_button = QPushButton()
        self.sort_by_ddl_button.setIcon(QIcon("./排序.png"))
        self.sort_by_ddl_button.setFixedSize(QSize(13, self.to_do_title_label.sizeHint().height()))  # 设置按钮高度与标签高度一致
        self.sort_by_ddl_button.setStyleSheet('''
        QPushButton {border:none;background-color:transparent;}
        QPushButton::icon {
            width: 100%;
            height: 100%;
        }
        ''')
        self.sort_by_ddl_button.clicked.connect(self.sort_by_ddl)

        self.to_do_title_layout.addWidget(self.to_do_title_label)
        self.to_do_title_layout.addWidget(self.to_do_ddl_label)
        self.to_do_title_layout.addWidget(self.sort_by_ddl_button)

        self.to_do_list = QListWidget()
        self.to_do_list.setStyleSheet("padding: 10px;")
        self.to_do_list.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        # 默认是单选模式，启用多选模式
        self.to_do_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.to_do_list.doubleClicked.connect(self.on_double_clicked)

        # 创建操作按钮
        self.buttons_layout = QHBoxLayout()
        self.mark_done_button = QPushButton("标记完成")
        self.mark_done_button.clicked.connect(self.mark_item_done)
        self.delete_button = QPushButton("删除")
        self.delete_button.clicked.connect(self.delete_item)
        self.buttons_layout.addWidget(self.mark_done_button)
        self.buttons_layout.addWidget(self.delete_button)

        # 将布局添加到主窗口
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.add_layout)
        self.main_layout.addLayout(self.to_do_title_layout)
        self.main_layout.addWidget(self.to_do_list)
        self.main_layout.addLayout(self.buttons_layout)

        # 设置窗口布局
        self.setLayout(self.main_layout)

        self.import_widget = ImportWidget(self)
        self.import_widget.import_finished.connect(self.batch_import)


        style_sheet = """* {
                            font-family: "华文新魏", "华文细黑", "方正兰亭黑", "Microsoft YaHei";  
                            font-size: 19px;
                        }
                        QLineEdit {
                            border: 1px solid pink;
                        }
                        QListWidget::item:selected {
                            background-color: skyblue;
                        }
                        QListWidget::item:hover {
                            background-color: skyblue;
                        }
                        /* 垂直滚动条 */
                        QScrollBar:vertical {
                            width: 20px;        /* 垂直滚动条宽度 */            
                        }
                        QScrollBar::handle:vertical {
                             background-color: blue;   /* 滚动条背景色 */
                        }
                        """

        self.setStyleSheet(style_sheet)
        
        self.init_from_file()

    def showAndWait(self):
        self.import_widget.show()

    def batch_import(self,json_data):
        self.import_widget.close()
        items = json_data['items']
        for item in items:
            self.add_item(item['title'],item['description'],item['deadline_time'],item['is_completed'])

    def export_to_clipboard(self,isCloseExport=False):
        # 获取所有任务
        items = []
        for i in range(self.to_do_list.count()):
            item = self.to_do_list.item(i)
            if item:
                todo_item = item.data(Qt.UserRole)
                items.append({
                    "title": todo_item.title,
                    "description": todo_item.description,
                    "deadline_time": todo_item.deadline_time,
                    "is_completed": todo_item.is_completed
                })
        # 转换为 JSON 格式
        json_data = {
            "items": items
        }
        json_str = json.dumps(json_data, indent=4, ensure_ascii=False)  # 格式化 JSON 字符串
        # 复制到剪切板
        clipboard = QApplication.clipboard()
        clipboard.setText(json_str)
        if isCloseExport:
            self.close()
            return
        # 弹出提示
        QMessageBox.information(self, "提示", "已复制到剪切板")
        
    def add_item(self,title=None, description=None,deadline_time=None, is_completed=False):
        # 如果 title 和 description 是传入的参数
        if title is not None or description is not None:
            # 使用传入的参数
            title = title.strip() if title else ""
            description = description.strip() if description else ""
            deadline_time = deadline_time.strip() if deadline_time else "未知"
        else:
            # 获取输入框的文本
            title = self.title_input.text().strip()
            description = self.description_input.text().strip()
            deadline_time = self.deadline_input.text().strip()
            if not deadline_time: deadline_time = "未知"
        # TODO 优化时间显示居右
        # 创建 ToDoItem 实例
        todo_item = ToDoItem(title, description,deadline_time,is_completed)
        # 创建新的列表项  创建自定义Widget
        item_widget = QWidget()
        layout = QHBoxLayout()

        # 标题部分
        title_label = QLabel(todo_item.title)
        title_label.setStyleSheet("QLabel{padding:0px}")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft| Qt.AlignmentFlag.AlignVCenter)

        # 时间部分
        time_label = QLabel(todo_item.deadline_time)
        time_label.setStyleSheet("QLabel{padding:0px}") # 添加padding设置，Qlabel有默认padding，不设置话，会将文字截断
        time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # 添加控件到布局
        layout.addWidget(title_label)
        layout.addWidget(time_label)
        item_widget.setLayout(layout)

        # 创建ListWidgetItem
        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())  # 设置每一项的宽高
        item.setToolTip(todo_item.description) # 设置悬浮提示
        item.setData(Qt.UserRole, todo_item)  # 保存任务对象
        item.setFlags(item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled |Qt.ItemIsEditable)
        if todo_item.is_completed:
            item.setCheckState(Qt.CheckState.Checked) 
            item_widget.setStyleSheet("QLabel{background-color:transparent;color:gray;}") 
        else:
            item.setCheckState(Qt.CheckState.Unchecked)
        self.to_do_list.addItem(item)
        self.to_do_list.setItemWidget(item, item_widget)
        
        # 清空输入框
        self.title_input.clear()
        self.description_input.clear()
        self.deadline_input.clear()

    def mark_item_done(self):
        # 获取当前选中的项
        selected_items = self.to_do_list.selectedItems()
        for item in selected_items:
            self.change_item_state(item)

    def delete_item(self):
        # 获取当前选中的项
        selected_items = self.to_do_list.selectedItems()
        for item in selected_items:
            self.to_do_list.takeItem(self.to_do_list.row(item))  # 删除 QListWidgetItem                         

    def change_item_state(self,item: QListWidgetItem):
        todo_item = item.data(Qt.UserRole)
        itemWidget = self.to_do_list.itemWidget(item)
        if item.checkState() == Qt.CheckState.Checked:
            todo_item.is_completed = False
            item.setCheckState(Qt.CheckState.Unchecked)
            itemWidget.setStyleSheet("QLabel{color:black;}")
        else:
            todo_item.is_completed = True
            item.setCheckState(Qt.CheckState.Checked)
            itemWidget.setStyleSheet("QLabel{background-color:transparent;color:gray;}")

    def on_double_clicked(self, index: QModelIndex):
        # print(index.row())  # 打印行号
        item = self.to_do_list.itemFromIndex(index)  # 获取 QListWidgetItem
        if item:
            self.change_item_state(item)
        else:
            print("QListWidgetItem获取失败")

    def init_from_file(self, file_path=None):
        # 默认初始化文件为当前目录下的 to_do.json
        if file_path is None:
            file_path = "./to_do.json"
            # 读取文件内容
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                self.batch_import(json.loads(text))
                print("读取文件成功")
        except FileNotFoundError:
            print("文件不存在")

    def sort_by_ddl(self):
        if self.sort_value == "asc":
            self.sort_value = "desc" 
        else:
            self.sort_value = "asc"
        # 按 DDL 排序
        items = []
        for i in range(self.to_do_list.count()):
            item = self.to_do_list.item(i)
            if item:
                todo_item = item.data(Qt.UserRole)
                items.append(todo_item)
        # 根据self.sort_value决定排序方向
        if self.sort_value == "asc":
            items.sort(key=self.sort_key)
        else:
            items.sort(key=self.sort_key, reverse=True)
        # 清空列表
        self.to_do_list.clear()
        # 重新添加排序后的任务
        for item in items:
            self.add_item(item.title, item.description, item.deadline_time, item.is_completed)
    
    def sort_key(self, item):
        item.deadline_time.replace("：",":")
        if item.deadline_time == "未知":
            return datetime.datetime.max
        else:
            return datetime.datetime.strptime(item.deadline_time.replace("：",":"), "%Y-%m-%d %H:%M")
          

    def closeEvent(self, event):
        # 关闭窗口时保存数据
        with open("./to_do.json", "w", encoding="utf-8") as f:
            self.export_to_clipboard(True)
            f.write(QApplication.clipboard().text())
            QApplication.clipboard().clear()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
