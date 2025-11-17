import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QDialog
)
from PyQt6.QtGui import QFont, QPixmap, QPainter
from PyQt6.QtCore import Qt, QTimer, QEvent

from keyboard import keyboard_buttons  # файл с раскладкой клавиатуры


BASE_W = 900
BASE_H = 700
BASE_KB_H = 350
BASE_KB_W = 870


class KeyboardWidget(QWidget):
    def __init__(self, parent=None):
        try:
            super().__init__(parent)
            self.buttons = {}
            self.norm_map = {}
            self.alias = {
                " ": "space",
                "\n": "enter",
                "\t": "tab",
                "\b": "backspace",
                "enter": "enter"
            }
            try:
                self.make_buttons()
            except Exception as e:
                print("Ошибка создания кнопок клавиатуры:", e)
        except Exception as e:
            print("Критическая ошибка в конструкторе KeyboardWidget:", e)

    def make_buttons(self):
        try:
            for name, x, y, w, h, color in keyboard_buttons:
                try:
                    btn = QPushButton(name, self)
                    btn.base_color = color
                    btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                    btn.setFont(QFont("Segoe Script", 12))
                    btn.setStyleSheet(f"background-color:{color}; border-radius:5px;")
                    btn.clicked.connect(lambda c, n=name: self.click(n))
                    self.buttons[name] = btn
                    self.norm_map[name.lower()] = name
                except Exception as e:
                    print(f"Ошибка создания кнопки {name}:", e)
                    continue
        except Exception as e:
            print("Ошибка создания клавиатуры:", e)

    def click(self, name):
        try:
            parent = self.parent()
            if not parent:
                return

            if name.lower() == "backspace":
                try:
                    txt = parent.input.text()
                    parent.input.setText(txt[:-1])
                    parent.check_live()
                except Exception as e:
                    print("Ошибка обработки Backspace:", e)
                return

            if name.lower() == "enter":
                try:
                    parent.check_word()
                except Exception as e:
                    print("Ошибка обработки Enter:", e)
                return

            if name.lower() == "space":
                try:
                    parent.insert_char(" ")
                except Exception as e:
                    print("Ошибка обработки Space:", e)
                return

            try:
                ch = name[0].lower()
                parent.insert_char(ch)
            except Exception as e:
                print(f"Ошибка обработки клавиши {name}:", e)

        except Exception as e:
            print("Ошибка в click:", e)

    def highlight(self, key):
        try:
            for btn in self.buttons.values():
                try:
                    btn.setStyleSheet(f"background-color:{btn.base_color}; border-radius:5px;")
                except Exception as e:
                    print("Ошибка сброса подсветки кнопки:", e)
                    continue

            if key is None:
                return

            if key in self.alias:
                key = self.alias[key]

            key = str(key).lower()
            target = None
            if key in self.norm_map:
                target = self.norm_map[key]
            else:
                for k in self.buttons.keys():
                    if k.lower() == key:
                        target = k

            if target and target in self.buttons:
                try:
                    self.buttons[target].setStyleSheet("background-color:red; border-radius:5px;")
                except Exception as e:
                    print(f"Ошибка подсветки кнопки {target}:", e)
        except Exception as e:
            print("Ошибка в highlight:", e)

    def resize_keyboard(self, W, H):
        try:
            scale_x = W / BASE_KB_W
            scale_y = H / BASE_KB_H
            s = min(scale_x, scale_y)

            for name, x, y, w, h, color in keyboard_buttons:
                try:
                    if name in self.buttons:
                        btn = self.buttons[name]
                        btn.setGeometry(int(x * s), int(y * s), int(w * s), int(h * s))
                        btn.setFont(QFont("Segoe Script", max(8, int(12 * s))))
                except Exception as e:
                    print(f"Ошибка изменения размера кнопки {name}:", e)
                    continue

            self.setFixedSize(int(BASE_KB_W * s), int(BASE_KB_H * s))
        except Exception as e:
            print("Ошибка в resize_keyboard:", e)


