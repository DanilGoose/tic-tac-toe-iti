import arcade
import arcade.gui


class RulesView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.setup_ui()
    
    def setup_ui(self):
        self.manager.clear()
        
        v_box = arcade.gui.UIBoxLayout()
        
        title_label = arcade.gui.UILabel(
            text="Правила игры",
            font_size=32,
            font_name="Arial",
            text_color=arcade.color.WHITE
        )
        v_box.add(title_label.with_space_around(bottom=30))
        
        rules_text = [
            "• Цель: собрать 5 фигур в ряд",
            "• Ряд может быть горизонтальным, вертикальным или диагональным",
            "• От 2 до 4 игроков ходят по очереди",
            "• За один ход можно поставить до 3 фигур",
            "• Нельзя ставить фигуру в занятую клетку",
            "• Клик мышью для выбора клетки",
            "• Нажмите 'Подтвердить' для завершения хода",
            "• Игра заканчивается победой или ничьей"
        ]
        
        for rule in rules_text:
            rule_label = arcade.gui.UILabel(
                text=rule,
                font_size=16,
                font_name="Arial",
                text_color=arcade.color.LIGHT_GRAY
            )
            v_box.add(rule_label.with_space_around(bottom=10))
        
        back_button = arcade.gui.UIFlatButton(text="Назад", width=200, height=50)
        back_button.on_click = self.on_back_click
        v_box.add(back_button.with_space_around(top=30))
        
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
    
    def on_back_click(self, event):
        from ui.menu_view import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)
