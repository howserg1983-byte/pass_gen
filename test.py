import json
from cryptography.fernet import Fernet

print("Проверка дешифровки последнего сохраненного пароля...")

try:
    # Проверка файла, есть ли строки
    with open("encrypted_pass.txt", "r") as file:
        lines = file.readlines()

    if not lines:
        print("Файл 'encrypted_pass.txt' пуст. Нечего дешифровать.")
    else:
        # Получение последней записи
        last_line = lines[-1].strip()
        try:
            record = json.loads(last_line)
            key = record["key"].encode()
            encrypted_password = record["encrypted_password"].encode()

            cipher_suite = Fernet(key)
            decrypted_password = cipher_suite.decrypt(encrypted_password).decode()

            print(f"УСПЕШНО: Дешифрованный пароль: {decrypted_password}")
        except Exception as e:
            print(f"ОШИБКА: Не удалось дешифровать последнюю запись: {e}. Запись: {last_line}")

except FileNotFoundError:
    print("ОШИБКА: Файл 'encrypted_pass.txt' не найден. Запустите генератор паролей, чтобы создать его.")
except Exception as e:
    print(f"ОШИБКА: Произошла общая ошибка при чтении файла: {e}")