import arcade
import arcade.gui


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.setup_ui()
    
    def setup_ui(self):
        self.manager.clear()
        
        v_box = arcade.gui.UIBoxLayout()
        
        title_label = arcade.gui.UILabel(
            text="Крестики-Нолики (5 в ряд)",
            font_size=44,
            font_name="Arial",
            bold=True,
            text_color=(255, 255, 255)
        )
        v_box.add(title_label.with_space_around(bottom=60))
        
        play_button = arcade.gui.UIFlatButton(text="Играть", width=280, height=60)
        play_button.on_click = self.on_play_click
        v_box.add(play_button.with_space_around(bottom=25))
        
        settings_button = arcade.gui.UIFlatButton(text="Настройки", width=280, height=60)
        settings_button.on_click = self.on_settings_click
        v_box.add(settings_button.with_space_around(bottom=25))
        
        rules_button = arcade.gui.UIFlatButton(text="Правила", width=280, height=60)
        rules_button.on_click = self.on_rules_click
        v_box.add(rules_button.with_space_around(bottom=25))
        
        exit_button = arcade.gui.UIFlatButton(text="Выход", width=280, height=60)
        exit_button.on_click = self.on_exit_click
        v_box.add(exit_button.with_space_around(bottom=25))
        
        hint_label = arcade.gui.UILabel(
            text="Клик мышью - выбор клетки | Enter - подтвердить ход",
            font_size=18,
            font_name="Arial",
            text_color=(200, 200, 200)
        )
        v_box.add(hint_label.with_space_around(top=40))
        
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=v_box
            )
        )
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.manager.enable()
    
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
