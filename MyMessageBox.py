import sys
import random
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer 
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QMovie,QPainter

class MyMessageBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.InitUI()
        self.setQSS()
        self.show()

    
    def InitUI(self):
        self.setWindowTitle('小D的提醒')
        # self.setStyleSheet(r'''*{"
        # "border-radius: 10px;"}''')

        # 设置提示语
        self.setWarmHeartSentences()
        
        # 设置按钮
        self.buttons_layout = QHBoxLayout()
        self.yes_button = QPushButton('好的', self)
        self.another_button = QPushButton('换一个', self)
        self.yes_button.clicked.connect(self.close_)
        self.another_button.clicked.connect(self.changeAnotherSentence)
        self.buttons_layout.addWidget(self.yes_button)
        self.buttons_layout.addWidget(self.another_button)

        # gif动画
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_list = [
            r'python\pyQt\ToDoApp\cccat.gif',
            r'python\pyQt\ToDoApp\cccat_eat.gif',
            r'python\pyQt\ToDoApp\cccat_fish.gif',
            r'python\pyQt\ToDoApp\cccat_smile.gif',
            r'python\pyQt\ToDoApp\cccat_lazy.gif',
        ]
        self.gif_label.setMovie(QMovie(random.choice(self.gif_list)))
        self.gif_label.setScaledContents(False)
        self.gif_label.movie().start()

        # 总体布局
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.sentence_label)
        self.main_layout.addWidget(self.gif_label)
        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

    def setQSS(self):
        pass

    def setWarmHeartSentences(self) -> None:
        self.warm_sentences = [
            "不要不开心啦",
            "要按时吃饭噢",
            "别忘了穿好衣服噢",
            "记得按时睡觉啦",
            "笨笨小D加油啦",
            "宝宝最棒捏"
        ]
        self.sentence_label = QLabel(self)
        self.sentence_label.setText(random.choice(self.warm_sentences))
        self.sentence_label.setAlignment(Qt.AlignCenter)
        self.sentence_label.setFont(QFont('华文新魏', 20))

    def changeAnotherSentence(self) -> None:
        self.sentence_label.clear() 
        self.sentence_label.setText(random.choice(self.warm_sentences))
        self.gif_label.movie().stop()
        self.gif_label.setMovie(QMovie(random.choice(self.gif_list)))
        self.gif_label.movie().start()
        

    def close_(self):
        self.close() # 关闭窗口后，将窗口对象销毁

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_message_box = MyMessageBox()
    sys.exit(app.exec_())