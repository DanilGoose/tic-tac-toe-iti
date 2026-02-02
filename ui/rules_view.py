import arcade
import arcade.gui


class RulesView(arcade.View):
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
            text="Правила игры для исходных настроек",
            font_size=int(32 * scale),
            font_name="Arial",
            text_color=arcade.color.WHITE
        )
        v_box.add(title_label.with_padding(bottom=int(30 * scale)))
        
        rules_text = [
            "• Цель: собрать 5 фигур в ряд",
            "• Ряд может быть горизонтальным, вертикальным или диагональным",
            "• 2 игрока ходят по очереди",
            "• За один ход можно поставить до 3 фигур",
            "• Нельзя ставить фигуру в занятую клетку",
            "• Клик мышью для выбора клетки",
            "• Нажмите 'Подтвердить' для завершения хода",
            "• Если игрок считает, что он победил, то необходимо нажать кнопку 'проверить'",
            "• Игра заканчивается победой или ничьей",
            "• При желании можно изменить настройки игры",
        ]
        
        for rule in rules_text:
            rule_label = arcade.gui.UILabel(
                text=rule,
                font_size=int(16 * scale),
                font_name="Arial",
                text_color=arcade.color.LIGHT_GRAY
            )
            v_box.add(rule_label.with_padding(bottom=int(10 * scale)))
        
        back_button = arcade.gui.UIFlatButton(text="Назад", width=max(160, int(200 * scale)), height=max(40, int(50 * scale)))
        back_button.on_click = self.on_back_click
        v_box.add(back_button.with_padding(top=int(30 * scale)))
        
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
        menu_view = MenuView()
        self.window.show_view(menu_view)
