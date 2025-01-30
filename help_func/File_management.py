import requests
import os
from concurrent.futures import ThreadPoolExecutor




class URL_MANAGEMENT:
    def __init__(self, on_progress_update=None):
        self.on_progress_update = on_progress_update

    def get_file_format(self, url):
        try:
            # Попробуем определить формат из URL
            url_extension = os.path.splitext(url)[1][1:]  # Извлекаем расширение (без точки)
            if url_extension:
                return url_extension

            # Если нет расширения в URL, отправляем запрос на сервер
            response = requests.head(url, allow_redirects=True)
            response.raise_for_status()

            # Получаем Content-Type из заголовков
            content_type = response.headers.get('Content-Type', 'unknown')
            if content_type != 'unknown' and '/' in content_type:
                file_format = content_type.split('/')[1]  # Берём часть после "/"
                return file_format
            return 'unknown'
        except requests.exceptions.RequestException as e:
            return f"Error FORMAT: \n {e}"

    def get_file_size(self, url):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.head(url, headers=headers, allow_redirects=True)
            response.raise_for_status()

            content_length = response.headers.get('Content-Length')
            if content_length:
                return f"{int(content_length) / (1024 * 1024):.2f}"
            else:
                return 'unknown'
        except requests.exceptions.RequestException as e:
            return f"Error SIZE: \n {e}"

    def get_file_name(self, url):
        try:
            # Получаем имя файла из URL
            file_name_with_extension = os.path.basename(url)

            # Убираем расширение
            file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
            return file_name_without_extension
        except Exception as e:
            return f"Error FILE NAME: \n {e}"

    def download_file(self, url, save_dir=None, container=None, page=None):
        """Скачивает один файл и обновляет прогресс-бар указанного контейнера."""
        try:
            urls = url.text
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(urls, stream=True, headers=headers)
            response.raise_for_status()

            # Формируем путь для сохранения файла
            file_name = os.path.basename(urls.split("?")[0])
            save_as = os.path.join(save_dir, file_name) if save_dir else file_name

            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            # Сохраняем файл
            with open(save_as, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    downloaded_size += len(chunk)

                    # Обновление прогресса для конкретного контейнера
                    if container and total_size > 0:
                        progress = downloaded_size / total_size
                        container.progress_container.width = 60 * progress
                        container.progress_container.update()
            container.set_status_icon(True)
            page.update()


        except requests.exceptions.RequestException as e:
            container.set_status_icon(False)

    def download_files_in_threads(self, urls, save_dir=None, page=None):
        """Скачивает файлы в несколько потоков, обновляя прогресс для каждого контейнера."""
        with ThreadPoolExecutor() as executor:
            for url in urls:
                executor.submit(self.download_file, url, save_dir, url, page)
        return True
