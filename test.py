import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor, QFont, QPixmap, QKeyEvent
from PyQt6.QtCore import Qt, QTimer, QTime

from keyboard import keyboard_buttons  

RECORD_FILE = "record.txt"  

class KeyboardWidget(QWidget):
    def __init__(self, parent, input_field):
        try:
            super().__init__(parent)
            self.input_field = input_field
            self.buttons = {}
            self.key_ids = []
            try:
                self.create_keyboard()
            except Exception as e:
                print("Ошибка создания клавиатуры:", e)
        except Exception as e:
            print("Критическая ошибка в конструкторе KeyboardWidget:", e)

    #=====СОЗДАНИЕ КНОПОК======
    def create_keyboard(self):
        try:
            font = QFont("Segoe Script", 12)
            for idx, (name, x, y, w, h, color) in enumerate(keyboard_buttons):
                try:
                    btn = QPushButton(name, self)
                    btn.setFont(font)
                    btn.base_color = color
                    btn.setStyleSheet(f"background-color: {color}; border-radius: 5px; font-weight: bold;")
                    btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                    btn.clicked.connect(lambda checked, key=name: self.insert_key(key))
                    key_id = f"{name}_{idx}"
                    self.buttons[key_id] = btn
                    self.key_ids.append(key_id)
                except Exception as e:
                    print(f"Ошибка создания кнопки {name}:", e)
                    continue
        except Exception as e:
            print("Ошибка создания клавиатуры:", e)

    #======ПОДСВЕТКА НУЖНОЙ КЛАВИШИ======
    def highlight_key(self, key):
        try:
            for idx, (name, *_rest) in enumerate(keyboard_buttons):
                try:
                    if idx < len(self.key_ids) and self.key_ids[idx] in self.buttons:
                        btn = self.buttons[self.key_ids[idx]]
                        btn.setStyleSheet(f"background-color: {btn.base_color}; border-radius:5px; font-weight:bold;")
                except Exception as e:
                    print(f"Ошибка сброса подсветки кнопки {idx}:", e)
                    continue

            key_lower = key.lower()
            for idx, (name, *_rest) in enumerate(keyboard_buttons):
                try:
                    if name.lower() == key_lower:
                        if idx < len(self.key_ids) and self.key_ids[idx] in self.buttons:
                            btn = self.buttons[self.key_ids[idx]]
                            btn.setStyleSheet("background-color:red; border-radius:5px; font-weight:bold;")
                        break
                except Exception as e:
                    print(f"Ошибка подсветки кнопки {name}:", e)
                    continue
        except Exception as e:
            print("Ошибка в highlight_key:", e)

    #======КЛИКИ======
    def insert_key(self, key):
        try:
            cursor = self.input_field.textCursor()
            k_lower = key.lower()

            if k_lower == "backspace":
                cursor.deletePreviousChar()
            elif k_lower == "enter":
                cursor.insertText("\n")
            elif k_lower == "space":
                cursor.insertText(" ")
            else:
                cursor.insertText(key.lower())

            self.input_field.setTextCursor(cursor)
            parent = self.input_field.parent()
            if hasattr(parent, 'update_display'):
                try:
                    parent.update_display()
                    parent.update_caret_and_keyboard()
                except Exception as e:
                    print("Ошибка обновления отображения:", e)
        except Exception as e:
            print("Ошибка в insert_key:", e)

    #======ИЗМЕНЕНИЕ РАЗМЕРА======
    def resizeEvent(self, event):
        try:
            super().resizeEvent(event)
            w, h = self.width(), self.height()
            base_w, base_h = 870, 350
            for idx, (name, x, y, bw, bh, color) in enumerate(keyboard_buttons):
                try:
                    if idx < len(self.key_ids) and self.key_ids[idx] in self.buttons:
                        btn = self.buttons[self.key_ids[idx]]
                        new_x = int(x / base_w * w)
                        new_y = int(y / base_h * h)
                        new_w = max(int(bw / base_w * w), 30)
                        new_h = max(int(bh / base_h * h), 30)
                        btn.setGeometry(new_x, new_y, new_w, new_h)
                except Exception as e:
                    print(f"Ошибка изменения размера кнопки {idx}:", e)
                    continue
        except Exception as e:
            print("Ошибка в resizeEvent клавиатуры:", e)


