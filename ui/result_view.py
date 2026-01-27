import arcade
import arcade.gui
from game.player import Player
from typing import Optional


class ResultView(arcade.View):
    def __init__(self, winner: Optional[Player], is_draw: bool, settings: dict):
        super().__init__()
        self.winner = winner
        self.is_draw = is_draw
        self.settings = settings
        self.manager = arcade.gui.UIManager()
        self.setup_ui()
    
    def setup_ui(self):
        self.manager.clear()
        
        v_box = arcade.gui.UIBoxLayout()
        
        if self.is_draw:
            result_text = "Ничья!"
            result_color = (255, 255, 100)
        else:
            result_text = f"Победил {self.winner.name}!"
            result_color = self.winner.color
        
        result_label = arcade.gui.UILabel(
            text=result_text,
            font_size=44,
            font_name="Arial",
            bold=True,
            text_color=result_color
        )
        v_box.add(result_label.with_space_around(bottom=30))
        
        if not self.is_draw and self.winner:
            figure_label = arcade.gui.UILabel(
                text=self.winner.figure,
                font_size=96,
                text_color=self.winner.color
            )
            v_box.add(figure_label.with_space_around(bottom=50))
        
        new_game_btn = arcade.gui.UIFlatButton(text="Новая игра", width=250, height=60)
        new_game_btn.on_click = self.on_new_game_click
        v_box.add(new_game_btn.with_space_around(bottom=25))
        
        menu_btn = arcade.gui.UIFlatButton(text="В главное меню", width=250, height=60)
        menu_btn.on_click = self.on_menu_click
        v_box.add(menu_btn)
        
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
    
    def on_new_game_click(self, event):
        from ui.game_view import GameView
        game_view = GameView(self.settings)
        self.window.show_view(game_view)
    
    def on_menu_click(self, event):
        from ui.menu_view import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)
