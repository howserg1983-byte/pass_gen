print("Добро пожаловать в генератор паролей!")
print()
# Пользователю предлагается ввести количество символов его будующего пароля
while True:
    try:
        num = int(input("Введите желаемое количество символов для Вашего пароля (от пяти символов): ")) # Преобразовывает входные данные в целое число
        if num <= 4:
            print("Пожалуйста, введите число большее и равное пяти")
            continue
        break
    except ValueError:
        print("Некорректный ввод. Пожалуйста, введите число.")

# Пользователю предлагается запрос на включение специальных символов
while True:
    include_special = input("Включить специальные символы (например, !@#$%^&*)? (да/нет): ").lower()
    if include_special in ['да', 'нет']:
        break
    else:
        print("Некорректный ввод. Пожалуйста, введите 'да' или 'нет'.")

# Импорт библиотек
import string
import secrets
import random
import json 
from cryptography.fernet import Fernet

# Оценка сложности пароля
def assess_password_strength(password):
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    score = 0
    if length >= 8: score += 1
    if length >= 12: score += 1
    if has_lower: score += 1
    if has_upper: score += 1
    if has_digit: score += 1
    if has_special: score += 1

    if score == 6: return "Очень сильный"
    if score >= 4: return "Сильный"
    if score >= 2: return "Средний"
    return "Слабый"

# Формирование наборов символов для пароля
password_characters = []

# Гарантируем включение хотя бы одного символа из каждого обязательного набора
password_characters.append(secrets.choice(string.ascii_lowercase))
password_characters.append(secrets.choice(string.ascii_uppercase))
password_characters.append(secrets.choice(string.digits))

# Строим общий алфавит из всех доступных символов
alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
if include_special == 'да':
    password_characters.append(secrets.choice(string.punctuation))
    alphabet += string.punctuation

# Заполняем оставшуюся длину пароля случайными символами из общего алфавита
remaining_length = num - len(password_characters)
if remaining_length > 0:
    password_characters.extend(secrets.choice(alphabet) for _ in range(remaining_length))

# Перемешиваем список символов, чтобы рандомизировать их позиции
random.shuffle(password_characters)

password = ''.join(password_characters)

print(password)
print(f"Сложность пароля: {assess_password_strength(password)}")

# Генерация ключа
fernet_key = Fernet.generate_key()
print(f"Ваш Fernet ключ (сохраните его для дешифровки): {fernet_key.decode()}")

cipher_suite = Fernet(fernet_key)
encrypted_password = cipher_suite.encrypt(password.encode())

# Подготовка данных для сохранения
record = {
    "key": fernet_key.decode(),             
    "encrypted_password": encrypted_password.decode() 
}

# Добавление новой строки
with open("encrypted_pass.txt", "a") as file: 
    file.write(json.dumps(record) + "\n")   

print("Пароль успешно зашифрован и сохранен!")