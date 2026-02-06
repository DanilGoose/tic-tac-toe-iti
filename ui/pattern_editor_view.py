import arcade
import arcade.gui
from ui.fade_view import FadeView


class PatternEditorView(FadeView):
    GRID_SIZE = 7
    CELL_SIZE = 40
    
    def __init__(self, pattern_index: int, pattern_data: dict, on_save_callback):
        super().__init__()
        self.pattern_index = pattern_index
        self.pattern_data = pattern_data
        self.on_save_callback = on_save_callback
        self.manager = arcade.gui.UIManager()
        self.input_bg_texture = None
        
        self.cells = set()
        for x, y in pattern_data.get("cells", []):
            self.cells.add((x, y))
        
        self.grid_offset_x = 0
        self.grid_offset_y = 0
        self.name_input = None
        
        self.setup_ui()
    
    def setup_ui(self):
        self.manager.clear()
        if self.input_bg_texture is None:
            self.input_bg_texture = arcade.make_soft_square_texture(64, (30, 30, 30, 255), 255, 255)
        
        self.grid_offset_x = (self.window.width - self.GRID_SIZE * self.CELL_SIZE) // 2
        self.grid_offset_y = (self.window.height - self.GRID_SIZE * self.CELL_SIZE) // 2 + 30
        
        v_box = arcade.gui.UIBoxLayout()
        
        title_label = arcade.gui.UILabel(
            text="Редактор фигуры",
            font_size=28,
            bold=True,
            text_color=(255, 255, 255)
        )
        v_box.add(title_label.with_padding(bottom=20))
        
        name_box = arcade.gui.UIBoxLayout(vertical=False)
        
        name_label = arcade.gui.UILabel(
            text="Название:",
            font_size=16,
            text_color=(255, 255, 255)
        )
        name_box.add(name_label.with_padding(right=10))
        
        self.name_input = arcade.gui.UIInputText(
            text=self.pattern_data.get("name", "Новая фигура"),
            width=200,
            height=35,
            font_size=16,
            text_color=(255, 255, 255)
        )
        self.name_input.caret.color = (255, 255, 255)
        try:
            self.name_input.layout.selection_color = (80, 80, 80, 200)
        except Exception:
            pass
        name_widget = self.name_input.with_background(texture=self.input_bg_texture).with_border(width=2, color=arcade.color.WHITE)
        name_box.add(name_widget)
        
        v_box.add(name_box.with_padding(bottom=15))
        
        hint_label = arcade.gui.UILabel(
            text="Кликните на клетки чтобы создать фигуру",
            font_size=14,
            text_color=(200, 200, 200)
        )
        v_box.add(hint_label.with_padding(bottom=10))
        
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(v_box, anchor_x="center", anchor_y="top", align_y=-30)
        self.manager.add(anchor)
        
        btn_box = arcade.gui.UIBoxLayout(vertical=False)
        
        save_btn = arcade.gui.UIFlatButton(text="Сохранить", width=120, height=40)
        save_btn.on_click = self.on_save_click
        btn_box.add(save_btn.with_padding(right=15))
        
        clear_btn = arcade.gui.UIFlatButton(text="Очистить", width=120, height=40)
        clear_btn.on_click = self.on_clear_click
        btn_box.add(clear_btn.with_padding(right=15))
        
        cancel_btn = arcade.gui.UIFlatButton(text="Отмена", width=120, height=40)
        cancel_btn.on_click = self.on_cancel_click
        btn_box.add(cancel_btn)
        
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(btn_box, anchor_x="center", anchor_y="bottom", align_y=50)
        self.manager.add(anchor)
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.manager.enable()
        super().on_show_view()
    
    def on_hide_view(self):
        self.manager.disable()
    
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.setup_ui()
    
    def on_draw(self):
        self.clear()
        self.draw_grid()
        self.manager.draw()
        self.draw_fade()
    
    def draw_grid(self):
        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                cell_x = self.grid_offset_x + x * self.CELL_SIZE
                cell_y = self.grid_offset_y + y * self.CELL_SIZE
                
                if (x, y) in self.cells:
                    rect = arcade.Rect.from_kwargs(
                        x=cell_x + self.CELL_SIZE // 2,
                        y=cell_y + self.CELL_SIZE // 2,
                        width=self.CELL_SIZE - 2,
                        height=self.CELL_SIZE - 2
                    )
                    arcade.draw_rect_filled(rect, (0, 200, 100))
                
                outline_rect = arcade.Rect.from_kwargs(
                    x=cell_x + self.CELL_SIZE // 2,
                    y=cell_y + self.CELL_SIZE // 2,
                    width=self.CELL_SIZE - 2,
                    height=self.CELL_SIZE - 2
                )
                arcade.draw_rect_outline(outline_rect, arcade.color.WHITE, 2)
    
    def on_mouse_press(self, x, y, button, modifiers):
        cell_x = (x - self.grid_offset_x) // self.CELL_SIZE
        cell_y = (y - self.grid_offset_y) // self.CELL_SIZE
        
        if 0 <= cell_x < self.GRID_SIZE and 0 <= cell_y < self.GRID_SIZE:
            if self.name_input and getattr(self.name_input, "_active", False):
                self.name_input._active = False
                self.name_input.caret.on_deactivate()
                self.name_input.trigger_full_render()
            cell = (cell_x, cell_y)
            if cell in self.cells:
                self.cells.remove(cell)
            else:
                self.cells.add(cell)
    
    def on_save_click(self, event):
        if not self.cells:
            return
        
        cells_list = list(self.cells)
        min_x = min(x for x, y in cells_list)
        min_y = min(y for x, y in cells_list)
        normalized = [(x - min_x, y - min_y) for x, y in cells_list]
        
        name = self.name_input.text.strip() if self.name_input else "Фигура"
        if not name:
            name = "Фигура"
        
        self.pattern_data["name"] = name
        self.pattern_data["cells"] = normalized
        
        if self.on_save_callback:
            self.on_save_callback(self.pattern_index, self.pattern_data)
        
        from ui.settings_view import SettingsView
        settings_view = SettingsView()
        self.window.show_view_fade(settings_view)
    
    def on_clear_click(self, event):
        self.cells.clear()
    
    def on_cancel_click(self, event):
        from ui.settings_view import SettingsView
        settings_view = SettingsView()
        self.window.show_view_fade(settings_view)
