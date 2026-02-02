import arcade
import arcade.gui

from game.player_db import get_player_stats


class RatingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.setup_ui()

    def setup_ui(self):
        self.manager.clear()
        scale = min(self.window.width / 1024, self.window.height / 768)
        scale = max(0.75, min(1.2, scale))

        v_box = arcade.gui.UIBoxLayout()

        title_label = arcade.gui.UILabel(
            text="Рейтинг игроков",
            font_size=int(40 * scale),
            font_name="Arial",
            bold=True,
            text_color=(255, 255, 255),
        )
        v_box.add(title_label.with_padding(bottom=int(30 * scale)))

        stats = get_player_stats()
        if not stats:
            empty_label = arcade.gui.UILabel(
                text="Нет игроков",
                font_size=int(22 * scale),
                text_color=(200, 200, 200),
            )
            v_box.add(empty_label.with_padding(bottom=int(20 * scale)))
        else:
            header = arcade.gui.UIBoxLayout(vertical=False)
            name_w = max(220, int(320 * scale))
            games_w = max(90, int(120 * scale))
            wins_w = max(90, int(120 * scale))

            header.add(arcade.gui.UILabel(text="Игрок", font_size=int(20 * scale), text_color=(255, 255, 255)).with_padding(right=20))
            header.add(arcade.gui.UILabel(text="Игры", font_size=int(20 * scale), text_color=(255, 255, 255)).with_padding(right=20))
            header.add(arcade.gui.UILabel(text="Победы", font_size=int(20 * scale), text_color=(255, 255, 255)))
            v_box.add(header.with_padding(bottom=int(10 * scale)))

            for row in stats:
                row_box = arcade.gui.UIBoxLayout(vertical=False)
                row_box.add(
                    arcade.gui.UILabel(
                        text=row["name"],
                        font_size=int(18 * scale),
                        text_color=(230, 230, 230),
                        width=name_w,
                    ).with_padding(right=20)
                )
                row_box.add(
                    arcade.gui.UILabel(
                        text=str(row["games_played"]),
                        font_size=int(18 * scale),
                        text_color=(230, 230, 230),
                        width=games_w,
                    ).with_padding(right=20)
                )
                row_box.add(
                    arcade.gui.UILabel(
                        text=str(row["wins"]),
                        font_size=int(18 * scale),
                        text_color=(230, 230, 230),
                        width=wins_w,
                    )
                )
                v_box.add(row_box.with_padding(bottom=int(6 * scale)))

        btn_width = max(200, int(240 * scale))
        btn_height = max(44, int(54 * scale))
        back_button = arcade.gui.UIFlatButton(text="Назад", width=btn_width, height=btn_height)
        back_button.on_click = self.on_back_click
        v_box.add(back_button.with_padding(top=int(25 * scale)))

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

    def on_back_click(self, event):
        from ui.menu_view import MenuView
        self.window.show_view(MenuView())
