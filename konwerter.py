import argparse
import mimetypes
import os
import json


def main():
    # Tworzymy parser argumentów
    parser = argparse.ArgumentParser(
        description='Prosty program do wyświetlania i zapisywania informacji o pliku JSON.')

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
        mime_type = 'Nieznany'
    print(f"Rodzaj pliku: {mime_type}")

    # Sprawdzamy, czy plik jest typu JSON
    if mime_type != 'application/json':
        print(f"Plik {filename} nie jest plikiem JSON.")
        return

    # Odczytujemy i weryfikujemy zawartość pliku JSON
    try:
        with open(filename, 'r') as file:
            content = file.read()
            # Próba załadowania zawartości jako JSON
            data = json.loads(content)
            print(f"Zawartość pliku JSON:\n{json.dumps(data, indent=4)}")
            print("Plik JSON jest poprawny składniowo.")

            # Jeśli podano ścieżkę do pliku wyjściowego, zapisujemy dane do tego pliku
            if args.output:
                try:
                    with open(args.output, 'w') as output_file:
                        json.dump(data, output_file, indent=4)
                    print(f"Dane zostały zapisane do pliku {args.output}")
                except Exception as e:
                    print(f"Nie udało się zapisać danych do pliku {args.output}: {e}")
    except json.JSONDecodeError as e:
        print(f"Nie udało się odczytać pliku {filename}: Błąd składni JSON - {e}")
    except Exception as e:
        print(f"Nie udało się odczytać pliku {filename}: {e}")


if __name__ == "__main__":
    main()
