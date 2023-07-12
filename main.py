import os
import sys
import pdfplumber
import pyttsx3
from PyPDF2 import PdfFileReader
from PyQt5 import QtWidgets, QtGui, QtCore

class Main_App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF to MP3 Converter")
        self.setFixedSize(500, 300)

        # Initialize Pyttsx3
        self.engine = pyttsx3.init()

        # Create GUI elements
        self.label_pdf = QtWidgets.QLabel("PDF Path:")
        self.entry_pdf = QtWidgets.QLineEdit()
        self.btn_browse_pdf = QtWidgets.QPushButton("Browse")
        self.btn_browse_pdf.clicked.connect(self.browse_pdf)

        self.label_voice = QtWidgets.QLabel("Select Voice:")
        self.voice_combobox = QtWidgets.QComboBox()
        self.voice_combobox.addItems(["Male Voice", "Female Voice"])

        self.label_start = QtWidgets.QLabel("Start Page:")
        self.entry_start = QtWidgets.QLineEdit()
        self.entry_start.setText("1")

        self.label_end = QtWidgets.QLabel("End Page:")
        self.entry_end = QtWidgets.QLineEdit()

        self.label_output_folder = QtWidgets.QLabel("Output Folder:")
        self.entry_output_folder = QtWidgets.QLineEdit()
        self.btn_browse_output = QtWidgets.QPushButton("Choose Output Folder")
        self.btn_browse_output.clicked.connect(self.browse_output_folder)

        self.btn_convert = QtWidgets.QPushButton("Convert to Audio")
        self.btn_convert.clicked.connect(self.convert_to_audio)

        # Set colors and styles
        self.setStyleSheet("background-color: #F5F5F5; color: #333333;")
        self.label_pdf.setStyleSheet("font-weight: bold;")
        self.label_voice.setStyleSheet("font-weight: bold;")
        self.label_start.setStyleSheet("font-weight: bold;")
        self.label_end.setStyleSheet("font-weight: bold;")
        self.label_output_folder.setStyleSheet("font-weight: bold;")
        self.btn_convert.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        
        # Create layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.label_pdf, 0, 0)
        layout.addWidget(self.entry_pdf, 0, 1)
        layout.addWidget(self.btn_browse_pdf, 0, 2)
        layout.addWidget(self.label_voice, 1, 0)
        layout.addWidget(self.voice_combobox, 1, 1)
        layout.addWidget(self.label_start, 2, 0)
        layout.addWidget(self.entry_start, 2, 1)
        layout.addWidget(self.label_end, 3, 0)
        layout.addWidget(self.entry_end, 3, 1)
        layout.addWidget(self.label_output_folder, 4, 0)
        layout.addWidget(self.entry_output_folder, 4, 1)
        layout.addWidget(self.btn_browse_output, 4, 2)
        layout.addWidget(self.btn_convert, 5, 0, 1, 3)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(layout)

    def browse_pdf(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            self.entry_pdf.setText(file_path)

    

    def browse_output_folder(self):
        file_dialog = QtWidgets.QFileDialog()
        folder_path = file_dialog.getExistingDirectory(self, "Select Output Folder")
        if folder_path:
            self.entry_output_folder.setText(folder_path)
        else:
            # Show error message if no folder selected
            QtWidgets.QMessageBox.warning(
            self, "Error", "No output folder selected."
            )



    def convert_to_audio(self):
        pdf_path = self.entry_pdf.text()
        start_page_text = self.entry_start.text()
        end_page_text = self.entry_end.text()
        voice_id = self.voice_combobox.currentIndex()
        output_folder = self.entry_output_folder.text()

        self.engine.setProperty('voice', self.engine.getProperty('voices')[voice_id].id)

        try:
            if not pdf_path:
                raise ValueError("Please provide a PDF file path.")
            if not os.path.isfile(pdf_path):
                raise FileNotFoundError("PDF file not found.")
            if not output_folder:
                raise ValueError("Please provide an output folder.")
            if not os.path.isdir(output_folder):
                raise NotADirectoryError("Output folder not found.")

            if not start_page_text:
                raise ValueError("Please provide a start page.")
            if not end_page_text:
                raise ValueError("Please provide an end page.")

            start_page = int(start_page_text) - 1  # Subtract 1 to convert to 0-based indexing
            end_page = int(end_page_text)  # No need to subtract 1 for end page

            base_name = os.path.splitext(os.path.basename(pdf_path))[0]  # Extract the base name of the PDF file
            output_file = os.path.join(output_folder, f"{base_name}_audio.mp3")  # Create the output file path

            with pdfplumber.open(pdf_path) as pdf:
                num_pages = len(pdf.pages)
                
                if start_page > num_pages or end_page > num_pages:
                    raise ValueError("Invalid start or end page number.")

                text = ""
                for i in range(start_page, end_page):
                    page = pdf.pages[i]
                    text += page.extract_text()

                self.engine.save_to_file(text, output_file)
                self.engine.runAndWait()

                # Show success message
                QtWidgets.QMessageBox.information(
                    self, "Conversion Complete", "PDF converted to MP3 successfully."
                )

                # Clear input fields after successful conversion
                self.entry_pdf.clear()
                self.entry_start.clear()
                self.entry_end.clear()
                self.entry_output_folder.clear()

        except Exception as e:
            # Show error message
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def closeEvent(self, event):
        self.engine.stop()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

        # Set application style
    app.setStyle("Fusion")
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#FFFFFF"))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor("#333333"))
    app.setPalette(palette)

    window = Main_App()
    window.show()
    app.exec_()

