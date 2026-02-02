import arcade
import arcade.gui
from game.player_db import get_player_names


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.error_label = None
        self.setup_ui()
    
    def setup_ui(self):
        self.manager.clear()
        scale = min(self.window.width / 1024, self.window.height / 768)
        scale = max(0.75, min(1.2, scale))
        
        v_box = arcade.gui.UIBoxLayout()
        
        title_label = arcade.gui.UILabel(
            text="Ментальные Крестики-Нолики",
            font_size=int(44 * scale),
            font_name="Arial",
            bold=True,
            text_color=(255, 255, 255)
        )
        v_box.add(title_label.with_padding(bottom=int(60 * scale)))
        
        btn_width = max(220, int(280 * scale))
        btn_height = max(48, int(60 * scale))
        play_button = arcade.gui.UIFlatButton(text="Играть", width=btn_width, height=btn_height)
        play_button.on_click = self.on_play_click
        v_box.add(play_button.with_padding(bottom=int(25 * scale)))
        
        settings_button = arcade.gui.UIFlatButton(text="Настройки", width=btn_width, height=btn_height)
        settings_button.on_click = self.on_settings_click
        v_box.add(settings_button.with_padding(bottom=int(25 * scale)))

        add_player_button = arcade.gui.UIFlatButton(text="Добавить игрока", width=btn_width, height=btn_height)
        add_player_button.on_click = self.on_add_player_click
        v_box.add(add_player_button.with_padding(bottom=int(25 * scale)))

        rating_button = arcade.gui.UIFlatButton(text="Рейтинг игроков", width=btn_width, height=btn_height)
        rating_button.on_click = self.on_rating_click
        v_box.add(rating_button.with_padding(bottom=int(25 * scale)))
        
        rules_button = arcade.gui.UIFlatButton(text="Правила", width=btn_width, height=btn_height)
        rules_button.on_click = self.on_rules_click
        v_box.add(rules_button.with_padding(bottom=int(25 * scale)))
        
        exit_button = arcade.gui.UIFlatButton(text="Выход", width=btn_width, height=btn_height)
        exit_button.on_click = self.on_exit_click
        v_box.add(exit_button.with_padding(bottom=int(25 * scale)))
        
        self.error_label = arcade.gui.UILabel(
            text="",
            font_size=int(18 * scale),
            font_name="Arial",
            text_color=arcade.color.RED
        )
        v_box.add(self.error_label.with_padding(top=int(10 * scale)))

        hint_label = arcade.gui.UILabel(
            text="Клик мышью - выбор клетки | Enter - подтвердить ход",
            font_size=int(18 * scale),
            font_name="Arial",
            text_color=(200, 200, 200)
        )
        v_box.add(hint_label.with_padding(top=int(40 * scale)))
        
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
    
    def on_play_click(self, event):
        settings = self.window.game_settings
        player_count = settings.get("player_count", 0)
        if player_count < 2:
            if self.error_label:
                self.error_label.text = "Слишком мало игроков"
            return
        players = settings.get("players", [])
        selected_names = [players[i].get("name", "") for i in range(player_count)]
        available_names = set(get_player_names())
        if any(name not in available_names for name in selected_names):
            if self.error_label:
                self.error_label.text = "Выберите игроков из списка"
            return
        if len(selected_names) != len(set(selected_names)):
            if self.error_label:
                self.error_label.text = "Игроки должны быть разными"
            return
        from ui.game_view import GameView
        game_view = GameView(self.window.game_settings)
        self.window.show_view(game_view)
    
    def on_settings_click(self, event):
        from ui.settings_view import SettingsView
        settings_view = SettingsView()
        self.window.show_view(settings_view)
    
    def on_rules_click(self, event):
        from ui.rules_view import RulesView
        rules_view = RulesView()
        self.window.show_view(rules_view)

    def on_add_player_click(self, event):
        from ui.player_add_view import PlayerAddView
        self.window.show_view(PlayerAddView())

    def on_rating_click(self, event):
        from ui.rating_view import RatingView
        self.window.show_view(RatingView())
    
    def on_exit_click(self, event):
        arcade.close_window()
