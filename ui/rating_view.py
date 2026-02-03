import arcade
import arcade.gui

from game.player_db import get_player_stats, delete_player


class RatingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.error_label = None
        self.pending_delete_name = None
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

        self.error_label = arcade.gui.UILabel(
            text="",
            font_size=int(18 * scale),
            text_color=arcade.color.RED,
        )
        v_box.add(self.error_label.with_padding(bottom=int(15 * scale)))

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
            actions_w = max(160, int(200 * scale))
            col_gap = int(20 * scale)

            header.add(arcade.gui.UILabel(text="Название", font_size=int(20 * scale), text_color=(255, 255, 255), width=name_w).with_padding(right=col_gap))
            header.add(arcade.gui.UILabel(text="Игры", font_size=int(20 * scale), text_color=(255, 255, 255), width=games_w).with_padding(right=col_gap))
            header.add(arcade.gui.UILabel(text="Победы", font_size=int(20 * scale), text_color=(255, 255, 255), width=wins_w).with_padding(right=col_gap))
            header.add(arcade.gui.UILabel(text="Действие", font_size=int(20 * scale), text_color=(255, 255, 255), width=actions_w))
            v_box.add(header.with_padding(bottom=int(10 * scale)))

            for row in stats:
                row_box = arcade.gui.UIBoxLayout(vertical=False)
                
                player_name = row["name"]
                row_box.add(
                    arcade.gui.UILabel(
                        text=player_name,
                        font_size=int(18 * scale),
                        text_color=(230, 230, 230),
                        width=name_w,
                    ).with_padding(right=col_gap)
                )
                row_box.add(
                    arcade.gui.UILabel(
                        text=str(row["games_played"]),
                        font_size=int(18 * scale),
                        text_color=(230, 230, 230),
                        width=games_w,
                    ).with_padding(right=col_gap)
                )
                row_box.add(
                    arcade.gui.UILabel(
                        text=str(row["wins"]),
                        font_size=int(18 * scale),
                        text_color=(230, 230, 230),
                        width=wins_w,
                    ).with_padding(right=col_gap)
                )

                actions = arcade.gui.UIBoxLayout(vertical=False)
                actions.width = actions_w
                actions_btn_w = max(90, int((actions_w - 10) / 2))
                edit_btn = arcade.gui.UIFlatButton(text="Изменить", width=actions_btn_w, height=max(26, int(32 * scale)))
                edit_btn.player_name = player_name
                edit_btn.on_click = self.on_edit_click
                actions.add(edit_btn.with_padding(right=10))

                delete_text = "Удалить" if self.pending_delete_name != player_name else "Подтвердить"
                del_btn = arcade.gui.UIFlatButton(text=delete_text, width=actions_btn_w, height=max(26, int(32 * scale)))
                del_btn.player_name = player_name
                del_btn.on_click = self.on_delete_click
                actions.add(del_btn)

                row_box.add(actions)
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

    def on_edit_click(self, event):
        self.pending_delete_name = None
        from ui.player_rename_view import PlayerRenameView
        self.window.show_view(PlayerRenameView(event.source.player_name))

    def on_delete_click(self, event):
        name = event.source.player_name
        if self.pending_delete_name != name:
            self.pending_delete_name = name
            self.setup_ui()
            if self.error_label:
                self.error_label.text = f"Удалить игрока '{name}'? Нажмите 'Подтвердить'."
            return
        ok, error = delete_player(name)
        self.pending_delete_name = None
        self.setup_ui()
        if not ok and self.error_label:
            self.error_label.text = error
