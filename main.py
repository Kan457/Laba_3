import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QMovie, QFont, QPixmap
from PyQt6.QtCore import Qt

try:
    from test import TypingTrainer
except Exception as e:
    print("Ошибка импорта TypingTrainer:", e)  
    TypingTrainer = None

try:
    from word import WordTrainer
except Exception as e:
    print("Ошибка импорта WordTrainer:", e)  
    WordTrainer = None


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # ==== НАСТРОЙКА ОКНА ====
        try:
            self.setWindowTitle("Клавиатурный тренажёр")
            self.resize(800, 400)
            self.setMinimumSize(600, 300)
        except Exception as e:
            print("Ошибка установки параметров окна:", e)  

        # ==== ФОНОВОЕ ИЗОБРАЖЕНИЕ ====
        try:
            self.background_label = QLabel(self)
            pix = QPixmap("f.jpg")
            if pix.isNull():
                print("Файл f.jpg не найден")  
            else:
                self.background_label.setPixmap(pix)
            self.background_label.setScaledContents(True)
            self.background_label.lower()
        except Exception as e:
            print("Ошибка загрузки фона:", e)  


        # ==== ЛЕВЫЙ GIF ====

        try:
            self.gif_left = QLabel(self)
            self.movie_left = QMovie("g.gif")
            if not self.movie_left.isValid():
                print("GIF g.gif не найден ")  
            self.gif_left.setMovie(self.movie_left)
            self.movie_left.start()
        except Exception as e:
            print("Ошибка при загрузке левого GIF:", e)  


        # ==== ПРАВЫЙ GIF ====

        try:
            self.gif_right = QLabel(self)
            self.movie_right = QMovie("g.gif")
            if not self.movie_right.isValid():
                print("GIF g.gif не найден ")  
            self.gif_right.setMovie(self.movie_right)
            self.gif_right.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            self.movie_right.start()
        except Exception as e:
            print("Ошибка при загрузке правого GIF:", e)  

        # ==== ЗАГОЛОВОК ====

        try:
            self.title_label = QLabel("Клавиатурный тренажёр", self)
            self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.title_label.setStyleSheet("color: black; font-weight: bold;")
        except Exception as e:
            print("Ошибка создания заголовка:", e)  # === ОБРАБОТКА ИСКЛЮЧЕНИЯ ===

        # ==== КНОПКИ ====

        try:
            self.button_train = QPushButton("Пройти обучение", self)
            self.button_train.clicked.connect(self.safe_open_word_trainer)
            self.button_train.setStyleSheet(
                "background-color: rgba(255,255,255,180); font-weight: bold;"
            )

            self.button_test = QPushButton("Пройти тест", self)
            self.button_test.clicked.connect(self.safe_open_typing_trainer)
            self.button_test.setStyleSheet(
                "background-color: rgba(255,255,255,180); font-weight: bold;"
            )
        except Exception as e:
            print("Ошибка создания кнопок:", e) 


        # ==== ИЗМЕНЕНИЕ ИНТЕРФЕЙСА ====

        try:
            self.resizeEvent(None)
        except Exception as e:
            print("Ошибка изменения маштаба интерфейса :", e)  

    #  ==== РАЗМЕЩЕНИЕ ЭЛЕМЕНТОВ ==== 

    def resizeEvent(self, event):
        try:
            w = self.width()
            h = self.height()

            # Фон
            self.background_label.setGeometry(0, 0, w, h)

            # текст
            title_font_size = max(16, h // 15)
            button_font_size = max(12, h // 20)

            self.title_label.setFont(QFont("Segoe Script", title_font_size, QFont.Weight.Bold))
            self.button_train.setFont(QFont("Segoe Script", button_font_size, QFont.Weight.Bold))
            self.button_test.setFont(QFont("Segoe Script", button_font_size, QFont.Weight.Bold))

            # GIF 
            gif_width = int(w * 0.08)
            gif_height = int(h * 0.15)

            self.gif_left.setGeometry(20, 20, gif_width, gif_height)
            self.movie_left.setScaledSize(self.gif_left.size())

            self.gif_right.setGeometry(w - gif_width - 20, 20, gif_width, gif_height)
            self.movie_right.setScaledSize(self.gif_right.size())

            # Заголовок
            title_x = 20 + gif_width + 10
            title_width = w - 2 * (gif_width + 20 + 10)
            title_height = gif_height
            self.title_label.setGeometry(title_x, 20, title_width, title_height)

            # Кнопки
            button_width = int(w * 0.5)
            button_height = int(h * 0.20)
            space_between = int(h * 0.05)
            y_start = title_height + 40
            x_center = (w - button_width) // 2

            self.button_train.setGeometry(x_center, y_start, button_width, button_height)
            self.button_test.setGeometry(x_center,y_start + button_height + space_between,button_width,button_height)

        except Exception as e:
            print("Ошибка в resizeEvent:", e)  


    # ==== ОТКРЫТИЕ ОКОН ====

    def safe_open_word_trainer(self):
        try:
            self.open_word_trainer()
        except Exception as e:
            print("Ошибка при открытии WordTrainer:", e) 

    def safe_open_typing_trainer(self):
        try:
            self.open_typing_trainer()
        except Exception as e:
            print("Ошибка при открытии TypingTrainer:", e)  

    def open_word_trainer(self):
        if WordTrainer is None:
            print("WordTrainer не загружен!") 
            return
        self.trainer_window = WordTrainer(parent_app=self)
        self.trainer_window.show()
        self.hide()

    def open_typing_trainer(self):
        if TypingTrainer is None:
            print("TypingTrainer не загружен!") 
            return
        self.test_window = TypingTrainer(parent_app=self)
        self.test_window.show()
        self.hide()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MyApp()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print("ОШИБКА ЗАПУСКА:", e)  
