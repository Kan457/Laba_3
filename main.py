import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QMovie, QFont, QPixmap
from PyQt6.QtCore import Qt
from test import TypingTren
from word import WordTren

class MyApp(QWidget):
    def __init__(self):
        super.__init__()
        self.setWindowTitle("Клавиатурный тренажёр")

        self.resize(800,400)
        self.setMinimumSize(600,300)

    # ======= ФОН ======== 
        self.back_label = QLabel(self)
        self.back_label.setPixmap(QPixmap("f.jpg"))
        self.back_label.setScaledContents(True)
        self.back_label.lower()

    # ======= GIF ======== 
        #ЛЕВАЯ
        self.gift_left = QLabel(self)
        self.movie_left = QMovie("g.gif")
        self.gift_left.setMovie(self.movie_left)
        self.gift_left.start()

        #ПРАВАЯ
        self.gift_rigth = QLabel(self)
        self.movie_rigth = QMovie("g.gif")
        self.gift_rigth.setMovie(self.movie_rigth)
        self.gift_rigth.start()  

    # ===== ЗАГОЛОВОК ======
        self.title = QLabel("Клавиатурный тренажёр" , self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("color: black; font-weigth: bold;")  #CSS

    # ====== КНОПКИ =======
        self.button_word = QPushButton("Пройти обучение", self)
        self.button_word.clicked.connect(self.open_word_trainer)
        self.button_word.setStyleSheet("background-color: rgba(255,255,255,180); font-weight: bold;")

        self.button_test = QPushButton("Пройти тест", self)
        self.button_test.clicked.connect(self.open_typing_trainer)
        self.button_test.setStyleSheet("background-color: rgba(255,255,255,180); font-weight: bold;")

    # ==== ПРИ ИЗМЕН.ПОЗИЦ ====
        self.resizeEvent(None)

    # ==== ИЗМЕНЕНИЕ ПОЗИЦИИ ====
    def resizeEvent(self, event):
        w = self.width
        h = self.height

    # ====== ОКНО =======
        self.back_label.setGeometry(0,0,w,h)
        title_size = max(16, h//15)
        button_size = max(12, h//20)

    # ====== КНОПКИ =======
        self.title.setFont(QFont("Segoe Script", title_size , QFont.Weight.Bold))
        self.button_word.setFont(QFont("Segoe Script", button_size , QFont.Weight.Bold))
        self.button_test.setFont(QFont("Segoe Script", button_size , QFont.Weight.Bold))

    # ====== GIF =======
        gif_width = int(w * 0.08)
        gif_height = int(h * 0.15)

        #====== ЛЕВАЯ =======
        self.gift_left.setGeometry(20 , 20 , gif_width , gif_height)
        self.movie_left.setScaledSize(self.gift_left.size())

        #====== ПРАВАЯ =======
        self.gift_rigth.setGeometry(w - gif_width - 20 , 20 , gif_width , gif_height)
        self.movie_rigth.setScaledSize(self.gift_rigth.size())

        # ===== ЗАГОЛОВОК ======
        title_x = 20 + gif_width + 10 #отступ + ширина 
        title_width = w - 2*(gif_width + 20 + 10)#щирина заголовка
        title_height = gif_height
        self.title.setGeometry(title_x, 20 , title_width , title_height)

        # ====== КНОПКИ =======
        button_weigth = int(w*0.5)
        button_heigth = int(h*0.2)
        space_between = int(h * 0.05)

        y_start = title_height + 40
        x_center = (w - button_weigth)//2

        self.button_word.setGeometry(x_center , y_start , button_weigth , button_heigth)
        self.button_test.setGeometry(x_center , y_start + button_heigth + space_between , button_weigth , button_heigth)

    # === Открытие окна обучения  ===
    def open_word_tren(self):
        self.tren_windows = TypingTren(app_first = self)
        self.tren_windows.show()
        self.hide()

    # === Открытие окна тестирования ===
    def open_test_tren(self):
        self.tren_window = WordTren(app_first = self)
        self.tren_window.show()
        self.hide()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp
    window.show()
    sys.exit(app.exec())