import argparse
import mimetypes
import os


def main():
    # Tworzymy parser argumentów
    parser = argparse.ArgumentParser(description='Prosty program do wyświetlania informacji o pliku.')

    # Dodajemy argument, który pozwala na podanie ścieżki do pliku
    parser.add_argument('filename', type=str, help='Ścieżka do pliku do przetworzenia')

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

    # Odczytujemy i wyświetlamy zawartość pliku
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print(f"Zawartość pliku:\n{content}")
    except Exception as e:
        print(f"Nie udało się odczytać pliku {filename}: {e}")


if __name__ == "__main__":
    main()
