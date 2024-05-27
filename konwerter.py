import argparse
import mimetypes
import os
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
    root = ET.Element("data")
    _dict_to_xml(data, root)
    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)
    print(f"Dane zostały zapisane do pliku {filename} w formacie XML")


def _dict_to_xml(data, parent):
    for key, value in data.items():
        if isinstance(value, dict):
            _dict_to_xml(value, ET.SubElement(parent, key))
        elif isinstance(value, list):
            for item in value:
                _dict_to_xml(item, ET.SubElement(parent, key))
        else:
            ET.SubElement(parent, key).text = str(value)


def main():
    # Tworzymy parser argumentów
    parser = argparse.ArgumentParser(
        description='Prosty program do wyświetlania i zapisywania informacji o plikach JSON, YAML i XML.')

    # Dodajemy argumenty, które pozwalają na podanie ścieżki do pliku wejściowego, ścieżki do pliku wyjściowego oraz formatu wyjściowego
    parser.add_argument('filename', type=str, help='Ścieżka do pliku do przetworzenia')
    parser.add_argument('-o', '--output', type=str, help='Ścieżka do pliku wyjściowego')
    parser.add_argument('-f', '--format', type=str, choices=['json', 'yaml', 'xml'],
                        help='Format pliku wyjściowego (json, yaml lub xml)')

    # Parsujemy argumenty
    args = parser.parse_args()

    # Odczytujemy nazwę pliku
    filename = args.filename

    # Sprawdzamy, czy plik istnieje
    if not os.path.isfile(filename):
        print(f"Plik {filename} nie został znaleziony.")
        return

    # Wyświetlamy nazwę pliku
    print(f"Nazwa pliku: {os.path.basename(filename)}")

    # Określamy rodzaj pliku
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type is None:
        # Jeżeli mime_type nie jest rozpoznane, próbujemy sprawdzić po rozszerzeniu pliku
        if filename.endswith('.json'):
            mime_type = 'application/json'
        elif filename.endswith('.yaml') or filename.endswith('.yml'):
            mime_type = 'application/x-yaml'
        elif filename.endswith('.xml'):
            mime_type = 'application/xml'
        else:
            mime_type = 'Nieznany'

    print(f"Rodzaj pliku: {mime_type}")

    # Ładujemy zawartość pliku i weryfikujemy jego poprawność składniową
    try:
        if mime_type == 'application/json':
            data = load_json(filename)
        elif mime_type == 'application/x-yaml':
            data = load_yaml(filename)
        elif mime_type == 'application/xml':
            data = load_xml(filename)
        else:
            print(f"Plik {filename} nie jest obsługiwanym typem pliku (JSON, YAML lub XML).")
            return

        # Jeśli podano ścieżkę do pliku wyjściowego, zapisujemy dane do tego pliku w odpowiednim formacie
        if args.output:
            if not args.format:
                print("Proszę podać format wyjściowy za pomocą opcji -f lub --format (json, yaml lub xml).")
                return

            try:
                if args.format == 'json':
                    save_json(data, args.output)
                elif args.format == 'yaml':
                    save_yaml(data, args.output)
                elif args.format == 'xml' and isinstance(data, ET.ElementTree):
                    save_xml(data, args.output)
                else:
                    print(f"Nieprawidłowy format danych do zapisania w formacie {args.format}")
            except Exception as e:
                print(f"Nie udało się zapisać danych do pliku {args.output}: {e}")
    except (json.JSONDecodeError, yaml.YAMLError, ET.ParseError) as e:
        print(f"Nie udało się odczytać pliku {filename}: Błąd składni - {e}")
    except Exception as e:
        print(f"Nie udało się odczytać pliku {filename}: {e}")


if __name__ == "__main__":
    main()
