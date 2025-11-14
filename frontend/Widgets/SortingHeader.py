from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class SortingHeader(QWidget):
    def __init__(self,text: str, callback , parent=None):
        super().__init__(parent)
        self.state=0
        self.base_text=text
        self.setupUi()
        self.callback=callback


    def setupUi(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.label = QLabel(self.base_text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)


    def onclick(self):
        self.state+=1
        if self.state>1:
            self.state=-1
            self.label.setText(self.base_text+" ▼")
        if self.state==0:
            self.label.setText(self.base_text)
        if self.state==1:
            self.label.setText(self.base_text+" ▲")


    def mousePressEvent(self, event):
        self.onclick()
        self.callback()
        return super().mousePressEvent(event)

    def get_txt(self):
        return self.base_text
    def get_state (self):
        return self.state