class HelpDialog(QDialog):
    def __init__(self):
        try:
            super().__init__()
            try:
                self.setWindowTitle("Помощь")
                self.setMinimumSize(400, 300) 
            except Exception as e:
                print("Ошибка установки параметров окна HelpDialog:", e)

            try:
                self.layout = QVBoxLayout(self)
                self.layout.setContentsMargins(0, 0, 0, 0)
                self.layout.setSpacing(0)
            except Exception as e:
                print("Ошибка создания окна HelpDialog:", e)

            # === Картинка ===
            try:
                self.lbl = QLabel(self)
                self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                try:
                    self.pixmap = QPixmap("k.jpg")
                    if not self.pixmap.isNull():
                        self.lbl.setPixmap(self.pixmap)
                    else:
                        print("Файл k.jpg не найден или поврежден")
                        self.pixmap = QPixmap()
                except Exception as e:
                    print("Ошибка загрузки картинки:", e)
                    self.pixmap = QPixmap()
                self.lbl.setScaledContents(True)  # масштабирование по размеру окна
                if hasattr(self, 'layout'):
                    self.layout.addWidget(self.lbl)
            except Exception as e:
                print("Ошибка создания метки картинки:", e)

            # === "Закрыть"  ===
            try:
                self.btn_close = QPushButton("Закрыть", self)
                self.btn_close.setFont(QFont("Segoe Script", 14))
                self.btn_close.setStyleSheet("background-color: red; color: white; border-radius: 5px;")
                self.btn_close.clicked.connect(self.close)
                if hasattr(self, 'layout'):
                    self.layout.addWidget(self.btn_close, alignment=Qt.AlignmentFlag.AlignCenter)
            except Exception as e:
                print("Ошибка создания кнопки закрытия:", e)
        except Exception as e:
            print("Критическая ошибка в конструкторе HelpDialog:", e)

    # Обновляем размер картинки при изменении окна
    def resizeEvent(self, event):
        try:
            super().resizeEvent(event)
            if hasattr(self, 'pixmap') and not self.pixmap.isNull():
                try:
                    if hasattr(self, 'lbl'):
                        self.lbl.setPixmap(self.pixmap.scaled(self.lbl.size(), Qt.AspectRatioMode.KeepAspectRatio))
                except Exception as e:
                    print("Ошибка обновления размера картинки:", e)
        except Exception as e:
            print("Ошибка в resizeEvent HelpDialog:", e)


