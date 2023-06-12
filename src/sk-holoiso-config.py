#!/usr/bin/python
# coding=utf-8
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class HomePage(Gtk.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_spacing(10)
        label = Gtk.Label(label="这是首页")
        self.pack_start(label, True, True, 0)

        button = Gtk.Button(label="下一页")
        button.connect("clicked", self.on_next_page_clicked)
        self.pack_start(button, True, True, 0)

    def on_next_page_clicked(self, button):
        app.show_page(SecondPage)


class SecondPage(Gtk.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_spacing(10)
        label = Gtk.Label(label="这是第二页")
        self.pack_start(label, True, True, 0)

        button = Gtk.Button(label="返回")
        button.connect("clicked", self.on_back_clicked)
        self.pack_start(button, True, True, 0)

    def on_back_clicked(self, button):
        app.show_page(HomePage)


class Application(Gtk.Window):
    def __init__(self):
        super().__init__(title="多级路由示例")
        self.set_default_size(300, 200)
        self.connect("destroy", Gtk.main_quit)

        self.pages = {
            HomePage: None,
            SecondPage: None
        }

        self.current_page = None

        self.show_page(HomePage)

    def show_page(self, page):
        if self.current_page is not None:
            self.remove(self.current_page)

        if self.pages[page] is None:
            self.pages[page] = page()

        self.current_page = self.pages[page]
        self.add(self.current_page)
        self.show_all()


if __name__ == "__main__":
    app = Application()
    Gtk.main()
