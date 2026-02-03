import arcade
import arcade.gui

from game.player_db import rename_player


class PlayerRenameView(arcade.View):
    def __init__(self, old_name: str):
        super().__init__()
        self.old_name = old_name
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
            text="Переименовать игрока",
            font_size=int(36 * scale),
            font_name="Arial",
            bold=True,
            text_color=(255, 255, 255),
        )
        v_box.add(title_label.with_padding(bottom=int(25 * scale)))

        current_label = arcade.gui.UILabel(
            text=f"Текущее имя: {self.old_name}",
            font_size=int(18 * scale),
            text_color=(200, 200, 200),
        )
        v_box.add(current_label.with_padding(bottom=int(15 * scale)))

        self.name_input = arcade.gui.UIInputText(
            text=self.old_name,
            width=max(360, int(520 * scale)),
            height=max(36, int(44 * scale)),
            font_size=int(20 * scale),
            text_color=(255, 255, 255),
        )
        self.name_input.caret.color = (255, 255, 255)
        try:
            self.name_input.layout.selection_color = (80, 80, 80, 200)
        except Exception:
            pass
        v_box.add(self.name_input.with_padding(bottom=int(15 * scale)))

        self.error_label = arcade.gui.UILabel(
            text="",
            font_size=int(18 * scale),
            text_color=arcade.color.RED,
        )
        v_box.add(self.error_label.with_padding(bottom=int(15 * scale)))

        btn_width = max(200, int(240 * scale))
        btn_height = max(42, int(52 * scale))

        buttons = arcade.gui.UIBoxLayout(vertical=False)
        save_btn = arcade.gui.UIFlatButton(text="Сохранить", width=btn_width, height=btn_height)
        save_btn.on_click = self.on_save_click
        buttons.add(save_btn.with_padding(right=int(20 * scale)))

        cancel_btn = arcade.gui.UIFlatButton(text="Отмена", width=btn_width, height=btn_height)
        cancel_btn.on_click = self.on_cancel_click
        buttons.add(cancel_btn)

        v_box.add(buttons.with_padding(top=int(10 * scale)))

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

    def on_save_click(self, event):
        new_name = self.name_input.text if self.name_input else ""
        ok, error = rename_player(self.old_name, new_name)
        if not ok:
            self.error_label.text = error
            return
        from ui.rating_view import RatingView
        self.window.show_view(RatingView())

    def on_cancel_click(self, event):
        from ui.rating_view import RatingView
        self.window.show_view(RatingView())

