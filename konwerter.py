import argparse
import mimetypes
import os
import json
import yaml


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


def main():
    # Tworzymy parser argumentów
    parser = argparse.ArgumentParser(
        description='Prosty program do wyświetlania i zapisywania informacji o plikach JSON i YAML.')

    # Dodajemy argumenty, które pozwalają na podanie ścieżki do pliku wejściowego i opcjonalnie do pliku wyjściowego
    parser.add_argument('filename', type=str, help='Ścieżka do pliku do przetworzenia')
    parser.add_argument('-o', '--output', type=str, help='Ścieżka do pliku wyjściowego')

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
        else:
            mime_type = 'Nieznany'

    print(f"Rodzaj pliku: {mime_type}")

    # Ładujemy zawartość pliku i weryfikujemy jego poprawność składniową
    try:
        if mime_type == 'application/json':
            data = load_json(filename)
        elif mime_type == 'application/x-yaml':
            data = load_yaml(filename)
        else:
            print(f"Plik {filename} nie jest obsługiwanym typem pliku (JSON lub YAML).")
            return

        # Jeśli podano ścieżkę do pliku wyjściowego, zapisujemy dane do tego pliku w formacie JSON
        if args.output:
            try:
                with open(args.output, 'w') as output_file:
                    json.dump(data, output_file, indent=4)
                print(f"Dane zostały zapisane do pliku {args.output}")
            except Exception as e:
                print(f"Nie udało się zapisać danych do pliku {args.output}: {e}")
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        print(f"Nie udało się odczytać pliku {filename}: Błąd składni - {e}")
    except Exception as e:
        print(f"Nie udało się odczytać pliku {filename}: {e}")


if __name__ == "__main__":
    main()
