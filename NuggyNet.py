import sys
import os
import subprocess
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QMenu, QMessageBox, QStackedWidget
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Central widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Background color
        self.default_background_color = QColor("#202020")
        palette = self.main_widget.palette()
        palette.setColor(QPalette.Window, self.default_background_color)
        self.main_widget.setPalette(palette)
        self.main_widget.setAutoFillBackground(True)

        # Stacked widget for multiple web views
        self.web_stack = QStackedWidget()
        self.layout.addWidget(self.web_stack)

        # Web views
        self.nuggynet_view = QWebEngineView()
        self.chirp_view = QWebEngineView()
        self.web_stack.addWidget(self.nuggynet_view)
        self.web_stack.addWidget(self.chirp_view)

        # Initialize URL bar layout and controls
        self.url_bar_layout = QHBoxLayout()
        self.is_url_bar_at_top = False  # Default URL bar at the bottom
        self.layout.addLayout(self.url_bar_layout)  # Initially added at the bottom

        # Button styles
        button_style = """
            QPushButton {
                background-color: #ffcfcf;
                border-radius: 5px;
                border: 1px solid #aaaaaa;
                padding: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ffeacd;
            }
            QPushButton:pressed {
                background-color: #ffbbbb;
            }
        """

        # Back button
        self.back_button = QPushButton()
        self.back_button.setFixedSize(32, 32)
        self.back_button.setFont(QFont("Segoe MDL2 Assets", 16))
        self.back_button.setText("")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setStyleSheet(button_style)
        self.url_bar_layout.addWidget(self.back_button)

        # Forward button
        self.forward_button = QPushButton()
        self.forward_button.setFixedSize(32, 32)
        self.forward_button.setFont(QFont("Segoe MDL2 Assets", 16))
        self.forward_button.setText("")
        self.forward_button.clicked.connect(self.go_forward)
        self.forward_button.setStyleSheet(button_style)
        self.url_bar_layout.addWidget(self.forward_button)

        # Refresh button
        self.refresh_button = QPushButton()
        self.refresh_button.setFixedSize(32, 32)
        self.refresh_button.setFont(QFont("Segoe MDL2 Assets", 16))
        self.refresh_button.setText("")
        self.refresh_button.clicked.connect(self.reload_page)
        self.refresh_button.setStyleSheet(button_style)
        self.url_bar_layout.addWidget(self.refresh_button)

        # URL text box
        self.url_text_box = QLineEdit()
        self.url_text_box.setPlaceholderText("Enter URL")
        self.url_text_box.setFixedHeight(32)
        self.url_text_box.setFont(QFont("Segoe UI", 14))
        self.url_text_box.returnPressed.connect(self.handle_url_input)
        self.url_bar_layout.addWidget(self.url_text_box)

        # Switch button
        self.switch_button = QPushButton()
        self.switch_button.setFixedSize(50, 32)
        self.switch_button.setFont(QFont("Segoe MDL2 Assets", 16))
        self.switch_button.setText("")
        self.switch_button.setMenu(self.create_mode_menu())
        self.switch_button.setStyleSheet(button_style)
        self.url_bar_layout.addWidget(self.switch_button)

        # Options button
        self.options_button = QPushButton()
        self.options_button.setFixedSize(50, 32)
        self.options_button.setFont(QFont("Segoe MDL2 Assets", 16))
        self.options_button.setText("")
        self.options_button.setMenu(self.create_options_menu())
        self.options_button.setStyleSheet(button_style)
        self.url_bar_layout.addWidget(self.options_button)

        # Set initial mode
        self.set_nuggynet_mode()

        # Window title and size
        self.setWindowTitle("Nuggynet")
        self.setMinimumSize(1400, 700)

        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        # Set URLs
        self.nuggynet_view.setUrl(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "nwin.html")))
        self.chirp_view.setUrl(QUrl("https://beta.chirpsocial.net"))

        # Signal connections
        self.nuggynet_view.urlChanged.connect(self.update_buttons)
        self.chirp_view.urlChanged.connect(self.handle_chirp_url_change)

        # Initial button states
        self.update_buttons()

    def create_mode_menu(self):
        menu = QMenu(self)

        nuggynet_action = menu.addAction("Nuggynet")
        nuggynet_action.triggered.connect(self.set_nuggynet_mode)

        social_chirp_action = menu.addAction("Chirp (Beta)")
        social_chirp_action.triggered.connect(self.set_chirp_mode)

        video_nugget_action = menu.addAction("Media Player (WIP)")
        video_nugget_action.setEnabled(False)

        return menu

    def create_options_menu(self):
        menu = QMenu(self)

        help_action = menu.addAction("Help")
        help_action.triggered.connect(self.open_help)

        personalize_action = menu.addAction("Personalize (Soon)")
        personalize_action.setEnabled(False)

        toggle_action = menu.addAction("Toggle Layout")
        toggle_action.triggered.connect(self.toggle_layout_position)

        return menu

    def open_help(self):
        help_path = os.path.join(os.path.dirname(__file__), "help.chm")
        if os.path.exists(help_path):
            subprocess.Popen(["hh.exe", help_path])
        else:
            QMessageBox.warning(self, "Help File Not Found", "The help file is missing.", QMessageBox.Ok)

    def handle_url_input(self):
        url = self.url_text_box.text()
        if url.startswith("nugget:"):
            self.handle_nugget_protocol(url)
        else:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://www." + url
            self.current_web_view().setUrl(QUrl(url))
        self.url_text_box.clear()

    def handle_nugget_protocol(self, url):
        QMessageBox.warning(self, "Nugget Protocol Error", "The requested protocol is unsupported.", QMessageBox.Ok)

    def go_back(self):
        self.current_web_view().back()

    def go_forward(self):
        self.current_web_view().forward()

    def reload_page(self):
        self.current_web_view().reload()

    def update_buttons(self):
        self.back_button.setEnabled(self.current_web_view().history().canGoBack())
        self.forward_button.setEnabled(self.current_web_view().history().canGoForward())

    def handle_chirp_url_change(self, qurl):
        if not qurl.isValid():
            QMessageBox.warning(self, "Error", "Invalid URL", QMessageBox.Ok)

    def toggle_layout_position(self):
        if self.is_url_bar_at_top:
            self.layout.removeItem(self.url_bar_layout)
            self.layout.addLayout(self.url_bar_layout)
        else:
            self.layout.removeItem(self.url_bar_layout)
            self.layout.insertLayout(0, self.url_bar_layout)
        self.is_url_bar_at_top = not self.is_url_bar_at_top

    def set_nuggynet_mode(self):
        self.web_stack.setCurrentWidget(self.nuggynet_view)
        self.url_text_box.setEnabled(True)
        self.url_text_box.setPlaceholderText("Enter URL")

    def set_chirp_mode(self):
        self.web_stack.setCurrentWidget(self.chirp_view)
        self.url_text_box.setEnabled(False)
        self.url_text_box.setPlaceholderText("Chirp doesn't support Search yet")

    def current_web_view(self):
        return self.web_stack.currentWidget()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
