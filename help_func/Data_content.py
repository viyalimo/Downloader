from flet import *
from help_func.File_management import URL_MANAGEMENT

class CustomContainer(UserControl, URL_MANAGEMENT):
    def __init__(self, text, parent_container, color, bg_color, page):
        super().__init__()
        self.text = text
        self.text_color = color
        self.bg_color = bg_color
        self.page = page
        self.text_control = Text(self.text[:74], size=16, color=color)
        self.parent_container = parent_container
        self.overlay = None  # Слой для отображения перекрывающего окна
        self.size_data = None
        self.format_data = None
        self.name_file = None
        self.flag = True
        self.delete_button = IconButton(
            icon=icons.CLOSE,
            icon_color=colors.RED,
            on_click=self.delete_row,
            visible=self.flag,
            icon_size=20
        )
        self.progress_container = Container(
            width=0,
            height=20,
            gradient=LinearGradient(
                begin=Alignment(-1, 0),
                end=Alignment(1, 0),
                colors=[Colors.GREEN_200, Colors.GREEN, Colors.GREEN_600],
            ),
            border_radius=5,
        )
        self.progress_background = Container(
            width=60,
            height=20,
            bgcolor=Colors.GREY,
            border_radius=5,
        )
        self.more_button = IconButton(
            icon=icons.MORE_VERT,
            icon_color=color,
            on_click=self.show_overlay,
            icon_size=20
        )
        self.pb = Stack([self.progress_background, self.progress_container])
        self.container_del = Container(content=self.delete_button)
        self.change_text_color(color)

    def change_text_color(self, color):
        self.text_control.color = color
        self.more_button.icon_color = color
        if color == Colors.BLACK:
            new_gradient = LinearGradient(
                begin=Alignment(-1, 0),
                end=Alignment(1, 0),
                colors=[Colors.GREEN_200, Colors.GREEN, Colors.GREEN_600],
            )
        else:
            new_gradient = LinearGradient(
                begin=Alignment(-1, 0),
                end=Alignment(1, 0),
                colors=[Colors.BLUE_200, Colors.BLUE, Colors.BLUE_600],
            )

            # Применяем новый градиент
        self.progress_container.gradient = new_gradient
        self.update()

    def show_overlay(self, e):
        """Показывает перекрывающее окно."""

        if self.size_data[:5] != "Error":
            size_data = Text(f"Размер файла: {self.size_data} MB", size=16, color=self.text_color)
        else:
            self.page.snack_bar = SnackBar(
                content=Row([Text(str(self.size_data), color='white')],
                            alignment=MainAxisAlignment.CENTER),
                bgcolor=Colors.RED,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        if self.format_data[:5] != "Error":
            format_data = Text(f"Формат файла: {self.format_data}", size=16, color=self.text_color)
        else:
            self.page.snack_bar = SnackBar(
                content=Row([Text(str(self.format_data), color='white')],
                            alignment=MainAxisAlignment.CENTER),
                bgcolor=Colors.RED,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        if self.name_file[:5] != "Error":
            name_file = Text(f"Имя файла: {self.name_file}", size=16, color=self.text_color)
        else:
            self.page.snack_bar = SnackBar(
                content=Row([Text(str(self.name_file), color='white')],
                            alignment=MainAxisAlignment.CENTER),
                bgcolor=Colors.RED,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.overlay = Container(
            content=Container(
                content=Column(
                    controls=[
                        size_data,
                        format_data,
                        name_file,
                    ],
                    scroll=ScrollMode.AUTO
                ),
                alignment=Alignment(0, 0),
                expand=True,
                width=250,
                height=140,
                padding=10,
                bgcolor=self.bg_color,
                border=border.all(2, color=self.text_color),
            ),
            alignment=alignment.center,
            expand=True,
            on_click=self.close_overlay
        )
        self.page.overlay.append(self.overlay)
        self.page.update()

    def close_overlay(self, e):
        """Закрывает перекрывающее окно."""
        if self.overlay in self.page.overlay:
            self.page.overlay.remove(self.overlay)
            self.page.update()

    def delete_row(self, e):
        if self in self.parent_container.content.controls:
            self.parent_container.content.controls.remove(self)
            self.parent_container.update()

    def set_status_icon(self, result):
        """Устанавливает иконку статуса вместо прогресс-бара."""
        if result:
            self.container_del.content = Icon(Icons.CHECK_CIRCLE, size=20, color=Colors.GREEN)
            self.container_del.update()
            self.update()
            self.page.update()
        else:
            self.container_del.content = IconButton(icon=Icons.WARNING)
            self.container_del.update()
            self.update()
            self.page.update()

    def build(self):

        """Строит основной контейнер."""


        if self.flag:
            self.container_del.content = self.delete_button
        else:
            self.container_del.content = self.pb
        self.size_data = self.get_file_size(self.text)
        self.format_data = self.get_file_format(self.text)
        self.name_file = self.get_file_name(self.text)
        return Container(
            content=Row(
                [
                    Row(
                        controls=[self.text_control],
                        alignment=MainAxisAlignment.START,
                        expand=True,
                    ),
                    Row(
                        controls=[self.more_button, self.container_del],
                        alignment=MainAxisAlignment.END,
                        expand=True,

                    )
                ],
                # alignment=MainAxisAlignment.SPACE_BETWEEN
            ),
            width=790,
            height=30,
        )
