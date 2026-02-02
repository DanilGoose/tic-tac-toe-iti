import arcade
import arcade.gui

from game.player_db import add_player


class PlayerAddView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.name_input = None
        self.error_label = None
        self.setup_ui()

    def setup_ui(self):
        self.manager.clear()
        scale = min(self.window.width / 1024, self.window.height / 768)
        scale = max(0.75, min(1.2, scale))

        v_box = arcade.gui.UIBoxLayout()

        title_label = arcade.gui.UILabel(
            text="Добавить игрока",
            font_size=int(40 * scale),
            font_name="Arial",
            bold=True,
            text_color=(255, 255, 255),
        )
        v_box.add(title_label.with_padding(bottom=int(35 * scale)))

        self.name_input = arcade.gui.UIInputText(
            text="",
            width=max(320, int(440 * scale)),
            height=max(36, int(44 * scale)),
            font_size=int(20 * scale),
            text_color=(255, 255, 255),
        )
        self.name_input.caret.color = (255, 255, 255)
        try:
            self.name_input.layout.selection_color = (80, 80, 80, 200)
        except Exception:
            pass
        v_box.add(self.name_input.with_padding(bottom=int(20 * scale)))

        self.error_label = arcade.gui.UILabel(
            text="",
            font_size=int(18 * scale),
            text_color=arcade.color.RED,
        )
        v_box.add(self.error_label.with_padding(bottom=int(20 * scale)))

        btn_width = max(200, int(240 * scale))
        btn_height = max(42, int(52 * scale))

        add_button = arcade.gui.UIFlatButton(text="Добавить", width=btn_width, height=btn_height)
        add_button.on_click = self.on_add_click
        v_box.add(add_button.with_padding(bottom=int(15 * scale)))

        back_button = arcade.gui.UIFlatButton(text="Назад", width=btn_width, height=btn_height)
        back_button.on_click = self.on_back_click
        v_box.add(back_button)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(v_box, anchor_x="center", anchor_y="center")
        self.manager.add(anchor)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.manager.enable()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.setup_ui()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_add_click(self, event):
        name = self.name_input.text if self.name_input else ""
        ok, error = add_player(name)
        if not ok:
            self.error_label.text = error
            return
        from ui.menu_view import MenuView
        self.window.show_view(MenuView())

    def on_back_click(self, event):
        from ui.menu_view import MenuView
        self.window.show_view(MenuView())
