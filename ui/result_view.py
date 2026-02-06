import arcade
import arcade.gui
from game.player import Player
from typing import Optional
from ui.fade_view import FadeView


class ResultView(FadeView):
    def __init__(self, winner: Optional[Player], is_draw: bool, settings: dict):
        super().__init__()
        self.winner = winner
        self.is_draw = is_draw
        self.settings = settings
        self.manager = arcade.gui.UIManager()
        self.setup_ui()
    
    def setup_ui(self):
        self.manager.clear()
        scale = min(self.window.width / 1024, self.window.height / 768)
        scale = max(0.75, min(1.2, scale))
        
        v_box = arcade.gui.UIBoxLayout()
        
        if self.is_draw:
            result_text = "Ничья!"
            result_color = (255, 255, 100)
        else:
            result_text = f"Победил {self.winner.name}!"
            result_color = self.winner.color
        
        result_label = arcade.gui.UILabel(
            text=result_text,
            font_size=int(44 * scale),
            font_name="Arial",
            bold=True,
            text_color=result_color
        )
        v_box.add(result_label.with_padding(bottom=int(30 * scale)))
        
        if not self.is_draw and self.winner:
            figure_label = arcade.gui.UILabel(
                text=self.winner.figure,
                font_size=int(96 * scale),
                text_color=self.winner.color
            )
            v_box.add(figure_label.with_padding(bottom=int(50 * scale)))
        
        btn_width = max(200, int(250 * scale))
        btn_height = max(48, int(60 * scale))
        new_game_btn = arcade.gui.UIFlatButton(text="Новая игра", width=btn_width, height=btn_height)
        new_game_btn.on_click = self.on_new_game_click
        v_box.add(new_game_btn.with_padding(bottom=int(25 * scale)))
        
        menu_btn = arcade.gui.UIFlatButton(text="В главное меню", width=btn_width, height=btn_height)
        menu_btn.on_click = self.on_menu_click
        v_box.add(menu_btn)
        
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(v_box, anchor_x="center", anchor_y="center")
        self.manager.add(anchor)
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.manager.enable()
        super().on_show_view()
    
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.setup_ui()
    
    def on_hide_view(self):
        self.manager.disable()
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.draw_fade()
    
    def on_new_game_click(self, event):
        from ui.game_view import GameView
        game_view = GameView(self.settings)
        self.window.show_view_fade(game_view)
    
    def on_menu_click(self, event):
        from ui.menu_view import MenuView
        menu_view = MenuView()
        self.window.show_view_fade(menu_view)
