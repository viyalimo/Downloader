import requests

def get_file_format(url):
    try:
        # Отправляем запрос HEAD, чтобы получить информацию без скачивания файла
        response = requests.head(url)
        response.raise_for_status()  # Проверяем наличие ошибок

        # Получаем Content-Type из заголовков
        content_type = response.headers.get('Content-Type', 'unknown')

        # Если Content-Type известен, извлекаем формат файла
        if content_type != 'unknown':
            file_format = content_type.split('/')[1]  # Берём часть после "/"
        else:
            file_format = 'unknown'

        return file_format
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Пример использования
url = "https://bookstime.ru/storage/app/uploads/public/654/cbd/64c/654cbd64c4d1b797292245.png"
file_format = get_file_format(url)
print(f"Формат файла: {file_format}")
