import arcade
import arcade.gui


class MenuView(arcade.View):
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
            text="Крестики-Нолики (5 в ряд)",
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
        
        rules_button = arcade.gui.UIFlatButton(text="Правила", width=btn_width, height=btn_height)
        rules_button.on_click = self.on_rules_click
        v_box.add(rules_button.with_padding(bottom=int(25 * scale)))
        
        exit_button = arcade.gui.UIFlatButton(text="Выход", width=btn_width, height=btn_height)
        exit_button.on_click = self.on_exit_click
        v_box.add(exit_button.with_padding(bottom=int(25 * scale)))
        
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
    
    def on_exit_click(self, event):
        arcade.close_window()