class TypingTrainer(QWidget):
    def __init__(self, parent_app=None):
        try:
            super().__init__()
            self.parent_app = parent_app

            try:
                self.setWindowTitle("Тренажёр набора текста")
                self.resize(900, 650)
                self.setMinimumSize(600, 400)
            except Exception as e:
                print("Ошибка установки параметров окна:", e)

            try:
                self.original_text = ""
                self.error_count = 0
                self.timer_running = False
                self.time = QTime(0, 0, 0)
                self.best_time = None
            except Exception as e:
                print("Ошибка инициализации переменных:", e)
                self.original_text = ""
                self.error_count = 0
                self.timer_running = False
                self.time = QTime(0, 0, 0)
                self.best_time = None

            # Фон
            try:
                self.background_label = QLabel(self)
                try:
                    self.background_label.setPixmap(QPixmap("u.png"))
                    self.background_label.setScaledContents(True)
                    self.background_label.lower()
                except Exception as e:
                    print("Ошибка загрузки фона:", e)
            except Exception as e:
                print("Ошибка создания фона:", e)

            try:
                self.init_ui()
            except Exception as e:
                print("Ошибка инициализации UI:", e)

            try:
                self.load_text_from_file()
            except Exception as e:
                print("Ошибка загрузки текста:", e)

            try:
                self.load_record()
            except Exception as e:
                print("Ошибка загрузки рекорда:", e)

            try:
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update_timer)
            except Exception as e:
                print("Ошибка создания таймера:", e)
                self.timer = None

            try:
                if hasattr(self, 'user_input'):
                    self.keyboard_widget = KeyboardWidget(self, self.user_input)
                    QTimer.singleShot(100, self.update_caret_and_keyboard)
                else:
                    print("Поле ввода не создано, клавиатура не будет создана")
                    self.keyboard_widget = None
            except Exception as e:
                print("Ошибка создания клавиатуры:", e)
                self.keyboard_widget = None
        except Exception as e:
            print("Критическая ошибка в конструкторе TypingTrainer:", e)

    def init_ui(self):
        try:
            self.original_display = QTextEdit(self)
            self.original_display.setReadOnly(True)
        except Exception as e:
            print("Ошибка создания поля отображения текста:", e)

        try:
            self.user_input = QTextEdit(self)
            self.user_input.textChanged.connect(self.update_display)
        except Exception as e:
            print("Ошибка создания поля ввода:", e)

        try:
            self.error_label = QLabel("Ошибок: 0", self)
            self.timer_label = QLabel("Время: 00:00", self)
            self.best_time_label = QLabel("Рекорд: —", self)
            self.best_time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        except Exception as e:
            print("Ошибка создания меток:", e)

        try:
            self.exit_button = QPushButton("Выйти", self)
            self.exit_button.setStyleSheet("background-color: black; color: white;")
            self.exit_button.clicked.connect(self.go_to_main)
        except Exception as e:
            print("Ошибка создания кнопки выхода:", e)

    # =================== виртуальная клавиатура ===================
    def update_caret_and_keyboard(self):
        try:
            pos = len(self.user_input.toPlainText())
            if pos >= len(self.original_text):
                return
            next_char = self.original_text[pos]
            if hasattr(self, 'keyboard_widget'):
                try:
                    if next_char == " ":
                        self.keyboard_widget.highlight_key("Space")
                    elif next_char == "\n":
                        self.keyboard_widget.highlight_key("Enter")
                    else:
                        self.keyboard_widget.highlight_key(next_char.lower())
                except Exception as e:
                    print("Ошибка подсветки клавиши:", e)

            try:
                cursor = self.original_display.textCursor()
                cursor.setPosition(pos)
                fmt = QTextCharFormat()
                fmt.setForeground(QColor("green"))
                fmt.setFontUnderline(True)
                cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)
                cursor.setCharFormat(fmt)
            except Exception as e:
                print("Ошибка обновления курсора:", e)
        except Exception as e:
            print("Ошибка в update_caret_and_keyboard:", e)

    # =================== Физическая клавиатура ====================
    def keyPressEvent(self, event: QKeyEvent):
        try:
            if len(self.user_input.toPlainText()) == 0 and not self.timer_running:
                return  # таймер не запускается пока нет первой буквы

            pos = len(self.user_input.toPlainText())
            if pos >= len(self.original_text):
                return

            expected = self.original_text[pos]
            key = event.key()
            text = event.text().lower()

            if key == Qt.Key.Key_Space:
                pressed = " "
                virt = "Space"
            elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                pressed = "\n"
                virt = "Enter"
            elif key == Qt.Key.Key_Backspace:
                try:
                    self.user_input.textCursor().deletePreviousChar()
                    if hasattr(self, 'keyboard_widget'):
                        self.keyboard_widget.highlight_key("Backspace")
                except Exception as e:
                    print("Ошибка обработки Backspace:", e)
                return
            else:
                pressed = text
                virt = text

            if pressed == expected:
                try:
                    self.user_input.insertPlainText(pressed)
                    self.update_display()
                except Exception as e:
                    print("Ошибка вставки текста:", e)
            else:
                try:
                    self.error_count += 1
                    if hasattr(self, 'error_label'):
                        self.error_label.setText(f"Ошибок: {self.error_count}")
                except Exception as e:
                    print("Ошибка обновления счетчика ошибок:", e)

            if hasattr(self, 'keyboard_widget'):
                try:
                    self.keyboard_widget.highlight_key(virt)
                except Exception as e:
                    print("Ошибка подсветки клавиши:", e)
        except Exception as e:
            print("Ошибка в keyPressEvent:", e)

    def keyReleaseEvent(self, event):
        try:
            self.update_caret_and_keyboard()
        except Exception as e:
            print("Ошибка в keyReleaseEvent:", e)

    # =================== Основная логика ==========================
    def load_text_from_file(self):
        try:
            with open("text.txt", "r", encoding="utf-8") as f:
                self.original_text = f.read()
        except:
            self.original_text = "Файл text.txt не найден."
        self.original_display.setPlainText(self.original_text)

    def update_display(self):
        try:
            user_text = self.user_input.toPlainText()

            # Таймер запускается только после первой буквы
            if len(user_text) == 1 and not self.timer_running:
                try:
                    self.start_timer()
                except Exception as e:
                    print("Ошибка запуска таймера:", e)

            if len(user_text) >= len(self.original_text) and len(self.original_text) > 0:
                try:
                    self.stop_timer()
                    self.check_record()

                    QMessageBox.information(
                        self,
                        "Тест завершён",
                        f"Вы завершили тест!\nВремя: {self.time.toString('mm:ss')}\nОшибок: {self.error_count}"
                    )
                    self.start_new_session()
                    return
                except Exception as e:
                    print("Ошибка завершения теста:", e)

            try:
                fmt_correct = QTextCharFormat(); fmt_correct.setForeground(QColor("green"))
                fmt_error = QTextCharFormat(); fmt_error.setForeground(QColor("red"))
                fmt_future = QTextCharFormat(); fmt_future.setForeground(QColor("gray"))

                cursor = self.original_display.textCursor()
                cursor.select(QTextCursor.SelectionType.Document)
                cursor.setCharFormat(QTextCharFormat())

                self.error_count = 0
                for i, char in enumerate(user_text):
                    if i >= len(self.original_text):
                        self.error_count += 1
                        continue
                    try:
                        cursor.setPosition(i)
                        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)
                        cursor.setCharFormat(fmt_correct if char == self.original_text[i] else fmt_error)
                        if char != self.original_text[i]:
                            self.error_count += 1
                    except Exception as e:
                        print(f"Ошибка форматирования символа {i}:", e)
                        continue

                cursor.setPosition(len(user_text))
                cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
                cursor.setCharFormat(fmt_future)

                if hasattr(self, 'error_label'):
                    self.error_label.setText(f"Ошибок: {self.error_count}")
                self.update_caret_and_keyboard()
            except Exception as e:
                print("Ошибка форматирования текста:", e)
        except Exception as e:
            print("Ошибка в update_display:", e)

    # ================= Таймер ==================
    def start_timer(self):
        try:
            self.time = QTime(0, 0, 0)
            if hasattr(self, 'timer'):
                self.timer.start(1000)
            self.timer_running = True
        except Exception as e:
            print("Ошибка запуска таймера:", e)

    def update_timer(self):
        try:
            self.time = self.time.addSecs(1)
            if hasattr(self, 'timer_label'):
                self.timer_label.setText(f"Время: {self.time.toString('mm:ss')}")
        except Exception as e:
            print("Ошибка обновления таймера:", e)

    def stop_timer(self):
        try:
            if hasattr(self, 'timer'):
                self.timer.stop()
            self.timer_running = False
        except Exception as e:
            print("Ошибка остановки таймера:", e)

    # ================= Рекорды =================
    def load_record(self):
        try:
            if os.path.exists(RECORD_FILE):
                try:
                    with open(RECORD_FILE, "r") as f:
                        t = f.read().strip()
                        if t:
                            self.best_time = QTime.fromString(t, "mm:ss")
                except Exception as e:
                    print("Ошибка чтения файла рекорда:", e)
            if hasattr(self, 'best_time_label'):
                self.best_time_label.setText(
                    f"Рекорд: {self.best_time.toString('mm:ss') if self.best_time else '—'}"
                )
        except Exception as e:
            print("Ошибка в load_record:", e)

    def save_record(self):
        try:
            if self.best_time:
                with open(RECORD_FILE, "w") as f:
                    f.write(self.best_time.toString("mm:ss"))
        except Exception as e:
            print("Ошибка сохранения рекорда:", e)

    def check_record(self):
        try:
            if self.error_count > 0:
                return
            current_secs = self.time.minute() * 60 + self.time.second()
            best_secs = None
            if self.best_time:
                best_secs = self.best_time.minute() * 60 + self.best_time.second()
            if not self.best_time or current_secs < best_secs:
                self.best_time = QTime(0, self.time.minute(), self.time.second())
                self.save_record()
                if hasattr(self, 'best_time_label'):
                    self.best_time_label.setText(f"Рекорд: {self.best_time.toString('mm:ss')}")
        except Exception as e:
            print("Ошибка проверки рекорда:", e)

    # ================= Новый сеанс =================
    def start_new_session(self):
        try:
            if hasattr(self, 'user_input'):
                self.user_input.clear()
            self.error_count = 0
            if hasattr(self, 'error_label'):
                self.error_label.setText("Ошибок: 0")
            self.time = QTime(0, 0, 0)
            if hasattr(self, 'timer_label'):
                self.timer_label.setText("Время: 00:00")
            self.timer_running = False
            self.load_text_from_file()
            self.update_display()
            self.update_caret_and_keyboard()
        except Exception as e:
            print("Ошибка начала нового сеанса:", e)

    # ================= Выход ===================
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

    # ================= Разметка ==================
    def resizeEvent(self, event):
        try:
            super().resizeEvent(event)
            w, h = self.width(), self.height()
            
            try:
                if hasattr(self, 'background_label'):
                    self.background_label.setGeometry(0, 0, w, h)
            except Exception as e:
                print("Ошибка установки геометрии фона:", e)

            scale = min(w / 900, h / 650)

            try:
                top_height = int(h // 3)
                if hasattr(self, 'original_display'):
                    self.original_display.setGeometry(10, 10, w - 20, top_height)
                    self.original_display.setFont(QFont("Segoe Script", max(10, int(14 * scale))))

                input_height = int(h // 12)
                if hasattr(self, 'user_input'):
                    self.user_input.setGeometry(10, 20 + top_height, w - 20, input_height)
                    self.user_input.setFont(QFont("Segoe Script", max(10, int(14 * scale))))
            except Exception as e:
                print("Ошибка установки геометрии текстовых полей:", e)

            try:
                label_y = 30 + top_height + input_height
                if hasattr(self, 'error_label'):
                    self.error_label.setGeometry(20, label_y, 200, 40)
                if hasattr(self, 'timer_label'):
                    self.timer_label.setGeometry(230, label_y, 200, 40)
                if hasattr(self, 'best_time_label'):
                    self.best_time_label.setGeometry(430, label_y, 200, 40)
                font_label = QFont("Segoe Script", max(10, int(14 * scale)))
                if hasattr(self, 'error_label'):
                    self.error_label.setFont(font_label)
                if hasattr(self, 'timer_label'):
                    self.timer_label.setFont(font_label)
                if hasattr(self, 'best_time_label'):
                    self.best_time_label.setFont(font_label)
            except Exception as e:
                print("Ошибка установки геометрии меток:", e)

            try:
                if hasattr(self, 'exit_button'):
                    self.exit_button.setGeometry(w - 130, label_y, 110, 35)
                    self.exit_button.setFont(QFont("Segoe Script", max(10, int(12 * scale))))
            except Exception as e:
                print("Ошибка установки геометрии кнопки выхода:", e)

            try:
                keyboard_top = label_y + 60
                keyboard_height = h - keyboard_top - 10
                if hasattr(self, 'keyboard_widget'):
                    self.keyboard_widget.setGeometry(0, keyboard_top, w, keyboard_height)
            except Exception as e:
                print("Ошибка установки геометрии клавиатуры:", e)
        except Exception as e:
            print("Ошибка в resizeEvent:", e)


# ============= Запуск =============
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = TypingTrainer()
        window.show()
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
