"""
Класс для проверки и поиска IPv6 адресов
Без использования внешних библиотек
"""

import re
import urllib.request
import urllib.error
import socket
from regex_patterns import IPV6_PATTERN


class IPv6Checker:
    """Класс для проверки и поиска IPv6 адресов"""

    def __init__(self, pattern=IPV6_PATTERN):
        """
        Инициализация класса

        Args:
            pattern: Регулярное выражение для поиска IPv6
        """
        self.pattern = pattern
        print(f"✓ IPv6Checker инициализирован")

    def is_valid_ipv6(self, ip_string):
        """
        Проверка, является ли строка валидным IPv6 адресом

        Args:
            ip_string: Строка для проверки

        Returns:
            bool: True если строка - валидный IPv6
        """
        if not ip_string or not isinstance(ip_string, str):
            return False

        # Удаляем пробелы в начале и конце
        ip_string = ip_string.strip()

        # Полное совпадение всей строки
        return bool(self.pattern.fullmatch(ip_string))

    def find_ipv6(self, text):
        """
        Поиск всех IPv6 адресов в тексте

        Args:
            text: Текст для поиска

        Returns:
            list: Список найденных IPv6 адресов
        """
        if not text:
            return []

        # Поиск всех совпадений
        return [match.group() for match in self.pattern.finditer(text)]

    def find_ipv6_in_file(self, filepath):
        """
        Поиск IPv6 адресов в файле

        Args:
            filepath: Путь к файлу

        Returns:
            list: Список найденных IPv6 адресов
        """
        try:
            # Пробуем разные кодировки
            encodings = ['utf-8', 'cp1251', 'latin-1', 'windows-1251']

            for encoding in encodings:
                try:
                    with open(filepath, 'r', encoding=encoding) as file:
                        content = file.read()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                print("❌ Не удалось прочитать файл")
                return []

            return self.find_ipv6(content)

        except FileNotFoundError:
            print(f"❌ Файл {filepath} не найден")
            return []
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return []

    def find_ipv6_in_url(self, url):
        """
        Поиск IPv6 адресов на веб-странице используя встроенную библиотеку urllib

        Args:
            url: URL страницы

        Returns:
            list: Список найденных IPv6 адресов
        """
        try:
            # Добавляем протокол, если его нет
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url

            # Создаем запрос
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )

            # Выполняем запрос
            with urllib.request.urlopen(req, timeout=10) as response:
                html_content = response.read().decode('utf-8', errors='ignore')

            return self.find_ipv6(html_content)

        except Exception as e:
            print(f"❌ Ошибка загрузки {url}: {e}")
            return []

    @staticmethod
    def normalize_ipv6(ip):
        """
        Нормализация IPv6 адреса

        Args:
            ip: IPv6 адрес

        Returns:
            str: Нормализованный адрес
        """
        try:
            import ipaddress
            return str(ipaddress.ip_address(ip))
        except:
            return ip