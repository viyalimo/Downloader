import os

from flet import *
from help_func.Data_content import CustomContainer
from help_func.File_management import URL_MANAGEMENT


class Downloader:
    def __init__(self, page):
        self.page = page
        self.Enter_text_container = Container(
            content=Column(
                controls=[],
                scroll=ScrollMode.HIDDEN
            ),
            alignment=Alignment(0, -1),
            border=border.all(1, color=self.update_colors()["icon_color"]),
            width=self.update_size()["enter_label_width"],
            height=self.update_size()["enter_container_height"],

        )
        self.main_page(clear=False)

    @staticmethod
    def update_size():
        return {
            "icon_size": 20,
            "enter_label_width": 800,
            "enter_label_height": 45,
            "enter_label_text_size": 15,
            "enter_container_height": 350,
            "download_container_width": 800,
            "download_container_height": 45,
            "text_field_path_width": 500,
            "text_field_path_height": 35,
        }

    def update_icon(self):
        if self.page.theme_mode == ThemeMode.LIGHT:
            return {
                "icon": Icons.DARK_MODE_OUTLINED,
            }
        else:
            return {
                "icon": Icons.SUNNY
            }

    def update_colors(self):
        if self.page.theme_mode == ThemeMode.LIGHT:
            return {
                "bgcolor": Colors.WHITE,
                "icon_color": Colors.BLACK,
            }
        else:
            return {
                "bgcolor": Colors.BLACK,
                "icon_color": Colors.BLUE,
            }

    def download_page(self, file_size: float, path_save):
        self.page.clean()
        self.page.update()

        def style_revert(e):
            if self.page.theme_mode == ThemeMode.DARK:
                self.page.theme_mode = ThemeMode.LIGHT
                icon_but.icon = Icons.DARK_MODE_OUTLINED
                icon_but.icon_color = Colors.BLACK
                back_btn.icon_color = Colors.BLACK
            else:
                self.page.theme_mode = ThemeMode.DARK
                icon_but.icon = Icons.SUNNY
                icon_but.icon_color = Colors.BLUE
                back_btn.icon_color = Colors.BLUE

            colors = self.update_colors()

            self.page.size_data.color = colors['icon_color']
            path_data.color = colors['icon_color']

            download_btn.bgcolor = colors["bgcolor"]
            download_btn.border = border.all(1, colors["icon_color"])
            download_btn.content.color = colors["icon_color"]

            for container in self.Enter_text_container.content.controls:
                container.change_text_color(colors["icon_color"])
                container.text_color = colors["icon_color"]
                container.bg_color = colors["bgcolor"]

            self.Enter_text_container.border = border.all(1, color=self.update_colors()["icon_color"])
            self.Enter_text_container.update()
            self.page.update()

        def hover(e):
            if self.page.theme_mode == ThemeMode.DARK:
                if e.data == 'true':
                    download_btn.bgcolor = Colors.BLUE_GREY_900
                else:
                    download_btn.bgcolor = Colors.BLACK
            else:
                if e.data == 'true':
                    download_btn.bgcolor = Colors.GREY_400
                else:
                    download_btn.bgcolor = Colors.WHITE
            download_btn.update()
            self.page.update()

        def update_flag():
            for i in self.Enter_text_container.content.controls:
                i.flag = not i.flag
                i.update()
            self.page.update()

        def end_download(e):
            self.main_page(clear=True)

        def start_download(e):
            urls = [container for container in self.Enter_text_container.content.controls]
            downloader = URL_MANAGEMENT()
            downloader.download_files_in_threads(urls, path_save, self.page)
            self.page.snack_bar = SnackBar(
                content=Row([Text(f"Файлы скачаны в папку: {path_save}", color='white')],
                            alignment=MainAxisAlignment.CENTER),
                bgcolor=colors.GREEN,

            )
            self.page.snack_bar.open = True
            os.startfile(path_save)
            back_btn.visible = False
            download_btn.content = Text("Finish", color=self.update_colors()["icon_color"], size=16)
            download_btn.on_click = lambda e: end_download(e)
            download_btn.update()
            self.page.update()


        def back(e):
            update_flag()
            self.Enter_text_container.update()
            self.main_page(clear=False, path_save=path_save)

        icon_but = IconButton(icon=self.update_icon()['icon'],
                              on_click=style_revert,
                              icon_size=self.update_size()["icon_size"],
                              icon_color=self.update_colors()["icon_color"])

        icon_but_container = Container(
            content=icon_but,
        )

        icon_but_row = Row(
            controls=[
                icon_but_container,
            ],
            alignment=MainAxisAlignment.END
        )

        back_btn = IconButton(icon=Icons.ARROW_BACK,
                              on_click=back,
                              icon_size=self.update_size()["icon_size"],
                              icon_color=self.update_colors()["icon_color"],
                              visible=True
                              )

        back_container = Container(
            content=back_btn,
        )

        back_row = Row(
            controls=[
                back_container,
            ],
            alignment=MainAxisAlignment.START
        )

        top_rectangle = Row(
            controls=[
                back_row,
                icon_but_row,
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        )

        Enter_container_place = Row(
            controls=[
                self.Enter_text_container,
            ],
            alignment=MainAxisAlignment.CENTER,
            expand=True,
        )

        self.page.size_data = Text(f"Общий размер данных: {file_size} Mb",
                                   size=self.update_size()["enter_label_text_size"],
                                   color=self.update_colors()["icon_color"])
        path_data = Text(f"Путь для сохранения: {path_save}", size=self.update_size()["enter_label_text_size"],
                         color=self.update_colors()["icon_color"])

        data_container = Container(
            content=Column(
                controls=[
                    self.page.size_data,
                    path_data,
                ],
            ),
            padding=padding.only(left=7)
        )

        data_place = Row(
            controls=[
                data_container,
            ],
            alignment=MainAxisAlignment.START,
            expand=True,
        )
        download_btn = Container(
            content=Text("Download", color=self.update_colors()["icon_color"], size=16),
            alignment=Alignment(0, 0),
            border=border.all(1, color=self.update_colors()["icon_color"]),
            width=100,
            height=40,
            on_hover=lambda e: hover(e),
            on_click=lambda e: start_download(e),
        )

        download_btn_place = Row(
            controls=[download_btn],
            alignment=MainAxisAlignment.END,
            expand=True,
        )

        download_container = Row([
            Container(
                content=download_btn_place,
                width=800,
                height=40,
                alignment=Alignment(0, 0),
            )
        ],
            alignment=MainAxisAlignment.CENTER,
            expand=True,
        )

        content_container = Column(
            controls=[top_rectangle, data_place, Enter_container_place, download_container],
            alignment=MainAxisAlignment.START,
        )
        update_flag()
        self.page.add(content_container)

    def main_page(self, clear: bool, path_save=None):
        if clear:
            self.Enter_text_container.content.controls.clear()
            path_save = None
        else:
            pass
        self.page.clean()
        self.page.update()
        pb = Container(
            ProgressBar(width=800, color="amber", bgcolor=Colors.GREEN),
            visible=False,
            alignment=Alignment(0, 0)
        )

        def add_new_container(text):
            """Добавляет новый контейнер в родительский контейнер."""
            pb.visible = True
            self.page.update()
            if text == "":
                self.page.snack_bar = SnackBar(
                    content=Row([Text("Введите ссылку!", color='white')],
                                alignment=MainAxisAlignment.CENTER),
                    bgcolor=Colors.RED,
                )
                self.page.snack_bar.open = True
                url_enter.focus()
                self.page.update()
            elif text[:4] != "http":
                self.page.snack_bar = SnackBar(
                    content=Row([Text("Введите корректную ссылку!", color='white')],
                                alignment=MainAxisAlignment.CENTER),
                    bgcolor=Colors.RED,
                )
                self.page.snack_bar.open = True
                url_enter.value = ""
                url_enter.focus()
                self.page.update()
            else:
                new_container = CustomContainer(text, self.Enter_text_container,
                                                color=self.update_colors()['icon_color'],
                                                bg_color=self.update_colors()['bgcolor'], page=self.page)
                self.Enter_text_container.content.controls.append(new_container)
                self.Enter_text_container.update()
                url_enter.value = ""
                self.page.update()
            pb.visible = False
            self.page.update()

        def update_parent_container(e):
            print("update")
            for contain in self.Enter_text_container.content.controls:
                contain.parent_container = self.Enter_text_container
                print(contain.parent_container)
                contain.update()
                self.Enter_text_container.update()

        # Функция для смены темы
        def style_revert(e):
            if self.page.theme_mode == ThemeMode.DARK:
                self.page.theme_mode = ThemeMode.LIGHT
                icon_but.icon = Icons.DARK_MODE_OUTLINED
                icon_but.icon_color = Colors.BLACK
            else:
                self.page.theme_mode = ThemeMode.DARK
                icon_but.icon = Icons.SUNNY
                icon_but.icon_color = Colors.BLUE

            colors = self.update_colors()
            icon_but_PLUS.icon_color = colors["icon_color"]

            url_enter.border_color = colors["icon_color"]
            url_enter.text_style = TextStyle(color=colors["icon_color"])
            url_enter.hint_style = TextStyle(color=colors["icon_color"])
            url_enter.cursor_color = colors["icon_color"]

            enter_path.border_color = colors["icon_color"]
            enter_path.text_style = TextStyle(color=colors["icon_color"])
            enter_path.hint_style = TextStyle(color=colors["icon_color"])
            enter_path.cursor_color = colors["icon_color"]

            folder_btn.icon_color = colors["icon_color"]

            next_btn.bgcolor = colors["bgcolor"]
            next_btn.border = border.all(1, colors["icon_color"])
            next_btn.content.color = colors["icon_color"]
            for container in self.Enter_text_container.content.controls:
                container.change_text_color(colors["icon_color"])
                container.text_color = colors["icon_color"]
                container.bg_color = colors["bgcolor"]

            self.Enter_text_container.border = border.all(1, color=self.update_colors()["icon_color"])
            self.Enter_text_container.update()
            self.page.update()

        def hover(e):
            if self.page.theme_mode == ThemeMode.DARK:
                if e.data == 'true':
                    next_btn.bgcolor = Colors.BLUE_GREY_900
                else:
                    next_btn.bgcolor = Colors.BLACK
            else:
                if e.data == 'true':
                    next_btn.bgcolor = Colors.GREY_400
                else:
                    next_btn.bgcolor = Colors.WHITE
            next_btn.update()
            self.page.update()

        def next_page(e):
            if enter_path.value == "":
                self.page.snack_bar = SnackBar(
                    content=Row([Text(f"Укажите путь к директории для сохранения!", color='white')],
                                alignment=MainAxisAlignment.CENTER),
                    bgcolor=colors.RED,

                )
                self.page.snack_bar.open = True
                enter_path.focus()
                self.page.update()
                return
            elif len(self.Enter_text_container.content.controls) == 0:
                self.page.snack_bar = SnackBar(
                    content=Row([Text(f"Нужно добавить хотя бы одну ссылку для скачивания!", color='white')],
                                alignment=MainAxisAlignment.CENTER),
                    bgcolor=colors.RED,

                )
                self.page.snack_bar.open = True
                url_enter.focus()
                self.page.update()
                return
            else:
                files_size = get_size_files()
                self.download_page(files_size, enter_path.value)

        def get_size_files():
            total_size = 0
            for container in self.Enter_text_container.content.controls:
                if container.size_data == "unknown":
                    pass
                else:
                    total_size += float(container.size_data)
            return total_size

        def click(e):
            path = e.path
            enter_path.value = path
            self.page.update()

        icon_but = IconButton(icon=self.update_icon()["icon"],
                              on_click=style_revert,
                              icon_size=self.update_size()["icon_size"],
                              icon_color=self.update_colors()["icon_color"])

        icon_but_container = Container(
            content=icon_but,
        )

        icon_but_row = Row(
            controls=[
                icon_but_container,
            ],
            alignment=MainAxisAlignment.CENTER
        )
        icon_but_PLUS = IconButton(icon=Icons.ADD, icon_size=self.update_size()["icon_size"],
                                   icon_color=self.update_colors()["icon_color"],
                                   on_click=lambda e: add_new_container(url_enter.value), )
        url_enter = TextField(hint_text="Enter url",
                              hint_style=TextStyle(size=self.update_size()["enter_label_text_size"],
                                                   color=self.update_colors()["icon_color"]),
                              width=self.update_size()["enter_label_width"],
                              height=self.update_size()["enter_label_height"],
                              text_size=self.update_size()["enter_label_text_size"],
                              suffix_icon=icon_but_PLUS,
                              text_style=TextStyle(size=self.update_size()["enter_label_text_size"],
                                                   color=self.update_colors()["icon_color"]),
                              border_color=self.update_colors()["icon_color"],
                              )

        enter_container = Container(
            content=url_enter,
            padding=padding.only(top=5)
        )

        enter_place = Row(
            controls=[
                enter_container,
            ],
            alignment=MainAxisAlignment.CENTER,
            expand=True
        )

        enter_container_place = Row(
            controls=[
                self.Enter_text_container,
            ],
            alignment=MainAxisAlignment.CENTER,
            expand=True,
        )

        file_peacker = FilePicker(on_result=lambda e: click(e))
        self.page.overlay.append(file_peacker)

        folder_btn = IconButton(icon=Icons.FOLDER, icon_size=self.update_size()["icon_size"],
                                icon_color=self.update_colors()["icon_color"],
                                on_click=lambda e: file_peacker.get_directory_path()
                                )

        enter_path = TextField(
            hint_text="Enter path",
            value=path_save,
            hint_style=TextStyle(size=self.update_size()["enter_label_text_size"],
                                 color=self.update_colors()["icon_color"]),
            width=self.update_size()["text_field_path_width"],
            height=self.update_size()["enter_label_height"],
            text_size=self.update_size()["enter_label_text_size"],
            suffix_icon=folder_btn,
            text_style=TextStyle(size=self.update_size()["enter_label_text_size"],
                                 color=self.update_colors()["icon_color"]),
            border_color=self.update_colors()["icon_color"],
            expand=4,
        )

        next_btn = Container(
            content=Text("Next", color=self.update_colors()["icon_color"], size=16),
            alignment=Alignment(0, 0),
            border=border.all(1, color=self.update_colors()["icon_color"]),
            width=80,
            height=50,
            on_hover=lambda e: hover(e),
            on_click=lambda e: next_page(e),
        )

        download_container_field = Container(
            content=Row(
                controls=[enter_path, next_btn],
            ),
            width=self.update_size()["download_container_width"],
            height=self.update_size()["enter_label_height"],
            alignment=Alignment(0, 0),
        )

        download_container_place = Row(
            controls=[download_container_field],
            alignment=MainAxisAlignment.CENTER,
            expand=True,
        )

        content_container = Column(
            controls=[icon_but_row, enter_place, pb, enter_container_place, download_container_place],
            alignment=MainAxisAlignment.START,

        )
        self.page.add(content_container)


def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT
    page.title = "Downloader"
    page.window.width = 850
    page.window.height = 620
    page.window.resizable = False
    Downloader(page)


if __name__ == "__main__":
    app(target=main)
