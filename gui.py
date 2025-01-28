import os
import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QFileDialog, QLineEdit, QListWidget, QRadioButton, QSpinBox, QComboBox,
    QCheckBox, QGridLayout, QMessageBox, QStatusBar, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QThreadPool, QLocale, QTranslator, QDir
from PyQt6.QtGui import QIcon

from ustx_harms import get_ustx_data, get_track_names, key_names
from worker import HarmonyGeneratorWorker

class HarmonyGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USTx Auto Harmony Generator") 
        self.setGeometry(100, 100, 600, 500)

        self.threadpool = QThreadPool()
        self.translator = QTranslator()
        self.current_locale = "en_US"

        self.init_ui()
        self.load_language(self.current_locale)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        language_menu = menubar.addMenu(self.tr("&Language"))

        ru_action = language_menu.addAction(self.tr("Русский"))
        ru_action.triggered.connect(lambda: self.load_language("ru_RU"))

        en_action = language_menu.addAction(self.tr("English"))
        en_action.triggered.connect(lambda: self.load_language("en_US"))

        jp_action = language_menu.addAction(self.tr("日本語"))
        jp_action.triggered.connect(lambda: self.load_language("ja_JP"))

        file_frame_layout = QGridLayout()
        file_frame = QWidget()
        file_frame.setLayout(file_frame_layout)

        file_label = QLabel(self.tr("USTx File:"))
        file_frame_layout.addWidget(file_label, 0, 0, 1, 1)

        self.ustx_file_entry = QLineEdit()
        file_frame_layout.addWidget(self.ustx_file_entry, 0, 1, 1, 2)

        browse_ustx_button = QPushButton(self.tr("Browse"))
        browse_ustx_button.clicked.connect(self.browse_ustx_file)
        file_frame_layout.addWidget(browse_ustx_button, 0, 3, 1, 1)

        output_label = QLabel(self.tr("Save As:"))
        file_frame_layout.addWidget(output_label, 1, 0, 1, 1)

        self.output_file_entry = QLineEdit()
        file_frame_layout.addWidget(self.output_file_entry, 1, 1, 1, 2)

        browse_output_button = QPushButton(self.tr("Browse"))
        browse_output_button.clicked.connect(self.browse_output_file)
        file_frame_layout.addWidget(browse_output_button, 1, 3, 1, 1)

        layout.addWidget(file_frame)

        track_frame_layout = QGridLayout()
        track_frame = QWidget()
        track_frame.setLayout(track_frame_layout)

        track_label = QLabel(self.tr("Select Tracks:"))
        track_frame_layout.addWidget(track_label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop)

        self.track_listbox = QListWidget()
        self.track_listbox.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        track_frame_layout.addWidget(self.track_listbox, 0, 1, 3, 1)

        harmony_label = QLabel(self.tr("Harmony Type:"))
        track_frame_layout.addWidget(harmony_label, 0, 2, 1, 1)

        self.harmony_type_radio_lower = QRadioButton(self.tr("Lower"))
        self.harmony_type_radio_upper = QRadioButton(self.tr("Upper"))
        self.harmony_type_radio_both = QRadioButton(self.tr("Both"))
        self.harmony_type_radio_lower.setChecked(True)
        track_frame_layout.addWidget(self.harmony_type_radio_lower, 1, 2, 1, 1)
        track_frame_layout.addWidget(self.harmony_type_radio_upper, 2, 2, 1, 1)
        track_frame_layout.addWidget(self.harmony_type_radio_both, 3, 2, 1, 1)

        interval_label = QLabel(self.tr("Interval (semitones):"))
        track_frame_layout.addWidget(interval_label, 4, 0, 1, 1)

        self.semitone_interval_spinbox = QSpinBox()
        self.semitone_interval_spinbox.setRange(-12, 12)
        self.semitone_interval_spinbox.setValue(3)
        track_frame_layout.addWidget(self.semitone_interval_spinbox, 4, 1, 1, 1)

        layout.addWidget(track_frame)

        key_frame_layout = QGridLayout()
        key_frame = QWidget()
        key_frame.setLayout(key_frame_layout)

        self.manual_key_checkbox = QCheckBox(self.tr("Manual Key Selection"))
        self.manual_key_checkbox.stateChanged.connect(self.toggle_key_selection)
        key_frame_layout.addWidget(self.manual_key_checkbox, 0, 0, 1, 2)

        key_label = QLabel(self.tr("Key:"))
        key_frame_layout.addWidget(key_label, 1, 0, 1, 1)

        self.key_name_combobox = QComboBox()
        self.key_name_combobox.addItems(key_names)
        self.key_name_combobox.setCurrentIndex(0)
        self.key_name_combobox.setEnabled(False)
        key_frame_layout.addWidget(self.key_name_combobox, 1, 1, 1, 1)

        mode_label = QLabel(self.tr("Mode"))
        key_frame_layout.addWidget(mode_label, 2, 0, 1, 1)

        self.key_mode_combobox = QComboBox()
        self.key_mode_combobox.addItems(["major", "minor"])
        self.key_mode_combobox.setCurrentIndex(0)
        self.key_mode_combobox.setEnabled(False)
        key_frame_layout.addWidget(self.key_mode_combobox, 2, 1, 1, 1)

        layout.addWidget(key_frame)

        self.generate_button = QPushButton(self.tr("Generate Harmonies"))
        self.generate_button.clicked.connect(self.start_harmony_generation)
        layout.addWidget(self.generate_button)

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar_label = QLabel(self.tr("Ready"))
        self.status_bar.addWidget(self.status_bar_label)


    def browse_ustx_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.tr("Select USTx File"), "", self.tr("USTx Files (*.ustx);;All Files (*.*)"))
        if file_path:
            self.ustx_file_entry.setText(file_path)
            self.load_track_names(file_path)

    def browse_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, self.tr("Save Harmony USTx File"), "", self.tr("USTx Files (*.ustx);;All Files (*.*)"))
        if file_path:
            self.output_file_entry.setText(file_path)

    def load_track_names(self, ustx_file_path):
        ustx_data, error_msg = get_ustx_data(ustx_file_path)
        if error_msg:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Error loading USTx file:\n") + error_msg)
            return

        track_names = get_track_names(ustx_data)
        self.track_listbox.clear()
        self.track_listbox.addItems(track_names)

    def toggle_key_selection(self, state):
        self.key_name_combobox.setEnabled(state == Qt.CheckState.Checked.value)
        self.key_mode_combobox.setEnabled(state == Qt.CheckState.Checked.value)

    def start_harmony_generation(self):
        print("Starting harmony generation.")
        ustx_file_path = self.ustx_file_entry.text()
        output_file_path = self.output_file_entry.text()

        if not ustx_file_path:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("Please select a USTx file."))
            return
        if not output_file_path:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("Please select an output file path."))
            return

        selected_track_indices = [self.track_listbox.row(item) for item in self.track_listbox.selectedItems()]
        if not selected_track_indices:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("Please select at least one track."))
            return

        harmony_type = 1
        if self.harmony_type_radio_upper.isChecked():
            harmony_type = 2
        elif self.harmony_type_radio_both.isChecked():
            harmony_type = 3

        semitone_interval = self.semitone_interval_spinbox.value()
        manual_key_selection = self.manual_key_checkbox.isChecked()
        key_name = self.key_name_combobox.currentText()
        key_mode = self.key_mode_combobox.currentText()

        worker = HarmonyGeneratorWorker(
            ustx_file_path, output_file_path, selected_track_indices, harmony_type,
            semitone_interval, manual_key_selection, key_name, key_mode
        )
        self.status_bar_label.setText(self.tr("Generating harmonies..."))
        self.threadpool.start(worker) 
        self.status_bar_label.setText(self.tr("Ready")) 


    def generation_finished(self, message):
        if "Error" in message or "YAMLError" in message or "FileNotFoundError" in message or "Invalid key" in message:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Harmony Generation Error:\n") + message)
            self.status_bar_label.setText(self.tr("Error during harmony generation"))
        else:
            QMessageBox.information(self, self.tr("Success"), self.tr(message))
            self.status_bar_label.setText(self.tr("Harmony generation complete"))

    def load_language(self, locale_code):
        app = QApplication.instance()
        if self.translator:
            app.removeTranslator(self.translator)
        if locale_code != "en_US":
            path = QDir.currentPath()
            translation_file = f"{locale_code}.qm"
            if self.translator.load(os.path.join(path, "i18n", translation_file)):
                app.installTranslator(self.translator)
                self.current_locale = locale_code
                self.retranslate_ui()
            else:
                QMessageBox.warning(self, "Warning", f"Translation file not found for locale: {locale_code}. Using default language.")
                self.current_locale = "en_US"
        else:
            self.current_locale = "en_US"
            self.retranslate_ui()

    def retranslate_ui(self):
        print("Retranslating UI...")

        self.setWindowTitle(self.tr("USTx Auto Harmony Generator"))
        self.menuBar().clear()
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)
        language_menu = menubar.addMenu(self.tr("&Language"))
        ru_action = language_menu.addAction(self.tr("Русский"))
        ru_action.triggered.connect(lambda: self.load_language("ru_RU"))
        en_action = language_menu.addAction(self.tr("English"))
        en_action.triggered.connect(lambda: self.load_language("en_US"))
        jp_action = language_menu.addAction(self.tr("日本語"))
        jp_action.triggered.connect(lambda: self.load_language("ja_JP"))

        file_frame = self.centralWidget().findChild(QWidget)
        file_label = file_frame.findChild(QLabel)
        file_label.setText(self.tr("USTx File:"))
        browse_ustx_button = file_frame.findChild(QPushButton)
        browse_ustx_button.setText(self.tr("Browse"))
        output_label = file_frame.findChild(QLabel)
        output_label.setText(self.tr("Save As:"))
        browse_output_button = file_frame.findChild(QPushButton)
        browse_output_button.setText(self.tr("Browse"))

        track_frame = self.centralWidget().findChild(QWidget)
        track_label = track_frame.findChild(QLabel)
        track_label.setText(self.tr("Select Tracks:"))
        harmony_label = track_frame.findChild(QLabel)
        harmony_label.setText(self.tr("Harmony Type:"))
        self.harmony_type_radio_lower.setText(self.tr("Lower"))
        self.harmony_type_radio_upper.setText(self.tr("Upper"))
        self.harmony_type_radio_both.setText(self.tr("Both"))
        interval_label = track_frame.findChild(QLabel)
        interval_label.setText(self.tr("Interval (semitones):"))

        key_frame = self.centralWidget().findChild(QWidget)
        manual_key_checkbox = key_frame.findChild(QCheckBox)
        if manual_key_checkbox:
            manual_key_checkbox.setText(self.tr("Manual Key Selection"))
        key_label = key_frame.findChild(QLabel)
        key_label.setText(self.tr("Key:"))
        mode_label = key_frame.findChild(QLabel)
        mode_label.setText(self.tr("Mode:"))

        self.generate_button.setText(self.tr("Generate Harmonies"))
        self.status_bar_label.setText(self.tr("Ready"))