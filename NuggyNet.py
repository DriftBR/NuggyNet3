import sys
import os
import subprocess
from PyQt5.QtCore import QUrl, Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QMenu, QMessageBox, QStackedWidget
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.default_background_color = QColor("#202020")
        palette = self.main_widget.palette()
        palette.setColor(QPalette.Window, self.default_background_color)
        self.main_widget.setPalette(palette)
        self.main_widget.setAutoFillBackground(True)

        # Create the stacked widget to handle multiple web views (for different modes)
        self.web_stack = QStackedWidget()
        self.layout.addWidget(self.web_stack)

        # Web views for Nuggynet and Chirp
        self.nuggynet_view = QWebEngineView()
        self.chirp_view = QWebEngineView()

        self.web_stack.addWidget(self.nuggynet_view)
        self.web_stack.addWidget(self.chirp_view)

        # Default mode is Nuggynet
        self.current_mode = "Nuggynet"
        self.web_stack.setCurrentWidget(self.nuggynet_view)

        # URL bar layout and controls
        self.url_bar_layout = QHBoxLayout()
        self.is_url_bar_at_top = True  # Flag to track URL bar position
        self.layout.addLayout(self.url_bar_layout)

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

        self.back_button = QPushButton()
        self.back_button.setFixedSize(32, 32)
        self.back_button.setFont(QFont("Segoe MDL2 Assets", 16))
        self.back_button.setText("")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setStyleSheet(button_style)
        self.url_bar_layout.addWidget(self.back_button)

        self.forward_button = QPushButton()
        self.forward_button.setFixedSize(32, 32)
        self.forward_button.setFont(QFont("Segoe MDL2 Assets", 16))
        self.forward_button.setText("")
        self.forward_button.clicked.connect(self.go_forward)
        self.forward_button.setStyleSheet(button_style)
        self.url_bar_layout.addWidget(self.forward_button)

        self.refresh_button = QPushButton()
        self.refresh_button.setFixedSize(32, 32)
        self.refresh_button.setFont(QFont("Segoe MDL2 Assets", 16))
        self.refresh_button.setText("")
        self.refresh_button.clicked.connect(self.reload_page)
        self.refresh_button.setStyleSheet(button_style)
        self.url_bar_layout.addWidget(self.refresh_button)

        self.url_text_box = QLineEdit()
        self.url_text_box.setPlaceholderText("Enter URL")
        self.url_text_box.setFixedHeight(32)
        self.url_text_box.setFont(QFont("Segoe UI", 14))
        self.url_text_box.returnPressed.connect(self.handle_url_input)
        self.url_bar_layout.addWidget(self.url_text_box)

        self.switch_button = QPushButton()
        self.switch_button.setFixedSize(50, 32)
        self.switch_button.setFont(QFont("Segoe MDL2 Assets", 16))
        self.switch_button.setText("")
        self.switch_button.setMenu(self.create_mode_menu())
        self.switch_button.setStyleSheet(button_style)
        self.url_bar_layout.addWidget(self.switch_button)

        # New menu for Help and Settings
        self.options_button = QPushButton()
        self.options_button.setFixedSize(50, 32)
        self.options_button.setFont(QFont("Segoe MDL2 Assets", 16))
        self.options_button.setText("")
        self.options_button.setMenu(self.create_options_menu())
        self.options_button.setStyleSheet(button_style)
        self.url_bar_layout.addWidget(self.options_button)

        self.setWindowTitle("Nuggynet")
        self.setMinimumSize(1400, 700)

        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.nuggynet_view.setUrl(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "nwin.html")))
        self.chirp_view.setUrl(QUrl("https://beta.chirpsocial.net"))

        # Signal connections for Nuggynet view
        self.nuggynet_view.urlChanged.connect(self.update_buttons)
        self.chirp_view.urlChanged.connect(self.handle_chirp_url_change)

        self.update_buttons()  # Initial check for button states

    def create_mode_menu(self):
        # Create the menu for switching modes
        menu = QMenu(self)

        nuggynet_action = menu.addAction("Nuggynet")
        nuggynet_action.setEnabled(True)
        nuggynet_action.triggered.connect(self.set_nuggynet_mode)

        social_chirp_action = menu.addAction("Social (Chirp)")
        social_chirp_action.setEnabled(True)
        social_chirp_action.triggered.connect(self.set_chirp_mode)

        video_nugget_action = menu.addAction("Media Player (WIP)")
        video_nugget_action.setEnabled(False)  # Greyed out

        return menu

    def create_options_menu(self):
        # Create the options menu for help and settings
        menu = QMenu(self)

        help_action = menu.addAction("Help")
        help_action.setEnabled(True)
        help_action.triggered.connect(self.open_help)

        settings_action = menu.addAction("Settings (Soon)")
        settings_action.setEnabled(False)  # Greyed out

        personalize_action = menu.addAction("Personalize (Soon)")
        personalize_action.setEnabled(False)  # Greyed out

        toggle_action = menu.addAction("Toggle Layout")
        toggle_action.setEnabled(True)
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
        self.url_text_box.clear()  # Clear the URL text box

    def handle_nugget_protocol(self, url):
        if url == "nugget:chirp":
            self.set_chirp_mode()
        elif url == "nugget:about":
            about_path = QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "about.html"))
            self.current_web_view().setUrl(about_path)
        else:
            self.show_invalid_protocol_dialog(url)

    def show_invalid_protocol_dialog(self, url):
        protocol = url.split(":")[1]  # Get the protocol part after 'nugget:'
        error_dialog = QMessageBox(self)
        error_dialog.setWindowTitle("Invalid Protocol")
        error_dialog.setText(f"'{protocol}' isn't a valid nugget link")
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.exec_()

    def go_back(self):
        self.current_web_view().back()

    def go_forward(self):
        self.current_web_view().forward()

    def reload_page(self):
        self.current_web_view().reload()

    def current_web_view(self):
        # Return the current web view based on the mode
        if self.current_mode == "Nuggynet":
            return self.nuggynet_view
        elif self.current_mode == "Chirp":
            return self.chirp_view

    def update_buttons(self):
        # Disable back button if no history available
        self.back_button.setEnabled(self.current_web_view().history().canGoBack())
        # Disable forward button if no forward history available
        self.forward_button.setEnabled(self.current_web_view().history().canGoForward())

        # Update URL bar state based on the current mode
        self.update_url_bar()

        # Keep title bar as "Nuggynet"
        self.setWindowTitle("Nuggynet")

        self.current_web_view().page().runJavaScript(
            """
            (function() {
                let title = document.title;
                return title;
            })();
            """,
            self.handle_page_title_change
        )

    def handle_page_title_change(self, title):
        if title != "":
            self.setWindowTitle("Nuggynet - " + title)
        else:
            self.setWindowTitle("Nuggynet")

    def handle_chirp_url_change(self, url):
        self.update_buttons()

    def update_url_bar(self):
        if self.current_mode == "Chirp":
            # Disable the URL bar and set a placeholder text
            self.url_text_box.setEnabled(False)
            self.url_text_box.setPlaceholderText("Chirp hasn't added Search yet")
        else:
            # Enable the URL bar and set the placeholder text
            self.url_text_box.setEnabled(True)
            self.url_text_box.setPlaceholderText("Enter URL")

    def set_nuggynet_mode(self):
        self.current_mode = "Nuggynet"
        self.web_stack.setCurrentWidget(self.nuggynet_view)
        self.update_buttons()

    def set_chirp_mode(self):
        self.current_mode = "Chirp"
        self.web_stack.setCurrentWidget(self.chirp_view)
        self.update_buttons()

    def toggle_layout_position(self):
        self.is_url_bar_at_top = not self.is_url_bar_at_top
        self.layout.removeItem(self.url_bar_layout)
        if self.is_url_bar_at_top:
            self.layout.insertLayout(0, self.url_bar_layout)
        else:
            self.layout.addLayout(self.url_bar_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Disable custom dragging
            pass

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # Disable custom resizing
            pass

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Disable custom resizing logic
            pass

    def keyPressEvent(self, event):
        # Example key press event
        if event.key() == Qt.Key_F5:
            self.reload_page()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
