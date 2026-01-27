import arcade
import arcade.gui
from game.player import AVAILABLE_FIGURES, AVAILABLE_COLORS, COLOR_NAMES


class SettingsView(arcade.View):
    MAX_VISIBLE_PATTERNS = 5
    
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.width_label = None
        self.height_label = None
        self.player_count_label = None
        self.player_settings = []
        self.error_label = None
        self.dropdown_active = False
        self.dropdown_type = None
        self.dropdown_player_index = None
        self.dropdown_items = []
        self.dropdown_rects = []
        self.pattern_scroll_offset = 0
        self.input_bg_texture = None
    
    def setup_ui(self):
        self.manager.clear()
        self.player_settings = []
        
        settings = self.window.game_settings
        if self.input_bg_texture is None:
            self.input_bg_texture = arcade.make_soft_square_texture(64, (30, 30, 30, 255), 255, 255)
        
        main_box = arcade.gui.UIBoxLayout()
        
        title_label = arcade.gui.UILabel(
            text="Настройки",
            font_size=40,
            font_name="Arial",
            bold=True,
            text_color=(255, 255, 255)
        )
        main_box.add(title_label.with_space_around(bottom=40))
        
        width_box = arcade.gui.UIBoxLayout(vertical=False)
        
        width_text = arcade.gui.UILabel(
            text="Ширина:",
            font_size=20,
            text_color=(255, 255, 255)
        )
        width_box.add(width_text.with_space_around(right=15))
        
        width_minus = arcade.gui.UIFlatButton(text="-", width=45, height=35)
        width_minus.on_click = self.on_decrease_width
        width_box.add(width_minus.with_space_around(right=10))
        
        self.width_label = arcade.gui.UILabel(
            text=str(settings["width"]),
            font_size=22,
            text_color=(255, 255, 100)
        )
        width_box.add(self.width_label.with_space_around(right=10))
        
        width_plus = arcade.gui.UIFlatButton(text="+", width=45, height=35)
        width_plus.on_click = self.on_increase_width
        width_box.add(width_plus)
        
        main_box.add(width_box.with_space_around(bottom=15))
        
        height_box = arcade.gui.UIBoxLayout(vertical=False)
        
        height_text = arcade.gui.UILabel(
            text="Высота:",
            font_size=20,
            text_color=(255, 255, 255)
        )
        height_box.add(height_text.with_space_around(right=15))
        
        height_minus = arcade.gui.UIFlatButton(text="-", width=45, height=35)
        height_minus.on_click = self.on_decrease_height
        height_box.add(height_minus.with_space_around(right=10))
        
        self.height_label = arcade.gui.UILabel(
            text=str(settings["height"]),
            font_size=22,
            text_color=(255, 255, 100)
        )
        height_box.add(self.height_label.with_space_around(right=10))
        
        height_plus = arcade.gui.UIFlatButton(text="+", width=45, height=35)
        height_plus.on_click = self.on_increase_height
        height_box.add(height_plus)
        
        main_box.add(height_box.with_space_around(bottom=20))
        
        players_box = arcade.gui.UIBoxLayout(vertical=False)
        
        players_label = arcade.gui.UILabel(
            text="Игроков:",
            font_size=20,
            text_color=(255, 255, 255)
        )
        players_box.add(players_label.with_space_around(right=15))
        
        minus_btn = arcade.gui.UIFlatButton(text="-", width=45, height=35)
        minus_btn.on_click = self.on_decrease_players
        players_box.add(minus_btn.with_space_around(right=10))
        
        self.player_count_label = arcade.gui.UILabel(
            text=str(settings["player_count"]),
            font_size=22,
            text_color=(255, 255, 100)
        )
        players_box.add(self.player_count_label.with_space_around(right=10))
        
        plus_btn = arcade.gui.UIFlatButton(text="+", width=45, height=35)
        plus_btn.on_click = self.on_increase_players
        players_box.add(plus_btn)
        
        main_box.add(players_box.with_space_around(bottom=20))
        
        hide_board_box = arcade.gui.UIBoxLayout(vertical=False)
        
        hide_board_label = arcade.gui.UILabel(
            text="Скрывать доску после победы:",
            font_size=18,
            text_color=(255, 255, 255)
        )
        hide_board_box.add(hide_board_label.with_space_around(right=15))
        
        hide_board_value = settings.get("hide_board_on_win", True)
        self.hide_board_btn = arcade.gui.UIFlatButton(
            text="Да" if hide_board_value else "Нет",
            width=80,
            height=35
        )
        self.hide_board_btn.on_click = self.on_toggle_hide_board
        hide_board_box.add(self.hide_board_btn)
        
        main_box.add(hide_board_box.with_space_around(bottom=25))
        
        player_config_label = arcade.gui.UILabel(
            text="Настройки игроков:",
            font_size=22,
            bold=True,
            text_color=(255, 255, 255)
        )
        main_box.add(player_config_label.with_space_around(bottom=15))
        
        for i in range(4):
            player_box = arcade.gui.UIBoxLayout(vertical=False)
            
            num_label = arcade.gui.UILabel(
                text=f"{i + 1}.",
                font_size=18,
                text_color=(200, 200, 200)
            )
            player_box.add(num_label.with_space_around(right=10))
            
            name_input = arcade.gui.UIInputText(
                text=settings["players"][i].get("name", f"Игрок {i + 1}"),
                width=140,
                height=40,
                font_size=18,
                text_color=(255, 255, 255)
            )
            name_input.caret.color = (255, 255, 255)
            try:
                name_input.layout.selection_color = (80, 80, 80, 200)
            except Exception:
                pass
            name_input.player_index = i
            name_widget = name_input.with_background(self.input_bg_texture, 4, 6, 4, 6).with_border(2, arcade.color.WHITE)
            player_box.add(name_widget.with_space_around(right=15))
            
            figure_btn = arcade.gui.UIFlatButton(
                text=settings["players"][i]["figure"],
                width=50,
                height=35
            )
            figure_btn.player_index = i
            figure_btn.on_click = self.on_open_figure_dropdown
            player_box.add(figure_btn.with_space_around(right=10))
            
            color = settings["players"][i]["color"]
            color_btn = arcade.gui.UIFlatButton(
                text=COLOR_NAMES.get(color, "?"),
                width=110,
                height=35
            )
            color_btn.player_index = i
            color_btn.on_click = self.on_open_color_dropdown
            player_box.add(color_btn)
            
            self.player_settings.append({
                "box": player_box,
                "name_input": name_input,
                "figure_btn": figure_btn,
                "color_btn": color_btn
            })
            
            main_box.add(player_box.with_space_around(bottom=12))
        
        patterns = settings.get("win_patterns", [])
        total_patterns = len(patterns)
        
        pattern_header = arcade.gui.UIBoxLayout(vertical=False)
        pattern_label = arcade.gui.UILabel(
            text=f"Фигуры ({total_patterns}):",
            font_size=20,
            bold=True,
            text_color=(255, 255, 255)
        )
        pattern_header.add(pattern_label.with_space_around(right=15))
        
        if total_patterns > self.MAX_VISIBLE_PATTERNS:
            prev_btn = arcade.gui.UIFlatButton(text="▲", width=30, height=25)
            prev_btn.on_click = self.on_pattern_scroll_up
            pattern_header.add(prev_btn.with_space_around(right=5))
            
            next_btn = arcade.gui.UIFlatButton(text="▼", width=30, height=25)
            next_btn.on_click = self.on_pattern_scroll_down
            pattern_header.add(next_btn)
        
        main_box.add(pattern_header.with_space_around(top=10, bottom=8))
        
        self.pattern_buttons = []
        start_idx = self.pattern_scroll_offset
        end_idx = min(start_idx + self.MAX_VISIBLE_PATTERNS, total_patterns)
        
        for i in range(start_idx, end_idx):
            pattern = patterns[i]
            pattern_box = arcade.gui.UIBoxLayout(vertical=False)
            
            toggle_btn = arcade.gui.UIFlatButton(
                text="✓" if pattern.get("enabled", True) else "✗",
                width=35,
                height=28
            )
            toggle_btn.pattern_index = i
            toggle_btn.on_click = self.on_toggle_pattern
            pattern_box.add(toggle_btn.with_space_around(right=8))
            
            name_text = pattern.get("name", f"Фигура {i+1}")
            if len(name_text) > 12:
                name_text = name_text[:10] + ".."
            name_label = arcade.gui.UILabel(
                text=name_text,
                font_size=14,
                text_color=(255, 255, 255)
            )
            pattern_box.add(name_label.with_space_around(right=10))
            
            edit_btn = arcade.gui.UIFlatButton(text="✎", width=30, height=28)
            edit_btn.pattern_index = i
            edit_btn.on_click = self.on_edit_pattern
            pattern_box.add(edit_btn.with_space_around(right=5))
            
            if total_patterns > 1:
                delete_btn = arcade.gui.UIFlatButton(text="✗", width=30, height=28)
                delete_btn.pattern_index = i
                delete_btn.on_click = self.on_delete_pattern
                pattern_box.add(delete_btn)
            
            self.pattern_buttons.append({
                "toggle_btn": toggle_btn,
                "name_label": name_label,
                "index": i
            })
            
            main_box.add(pattern_box.with_space_around(bottom=5))
        
        add_pattern_btn = arcade.gui.UIFlatButton(text="+ Добавить", width=120, height=30)
        add_pattern_btn.on_click = self.on_add_pattern
        main_box.add(add_pattern_btn.with_space_around(bottom=8))
        
        self.error_label = arcade.gui.UILabel(
            text="",
            font_size=18,
            text_color=arcade.color.RED
        )
        main_box.add(self.error_label.with_space_around(bottom=15))
        
        buttons_box = arcade.gui.UIBoxLayout(vertical=False)
        
        save_button = arcade.gui.UIFlatButton(text="Сохранить", width=160, height=55)
        save_button.on_click = self.on_save_click
        buttons_box.add(save_button.with_space_around(right=25))
        
        back_button = arcade.gui.UIFlatButton(text="Назад", width=160, height=55)
        back_button.on_click = self.on_back_click
        buttons_box.add(back_button)
        
        main_box.add(buttons_box.with_space_around(top=20))
        
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=main_box
            )
        )
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.setup_ui()
        self.manager.enable()
    
    def on_hide_view(self):
        self.manager.disable()
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.draw_dropdown()
    
    def draw_dropdown(self):
        if not self.dropdown_active:
            return
        
        self.dropdown_rects = []
        start_x = self.window.width // 2
        start_y = self.window.height // 2
        item_height = 30
        item_width = 120
        
        for i, item in enumerate(self.dropdown_items):
            rect_y = start_y - i * item_height
            self.dropdown_rects.append((start_x - item_width // 2, rect_y - item_height // 2, item_width, item_height))
            
            arcade.draw_rectangle_filled(
                start_x, rect_y,
                item_width, item_height,
                arcade.color.DARK_GRAY
            )
            arcade.draw_rectangle_outline(
                start_x, rect_y,
                item_width, item_height,
                arcade.color.WHITE, 1
            )
            
            if self.dropdown_type == "figure":
                arcade.draw_text(
                    item, start_x, rect_y,
                    arcade.color.WHITE, 16,
                    anchor_x="center", anchor_y="center"
                )
            else:
                color_tuple = item
                arcade.draw_rectangle_filled(
                    start_x - 30, rect_y, 20, 20, color_tuple
                )
                arcade.draw_text(
                    COLOR_NAMES.get(color_tuple, "?"),
                    start_x + 10, rect_y,
                    arcade.color.WHITE, 12,
                    anchor_x="center", anchor_y="center"
                )
    
    def on_mouse_press(self, x, y, button, modifiers):
        target_input = None
        for ps in self.player_settings:
            inp = ps.get("name_input")
            if inp and inp.rect.collide_with_point(x, y):
                target_input = inp
                break
        self.deactivate_other_inputs(target_input)

        if self.dropdown_active:
            for i, (rx, ry, rw, rh) in enumerate(self.dropdown_rects):
                if rx <= x <= rx + rw and ry <= y <= ry + rh:
                    self.select_dropdown_item(i)
                    return
            self.dropdown_active = False
            return

    def deactivate_other_inputs(self, keep_input):
        for ps in self.player_settings:
            inp = ps.get("name_input")
            if not inp or inp is keep_input:
                continue
            if getattr(inp, "_active", False):
                inp._active = False
                inp.caret.on_deactivate()
                inp.trigger_full_render()
    
    def select_dropdown_item(self, index):
        settings = self.window.game_settings
        player_idx = self.dropdown_player_index
        
        if self.dropdown_type == "figure":
            new_figure = self.dropdown_items[index]
            settings["players"][player_idx]["figure"] = new_figure
            self.player_settings[player_idx]["figure_btn"].text = new_figure
        else:
            new_color = self.dropdown_items[index]
            settings["players"][player_idx]["color"] = new_color
            self.player_settings[player_idx]["color_btn"].text = COLOR_NAMES.get(new_color, "?")
        
        self.dropdown_active = False
        self.error_label.text = ""
    
    def get_used_figures(self, exclude_player: int):
        settings = self.window.game_settings
        used = set()
        for i in range(settings["player_count"]):
            if i != exclude_player:
                used.add(settings["players"][i]["figure"])
        return used
    
    def get_used_colors(self, exclude_player: int):
        settings = self.window.game_settings
        used = set()
        for i in range(settings["player_count"]):
            if i != exclude_player:
                used.add(settings["players"][i]["color"])
        return used
    
    def on_open_figure_dropdown(self, event):
        btn = event.source
        idx = btn.player_index
        used = self.get_used_figures(idx)
        available = [f for f in AVAILABLE_FIGURES if f not in used]
        
        if not available:
            return
        
        self.dropdown_active = True
        self.dropdown_type = "figure"
        self.dropdown_player_index = idx
        self.dropdown_items = available
    
    def on_open_color_dropdown(self, event):
        btn = event.source
        idx = btn.player_index
        used = self.get_used_colors(idx)
        available = [c for c in AVAILABLE_COLORS if c not in used]
        
        if not available:
            return
        
        self.dropdown_active = True
        self.dropdown_type = "color"
        self.dropdown_player_index = idx
        self.dropdown_items = available
    
    def on_decrease_width(self, event):
        settings = self.window.game_settings
        if settings["width"] > 5:
            settings["width"] -= 1
            self.width_label.text = str(settings["width"])
    
    def on_increase_width(self, event):
        settings = self.window.game_settings
        if settings["width"] < 30:
            settings["width"] += 1
            self.width_label.text = str(settings["width"])
    
    def on_decrease_height(self, event):
        settings = self.window.game_settings
        if settings["height"] > 5:
            settings["height"] -= 1
            self.height_label.text = str(settings["height"])
    
    def on_increase_height(self, event):
        settings = self.window.game_settings
        if settings["height"] < 30:
            settings["height"] += 1
            self.height_label.text = str(settings["height"])
    
    def on_decrease_players(self, event):
        settings = self.window.game_settings
        if settings["player_count"] > 2:
            settings["player_count"] -= 1
            self.player_count_label.text = str(settings["player_count"])
            self.error_label.text = ""
    
    def on_increase_players(self, event):
        settings = self.window.game_settings
        if settings["player_count"] < 4:
            settings["player_count"] += 1
            self.player_count_label.text = str(settings["player_count"])
            self.ensure_unique_settings()
    
    def on_toggle_hide_board(self, event):
        settings = self.window.game_settings
        settings["hide_board_on_win"] = not settings.get("hide_board_on_win", True)
        self.hide_board_btn.text = "Да" if settings["hide_board_on_win"] else "Нет"
    
    def on_toggle_pattern(self, event):
        idx = event.source.pattern_index
        settings = self.window.game_settings
        patterns = settings.get("win_patterns", [])
        if idx < len(patterns):
            patterns[idx]["enabled"] = not patterns[idx].get("enabled", True)
            self.pattern_buttons[idx]["toggle_btn"].text = "✓" if patterns[idx]["enabled"] else "✗"
    
    def on_edit_pattern(self, event):
        idx = event.source.pattern_index
        settings = self.window.game_settings
        patterns = settings.get("win_patterns", [])
        if idx < len(patterns):
            from ui.pattern_editor_view import PatternEditorView
            editor = PatternEditorView(idx, patterns[idx].copy(), self.save_pattern)
            self.window.show_view(editor)
    
    def on_pattern_scroll_up(self, event):
        if self.pattern_scroll_offset > 0:
            self.pattern_scroll_offset -= 1
            self.setup_ui()
    
    def on_pattern_scroll_down(self, event):
        settings = self.window.game_settings
        patterns = settings.get("win_patterns", [])
        max_offset = max(0, len(patterns) - self.MAX_VISIBLE_PATTERNS)
        if self.pattern_scroll_offset < max_offset:
            self.pattern_scroll_offset += 1
            self.setup_ui()
    
    def on_delete_pattern(self, event):
        idx = event.source.pattern_index
        settings = self.window.game_settings
        patterns = settings.get("win_patterns", [])
        if idx < len(patterns) and len(patterns) > 1:
            patterns.pop(idx)
            max_offset = max(0, len(patterns) - self.MAX_VISIBLE_PATTERNS)
            if self.pattern_scroll_offset > max_offset:
                self.pattern_scroll_offset = max_offset
            self.setup_ui()
    
    def on_add_pattern(self, event):
        settings = self.window.game_settings
        patterns = settings.get("win_patterns", [])
        new_pattern = {
            "name": f"Фигура {len(patterns) + 1}",
            "enabled": True,
            "cells": [(0, 0), (1, 0), (2, 0)]
        }
        from ui.pattern_editor_view import PatternEditorView
        editor = PatternEditorView(len(patterns), new_pattern, self.save_pattern)
        self.window.show_view(editor)
    
    def save_pattern(self, index: int, pattern_data: dict):
        settings = self.window.game_settings
        patterns = settings.get("win_patterns", [])
        if index < len(patterns):
            patterns[index] = pattern_data
        else:
            patterns.append(pattern_data)
    
    def ensure_unique_settings(self):
        settings = self.window.game_settings
        player_count = settings["player_count"]
        
        used_figures = set()
        used_colors = set()
        
        for i in range(player_count):
            current_figure = settings["players"][i]["figure"]
            current_color = settings["players"][i]["color"]
            
            if current_figure in used_figures:
                for fig in AVAILABLE_FIGURES:
                    if fig not in used_figures:
                        settings["players"][i]["figure"] = fig
                        self.player_settings[i]["figure_btn"].text = fig
                        break
            used_figures.add(settings["players"][i]["figure"])
            
            if current_color in used_colors:
                for col in AVAILABLE_COLORS:
                    if col not in used_colors:
                        settings["players"][i]["color"] = col
                        self.player_settings[i]["color_btn"].text = COLOR_NAMES.get(col, "?")
                        break
            used_colors.add(settings["players"][i]["color"])
    
    def validate_unique(self) -> bool:
        settings = self.window.game_settings
        player_count = settings["player_count"]
        
        figures = []
        colors = []
        
        for i in range(player_count):
            figures.append(settings["players"][i]["figure"])
            colors.append(settings["players"][i]["color"])
        
        if len(figures) != len(set(figures)):
            self.error_label.text = "Фигуры игроков должны быть уникальными!"
            return False
        
        if len(colors) != len(set(colors)):
            self.error_label.text = "Цвета игроков должны быть уникальными!"
            return False
        
        return True
    
    def on_save_click(self, event):
        if not self.validate_unique():
            return
        
        settings = self.window.game_settings
        for i in range(4):
            name = self.player_settings[i]["name_input"].text.strip()
            if name:
                settings["players"][i]["name"] = name
            else:
                settings["players"][i]["name"] = f"Игрок {i + 1}"
        
        from ui.menu_view import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)
    
    def on_back_click(self, event):
        from ui.menu_view import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)
