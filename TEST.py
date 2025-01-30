from flet import *
from help_func.File_management import URL_MANAGEMENT

def main(page: Page):
    # Интерфейс прогресс-бара
    progress_container = Container(
        width=0,
        height=30,
        gradient=LinearGradient(
            begin=Alignment(-1, 0),
            end=Alignment(1, 0),
            colors=[Colors.GREEN_200, Colors.GREEN, Colors.GREEN_600],
        ),
        border_radius=5,
    )
    progress_background = Container(
        width=400,
        height=30,
        bgcolor=Colors.GREY,
        border_radius=5,
    )
    progress_label = Text("Прогресс: 0%", size=14)

    def update_progress(progress):
        """Обновляет прогресс-бара."""
        progress_container.width = 400 * progress
        progress_label.value = f"Прогресс: {int(progress * 100)}%"
        page.update()

    def start_download(e):
        """Начало скачивания файлов."""
        urls = [
            "https://cdn.culture.ru/files/208468e9-a0d3-5e01-8191-fbf9a1cff57a/voina-i-mir",
            "https://flibusta.su/b/img/big/170983.jpg",
        ]
        downloader = URL_MANAGEMENT(on_progress_update=update_progress)
        downloader.download_files_in_threads(urls)

    start_button = ElevatedButton("Скачать файлы", on_click=start_download)

    # Добавляем элементы на страницу
    page.add(
        Column(
            [
                Stack([progress_background, progress_container]),
                progress_label,
                start_button,
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
    )

app(main)
