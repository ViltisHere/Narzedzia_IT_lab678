import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, \
    QComboBox, QLineEdit
import json
import yaml
import xml.etree.ElementTree as ET


def load_json(filename):
    with open(filename, 'r') as file:
        content = file.read()
        data = json.loads(content)
        print(f"Zawartość pliku JSON:\n{json.dumps(data, indent=4)}")
        print("Plik JSON jest poprawny składniowo.")
        return data


def load_yaml(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
        print(f"Zawartość pliku YAML:\n{yaml.dump(data, default_flow_style=False)}")
        print("Plik YAML jest poprawny składniowo.")
        return data


def load_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    data = ET.tostring(root, encoding='unicode')
    print(f"Zawartość pliku XML:\n{data}")
    print("Plik XML jest poprawny składniowo.")
    return tree


def save_json(data, filename):
    with open(filename, 'w') as output_file:
        json.dump(data, output_file, indent=4)
    print(f"Dane zostały zapisane do pliku {filename} w formacie JSON")


def save_yaml(data, filename):
    with open(filename, 'w') as output_file:
        yaml.dump(data, output_file, default_flow_style=False)
    print(f"Dane zostały zapisane do pliku {filename} w formacie YAML")


def save_xml(data, filename):
    data.write(filename, encoding='unicode', xml_declaration=True)
    print(f"Dane zostały zapisane do pliku {filename} w formacie XML")


class Konwerter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Konwerter')
        self.setGeometry(100, 100, 400, 200)

        self.file_label = QLabel('Plik wejściowy:')
        self.file_path = QLineEdit()
        self.browse_button = QPushButton('Przeglądaj')
        self.browse_button.clicked.connect(self.browseFile)

        self.format_label = QLabel('Format wyjściowy:')
        self.format_combo = QComboBox()
        self.format_combo.addItems(['json', 'yaml', 'xml'])

        self.output_label = QLabel('Plik wyjściowy:')
        self.output_path = QLineEdit()
        self.output_button = QPushButton('Przeglądaj')
        self.output_button.clicked.connect(self.browseOutputFile)

        self.process_button = QPushButton('Konwertuj')
        self.process_button.clicked.connect(self.processFile)

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.file_label)
        hbox1.addWidget(self.file_path)
        hbox1.addWidget(self.browse_button)
        vbox.addLayout(hbox1)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.format_label)
        hbox2.addWidget(self.format_combo)
        vbox.addLayout(hbox2)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.output_label)
        hbox3.addWidget(self.output_path)
        hbox3.addWidget(self.output_button)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.process_button)

        self.setLayout(vbox)

    def browseFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Przeglądaj plik')
        if file_path:
            self.file_path.setText(file_path)

    def browseOutputFile(self):
        output_path, _ = QFileDialog.getSaveFileName(self, 'Zapisz plik')
        if output_path:
            self.output_path.setText(output_path)

    def processFile(self):
        input_file = self.file_path.text()
        output_file = self.output_path.text()
        output_format = self.format_combo.currentText()

        if output_format == 'json':
            loader = load_json
            saver = save_json
        elif output_format == 'yaml':
            loader = load_yaml
            saver = save_yaml
        elif output_format == 'xml':
            loader = load_xml
            saver = save_xml
        else:
            return

        data = loader(input_file)
        if data:
            saver(data, output_file)
            print("Konwersja zakończona pomyślnie.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Konwerter()
    ex.show()
    sys.exit(app.exec_())