class WordTrainer(QWidget):
    def __init__(self, parent_app=None):
        try:
            super().__init__()
            self.parent_app = parent_app
            try:
                self.setWindowTitle("Тренажёр слов")
                self.setMinimumSize(650, 500)
            except Exception as e:
                print("Ошибка установки параметров окна:", e)

            # === ФОН ===
            try:
                self.bg = QPixmap("r.jpg")
            except Exception as e:
                print("Ошибка загрузки фона:", e)
                self.bg = QPixmap()

            try:
                self.words = self.load_words()
                self.index = 0
                self.errors = 0
            except Exception as e:
                print("Ошибка загрузки слов:", e)
                self.words = ["пример", "слово", "текст"]
                self.index = 0
                self.errors = 0

            # === СООБЩЕНИЕ ОБ ОШИБКЕ ===
            try:
                self.error_msg = QLabel("")
                self.error_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.error_msg.setFont(QFont("Segoe Script", 16, QFont.Weight.Bold))
                self.error_msg.setStyleSheet("color: red;")
                self.error_msg.hide()
            except Exception as e:
                print("Ошибка создания сообщения об ошибке:", e)

            try:
                self.word_label = QLabel("")
                self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.word_label.setFont(QFont("Segoe Script", 24))
            except Exception as e:
                print("Ошибка создания метки слова:", e)

            try:
                self.input = QLineEdit()
                self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.input.setFont(QFont("Segoe Script", 18))
                self.input.returnPressed.connect(self.check_word)
                self.input.textEdited.connect(self.check_live)
            except Exception as e:
                print("Ошибка создания поля ввода:", e)

            try:
                self.error_label = QLabel("Ошибок: 0")
                self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.error_label.setFont(QFont("Segoe Script", 18))
            except Exception as e:
                print("Ошибка создания метки ошибок:", e)

            try:
                self.help_btn = QPushButton("Помощь")
                self.help_btn.clicked.connect(lambda: HelpDialog().exec())
                self.help_btn.setFont(QFont("Segoe Script", 18))
                self.help_btn.setStyleSheet("background-color: red; color: white; border-radius: 5px;")
            except Exception as e:
                print("Ошибка создания кнопки помощи:", e)

            try:
                self.exit_btn = QPushButton("Выйти")
                self.exit_btn.clicked.connect(self.go_to_main)
                self.exit_btn.setFont(QFont("Segoe Script", 18))
                self.exit_btn.setStyleSheet("background-color: black; color: white; border-radius: 5px;")
            except Exception as e:
                print("Ошибка создания кнопки выхода:", e)

            try:
                top_bar = QHBoxLayout()
                top_bar.addWidget(self.exit_btn)
                top_bar.addStretch(1)
                top_bar.addWidget(self.help_btn)

                self.main_area = QVBoxLayout()
                self.main_area.addLayout(top_bar)
                self.main_area.addStretch(1)
                self.main_area.addWidget(self.error_msg)
                self.main_area.addWidget(self.word_label)
                self.main_area.addWidget(self.input, alignment=Qt.AlignmentFlag.AlignCenter)
                self.main_area.addWidget(self.error_label, alignment=Qt.AlignmentFlag.AlignCenter)
                self.main_area.addStretch(1)
            except Exception as e:
                print("Ошибка создания интерфейса:", e)

            try:
                self.keyboard = KeyboardWidget(self)
            except Exception as e:
                print("Ошибка создания клавиатуры:", e)
                self.keyboard = None

            try:
                layout = QVBoxLayout(self)
                layout.setContentsMargins(10, 10, 10, 10)
                layout.addLayout(self.main_area)
                if self.keyboard:
                    layout.addWidget(self.keyboard, alignment=Qt.AlignmentFlag.AlignCenter)
            except Exception as e:
                print("Ошибка установки основного лейаута:", e)

            try:
                self.show_word()
                self.highlight_expected()
                if hasattr(self, 'input'):
                    self.input.installEventFilter(self)
            except Exception as e:
                print("Ошибка инициализации отображения:", e)

            try:
                QTimer.singleShot(100, self.resize_all)
            except Exception as e:
                print("Ошибка установки таймера изменения размера:", e)
        except Exception as e:
            print("Критическая ошибка в конструкторе WordTrainer:", e)

    def go_to_main(self):
        try:
            self.close()
            if self.parent_app:
                try:
                    self.parent_app.show()
                except Exception as e:
                    print("Ошибка показа главного окна:", e)
        except Exception as e:
            print("Ошибка выхода:", e)

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            if hasattr(self, 'bg') and not self.bg.isNull():
                painter.drawPixmap(self.rect(), self.bg)
        except Exception as e:
            print("Ошибка в paintEvent:", e)

    def load_words(self):
        try:
            with open("word.txt", "r", encoding="utf-8") as f:
                return f.read().split()
        except FileNotFoundError:
            print("Файл word.txt не найден, используются слова по умолчанию")
            return ["пример", "слово", "текст"]
        except Exception as e:
            print("Ошибка чтения файла word.txt:", e)
            return ["пример", "слово", "текст"]

    def show_word(self):
        try:
            if self.index < len(self.words):
                if hasattr(self, 'word_label'):
                    self.word_label.setText(self.words[self.index])
                if hasattr(self, 'input'):
                    self.input.setText("")
                    self.input.setStyleSheet("color:black;")
            else:
                if hasattr(self, 'word_label'):
                    self.word_label.setText("Готово!")
                if hasattr(self, 'input'):
                    self.input.setDisabled(True)
            self.highlight_expected()
        except Exception as e:
            print("Ошибка в show_word:", e)

    def show_error_message(self):
        try:
            if hasattr(self, 'error_msg'):
                self.error_msg.setText("Ошибка")
                self.error_msg.show()
                QTimer.singleShot(700, lambda: self.error_msg.hide() if hasattr(self, 'error_msg') else None)
        except Exception as e:
            print("Ошибка показа сообщения об ошибке:", e)

    def insert_char(self, ch):
        try:
            if hasattr(self, 'input'):
                self.input.insert(ch)
                self.check_live()
        except Exception as e:
            print("Ошибка вставки символа:", e)

    def check_live(self):
        try:
            if self.index < len(self.words):
                word = self.words[self.index]
                if hasattr(self, 'input'):
                    typed = self.input.text()
                    if typed == word[:len(typed)]:
                        self.input.setStyleSheet("color:green;")
                    else:
                        self.input.setStyleSheet("color:red;")
                        self.show_error_message()
        except Exception as e:
            print("Ошибка в check_live:", e)

    def check_word(self):
        try:
            if self.index < len(self.words):
                word = self.words[self.index]
                if hasattr(self, 'input'):
                    typed = self.input.text()
                    if typed == word:
                        self.index += 1
                        self.show_word()
                    else:
                        self.errors += 1
                        if hasattr(self, 'error_label'):
                            self.error_label.setText(f"Ошибок: {self.errors}")
                        if hasattr(self, 'input'):
                            self.input.selectAll()
                        self.show_error_message()
        except Exception as e:
            print("Ошибка в check_word:", e)

    def resize_all(self):
        try:
            W = self.width()
            H = self.height()
            kb_h = H * 0.50
            kb_w = W - 40
            if hasattr(self, 'keyboard'):
                try:
                    self.keyboard.resize_keyboard(kb_w, kb_h)
                except Exception as e:
                    print("Ошибка изменения размера клавиатуры:", e)
            
            scale = W / BASE_W
            try:
                if hasattr(self, 'word_label'):
                    self.word_label.setFont(QFont("Segoe Script", max(18, int(40 * scale))))
                if hasattr(self, 'input'):
                    self.input.setFont(QFont("Segoe Script", max(14, int(22 * scale))))
                    self.input.setFixedWidth(int(W * 0.5))
                    self.input.setFixedHeight(int(45 * scale))
                if hasattr(self, 'error_label'):
                    self.error_label.setFont(QFont("Segoe Script", max(12, int(18 * scale))))
                if hasattr(self, 'error_msg'):
                    self.error_msg.setFont(QFont("Segoe Script", max(14, int(16 * scale)), QFont.Weight.Bold))
                if hasattr(self, 'help_btn'):
                    self.help_btn.setFont(QFont("Segoe Script", max(10, int(14 * scale))))
                if hasattr(self, 'exit_btn'):
                    self.exit_btn.setFont(QFont("Segoe Script", max(10, int(14 * scale))))
            except Exception as e:
                print("Ошибка установки шрифтов:", e)
        except Exception as e:
            print("Ошибка в resize_all:", e)

    def resizeEvent(self, event):
        try:
            super().resizeEvent(event)
            self.resize_all()
        except Exception as e:
            print("Ошибка в resizeEvent:", e)

    def eventFilter(self, obj, event):
        try:
            if obj is self.input:
                if event.type() == QEvent.Type.KeyPress:
                    try:
                        key = event.key()
                        ch = event.text()
                        if hasattr(self, 'keyboard'):
                            if key == Qt.Key.Key_Space:
                                self.keyboard.highlight("space")
                            elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                                self.keyboard.highlight("enter")
                            elif key == Qt.Key.Key_Backspace:
                                self.keyboard.highlight("backspace")
                            elif ch:
                                self.keyboard.highlight(ch.lower())
                            else:
                                self.keyboard.highlight(None)
                    except Exception as e:
                        print("Ошибка обработки нажатия клавиши:", e)
                elif event.type() == QEvent.Type.KeyRelease:
                    try:
                        QTimer.singleShot(30, self.highlight_expected)
                    except Exception as e:
                        print("Ошибка обработки отпускания клавиши:", e)
        except Exception as e:
            print("Ошибка в eventFilter:", e)
        return super().eventFilter(obj, event)

    def highlight_expected(self):
        try:
            if self.index < len(self.words):
                w = self.words[self.index]
                if hasattr(self, 'input') and hasattr(self, 'keyboard'):
                    pos = len(self.input.text())
                    if pos < len(w):
                        self.keyboard.highlight(w[pos])
                    else:
                        self.keyboard.highlight("enter")
                else:
                    if hasattr(self, 'keyboard'):
                        self.keyboard.highlight(None)
            else:
                if hasattr(self, 'keyboard'):
                    self.keyboard.highlight(None)
        except Exception as e:
            print("Ошибка в highlight_expected:", e)


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        win = WordTrainer()
        win.show()
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("Программа прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print("ОШИБКА ЗАПУСКА:", e)
        try:
            import traceback
            traceback.print_exc()
        except:
            pass
        sys.exit(1)
