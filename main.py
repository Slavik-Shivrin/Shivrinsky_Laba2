"""
Главный файл для запуска программы
Интерактивный интерфейс для работы с IPv6 адресами
"""

import argparse
import os
from ipv6_checker import IPv6Checker


def print_banner():
    """Вывод приветственного баннера"""
    print("=" * 60)
    print("    ПРОВЕРКА И ПОИСК IPv6 АДРЕСОВ")
    print("=" * 60)


def interactive_mode(checker):
    """
    Интерактивный режим работы

    Args:
        checker: объект IPv6Checker
    """
    print("\n📱 ИНТЕРАКТИВНЫЙ РЕЖИМ")
    print("Команды:")
    print("  - Введите текст для поиска IPv6")
    print("  - 'file <путь>' - поиск в файле")
    print("  - 'url <адрес>' - поиск на веб-странице")
    print("  - 'quit' или 'exit' - выход")
    print("-" * 40)

    while True:
        try:
            user_input = input("\n>>> ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("До свидания!")
                break

            # Проверка команд
            if user_input.startswith('file '):
                filepath = user_input[5:].strip()
                results = checker.find_ipv6_in_file(filepath)
                print_results(results, "файле")

            elif user_input.startswith('url '):
                url = user_input[4:].strip()
                results = checker.find_ipv6_in_url(url)
                print_results(results, "URL")

            else:
                # Обычный поиск в тексте
                if checker.is_valid_ipv6(user_input):
                    print(f"✅ '{user_input}' - валидный IPv6 адрес")
                else:
                    found = checker.find_ipv6(user_input)
                    if found:
                        print_results(found, "тексте")
                    else:
                        print(f"❌ '{user_input}' - не IPv6 адрес")

        except KeyboardInterrupt:
            print("\nВыход по Ctrl+C")
            break
        except Exception as e:
            print(f"Ошибка: {e}")


def print_results(results, source_type):
    """
    Вывод результатов поиска

    Args:
        results: список найденных адресов
        source_type: тип источника
    """
    if results:
        print(f"\n✅ Найдено IPv6 адресов в {source_type}: {len(results)}")
        for i, ip in enumerate(results, 1):
            print(f"  {i}. {ip}")
    else:
        print(f"\n❌ IPv6 адреса в {source_type} не найдены")


def save_results(results, filename):
    """
    Сохранение результатов в файл

    Args:
        results: список адресов
        filename: имя файла
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for ip in set(results):  # Убираем дубликаты
                f.write(ip + '\n')
        print(f"✅ Результаты сохранены в {os.path.abspath(filename)}")
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")


def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description='Поиск и проверка IPv6 адресов',
        epilog='Примеры: python main.py 2001:db8::1'
    )

    parser.add_argument(
        'source',
        nargs='?',
        help='Строка для проверки'
    )

    parser.add_argument(
        '-f', '--file',
        help='Поиск в файле'
    )

    parser.add_argument(
        '-u', '--url',
        help='Поиск на веб-странице'
    )

    parser.add_argument(
        '-o', '--output',
        help='Файл для сохранения результатов'
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Интерактивный режим'
    )

    args = parser.parse_args()

    # Создаем объект для проверки
    checker = IPv6Checker()

    print_banner()

    all_results = []

    # Интерактивный режим
    if args.interactive or not any([args.source, args.file, args.url]):
        interactive_mode(checker)
        return

    # Проверка отдельной строки
    if args.source:
        print(f"\n🔍 Проверка строки: '{args.source}'")
        if checker.is_valid_ipv6(args.source):
            print(f"✅ Это валидный IPv6 адрес")
            all_results.append(args.source)
        else:
            found = checker.find_ipv6(args.source)
            if found:
                print_results(found, "строке")
                all_results.extend(found)
            else:
                print(f"❌ Это не IPv6 адрес")

    # Поиск в файле
    if args.file:
        print(f"\n📄 Поиск в файле: {args.file}")
        file_results = checker.find_ipv6_in_file(args.file)
        print_results(file_results, "файле")
        all_results.extend(file_results)

    # Поиск на веб-странице
    if args.url:
        print(f"\n🌐 Поиск на странице: {args.url}")
        url_results = checker.find_ipv6_in_url(args.url)
        print_results(url_results, "URL")
        all_results.extend(url_results)

    # Сохранение результатов
    if args.output and all_results:
        save_results(all_results, args.output)

    # Итог
    if all_results:
        print(f"\n📊 Всего найдено уникальных адресов: {len(set(all_results))}")


if __name__ == '__main__':
    main()