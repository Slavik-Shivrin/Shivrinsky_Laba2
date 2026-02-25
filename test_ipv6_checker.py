"""
Unit-тесты для проверки IPv6 адресов
"""

import unittest
import tempfile
import os
from ipv6_checker import IPv6Checker


class TestIPv6Checker(unittest.TestCase):
    """Класс с тестами"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.checker = IPv6Checker()
        print(f"\nЗапуск теста: {self._testMethodName}")

    def tearDown(self):
        """Очистка после каждого теста"""
        print(f"Тест завершен: {self._testMethodName}")

    def test_valid_ipv6_addresses(self):
        """Тест 1: Проверка валидных IPv6 адресов"""
        valid_ips = [
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            "2001:db8:85a3:0:0:8a2e:370:7334",
            "2001:db8:85a3::8a2e:370:7334",
            "::1",
            "::",
            "2001:db8::",
            "fe80::1",
            "fe80::1%eth0",
            "::ffff:192.0.2.128",
        ]

        for ip in valid_ips:
            with self.subTest(ip=ip):
                self.assertTrue(
                    self.checker.is_valid_ipv6(ip),
                    f"Ошибка: '{ip}' должен быть валидным"
                )

    def test_invalid_ipv6_addresses(self):
        """Тест 2: Проверка невалидных IPv6 адресов"""
        invalid_ips = [
            "",
            "   ",
            "192.168.1.1",
            "2001:db8:::1",
            "gggg:db8::1",
            "2001:db8::12345",
            "fe80::1%",
            "::ffff:256.0.2.128",
            "not an ip",
            "2001:db8:85a3::8a2e:370:7334:extra",
        ]

        for ip in invalid_ips:
            with self.subTest(ip=ip):
                self.assertFalse(
                    self.checker.is_valid_ipv6(ip),
                    f"Ошибка: '{ip}' не должен быть валидным"
                )

    def test_find_in_text(self):
        """Тест 3: Поиск IPv6 в тексте"""
        text = """
        Здесь есть несколько адресов:
        2001:db8::1 - это localhost
        fe80::1%eth0 - link-local
        А также 2001:0db8:85a3:0000:0000:8a2e:0370:7334
        И невалидный 2001:db8:::1 должен игнорироваться.
        """

        found = self.checker.find_ipv6(text)
        expected_count = 3

        self.assertEqual(
            len(found),
            expected_count,
            f"Найдено {len(found)}, ожидалось {expected_count}"
        )

        # Проверяем, что все ожидаемые адреса найдены
        expected_ips = ["2001:db8::1", "fe80::1%eth0",
                        "2001:0db8:85a3:0000:0000:8a2e:0370:7334"]

        for ip in expected_ips:
            self.assertIn(ip, found, f"Адрес {ip} не найден")

    def test_find_in_file(self):
        """Тест 4: Поиск в файле"""
        # Создаем временный файл с тестовыми данными
        test_content = """
        2001:db8::1
        192.168.1.1 (не IPv6)
        fe80::1%eth0
        невалидный 2001:db8:::1
        """

        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write(test_content)
            temp_file = f.name

        try:
            found = self.checker.find_ipv6_in_file(temp_file)
            self.assertEqual(len(found), 2, "Должно быть найдено 2 адреса")
        finally:
            # Удаляем временный файл
            os.unlink(temp_file)

    def test_empty_input(self):
        """Тест 5: Пустой ввод"""
        self.assertFalse(self.checker.is_valid_ipv6(None))
        self.assertFalse(self.checker.is_valid_ipv6(""))
        self.assertEqual(self.checker.find_ipv6(""), [])
        self.assertEqual(self.checker.find_ipv6(None), [])

    def test_normalize_ipv6(self):
        """Тест 6: Нормализация адресов"""
        test_cases = [
            ("2001:0db8:0000:0000:0000:0000:0000:0001",
             "2001:db8::1"),
            ("::1", "::1"),
        ]

        for original, expected in test_cases:
            normalized = self.checker.normalize_ipv6(original)
            # Проверяем, что результат содержит меньше символов (сокращен)
            self.assertLessEqual(len(normalized), len(original))


def run_tests():
    """Функция для запуска тестов"""
    # Создаем тестовый набор
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIPv6Checker)

    # Запускаем тесты с подробным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Выводим статистику
    print(f"\n{'=' * 50}")
    print(f"Результаты тестирования:")
    print(f"  Запущено тестов: {result.testsRun}")
    print(f"  Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  Ошибок: {len(result.errors)}")
    print(f"  Провалено: {len(result.failures)}")
    print(f"{'=' * 50}")

    return result


if __name__ == '__main__':
    run_tests()