import arcade
import arcade.gui
from game.board import MIN_BOARD_SIZE, MAX_BOARD_SIZE
from game.player import AVAILABLE_FIGURES, AVAILABLE_COLORS, COLOR_NAMES, MAX_PLAYERS


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
        self.dropdown_anchor = None
        self.pattern_scroll_offset = 0
        self.input_bg_texture = None
    
    def setup_ui(self):
        self.manager.clear()
        self.player_settings = []
        
        settings = self.window.game_settings
        self.ensure_players_capacity()
        if self.input_bg_texture is None:
            self.input_bg_texture = arcade.make_soft_square_texture(64, (30, 30, 30, 255), 255, 255)
        
        scale = self.get_scale()
        title_size = int(40 * scale)
        header_size = int(22 * scale)
        label_size = int(20 * scale)
        small_label_size = int(18 * scale)
        tiny_label_size = int(14 * scale)
        btn_height = max(30, int(35 * scale))
        small_btn_width = max(40, int(45 * scale))
        input_height = max(30, int(40 * scale))
        row_spacing = max(6, int(12 * scale))
        section_spacing = max(12, int(20 * scale))
        
        player_count = settings["player_count"]
        player_columns = self.get_player_columns(player_count)
        name_width = max(110, int(150 * scale))
        figure_width = max(44, int(50 * scale))
        color_width = max(95, int(110 * scale))
        if player_columns == 2:
            name_width = max(100, int(130 * scale))
            color_width = max(90, int(100 * scale))
        
        self.dropdown_item_height = max(24, int(30 * scale))
        self.dropdown_figure_width = max(48, int(60 * scale))
        self.dropdown_color_width = max(120, int(150 * scale))
        self.dropdown_gap = max(4, int(6 * scale))
        
        main_box = arcade.gui.UIBoxLayout()
        
        title_label = arcade.gui.UILabel(
            text="Настройки",
            font_size=title_size,
            font_name="Arial",
            bold=True,
            text_color=(255, 255, 255)
        )
        main_box.add(title_label.with_padding(bottom=section_spacing * 2))
        
        width_box = arcade.gui.UIBoxLayout(vertical=False)
        
        width_text = arcade.gui.UILabel(
            text="Ширина:",
            font_size=label_size,
            text_color=(255, 255, 255)
        )
        width_box.add(width_text.with_padding(right=15))
        
        width_minus = arcade.gui.UIFlatButton(text="-", width=small_btn_width, height=btn_height)
        width_minus.on_click = self.on_decrease_width
        width_box.add(width_minus.with_padding(right=10))
        
        self.width_label = arcade.gui.UILabel(
            text=str(settings["width"]),
            font_size=label_size,
            text_color=(255, 255, 100)
        )
        width_box.add(self.width_label.with_padding(right=10))
        
        width_plus = arcade.gui.UIFlatButton(text="+", width=small_btn_width, height=btn_height)
        width_plus.on_click = self.on_increase_width
        width_box.add(width_plus)
        
        main_box.add(width_box.with_padding(bottom=row_spacing))
        
        height_box = arcade.gui.UIBoxLayout(vertical=False)
        
        height_text = arcade.gui.UILabel(
            text="Высота:",
            font_size=label_size,
            text_color=(255, 255, 255)
        )
        height_box.add(height_text.with_padding(right=15))
        
        height_minus = arcade.gui.UIFlatButton(text="-", width=small_btn_width, height=btn_height)
        height_minus.on_click = self.on_decrease_height
        height_box.add(height_minus.with_padding(right=10))
        
        self.height_label = arcade.gui.UILabel(
            text=str(settings["height"]),
            font_size=label_size,
            text_color=(255, 255, 100)
        )
        height_box.add(self.height_label.with_padding(right=10))
        
        height_plus = arcade.gui.UIFlatButton(text="+", width=small_btn_width, height=btn_height)
        height_plus.on_click = self.on_increase_height
        height_box.add(height_plus)
        
        main_box.add(height_box.with_padding(bottom=section_spacing))
        
        players_box = arcade.gui.UIBoxLayout(vertical=False)
        
        players_label = arcade.gui.UILabel(
            text="Игроков:",
            font_size=label_size,
            text_color=(255, 255, 255)
        )
        players_box.add(players_label.with_padding(right=15))
        
        minus_btn = arcade.gui.UIFlatButton(text="-", width=small_btn_width, height=btn_height)
        minus_btn.on_click = self.on_decrease_players
        players_box.add(minus_btn.with_padding(right=10))
        
        self.player_count_label = arcade.gui.UILabel(
            text=str(settings["player_count"]),
            font_size=label_size,
            text_color=(255, 255, 100)
        )
        players_box.add(self.player_count_label.with_padding(right=10))
        
        plus_btn = arcade.gui.UIFlatButton(text="+", width=small_btn_width, height=btn_height)
        plus_btn.on_click = self.on_increase_players
        players_box.add(plus_btn)
        
        main_box.add(players_box.with_padding(bottom=section_spacing))
        
        hide_board_box = arcade.gui.UIBoxLayout(vertical=False)
        
        hide_board_label = arcade.gui.UILabel(
            text="Скрывать доску после победы:",
            font_size=small_label_size,
            text_color=(255, 255, 255)
        )
        hide_board_box.add(hide_board_label.with_padding(right=15))
        
        hide_board_value = settings.get("hide_board_on_win", True)
        self.hide_board_btn = arcade.gui.UIFlatButton(
            text="Да" if hide_board_value else "Нет",
            width=max(70, int(80 * scale)),
            height=btn_height
        )
        self.hide_board_btn.on_click = self.on_toggle_hide_board
        hide_board_box.add(self.hide_board_btn)
        
        main_box.add(hide_board_box.with_padding(bottom=section_spacing))
        
        player_config_label = arcade.gui.UILabel(
            text="Настройки игроков:",
            font_size=header_size,
            bold=True,
            text_color=(255, 255, 255)
        )
        main_box.add(player_config_label.with_padding(bottom=row_spacing))
        
        players_container = arcade.gui.UIBoxLayout(vertical=False)
        column_boxes = [arcade.gui.UIBoxLayout() for _ in range(player_columns)]
        players_per_col = (player_count + player_columns - 1) // player_columns
        
        for i in range(player_count):
            player_box = arcade.gui.UIBoxLayout(vertical=False)
            
            num_label = arcade.gui.UILabel(
                text=f"{i + 1}.",
                font_size=small_label_size,
                text_color=(200, 200, 200)
            )
            player_box.add(num_label.with_padding(right=10))
            
            name_input = arcade.gui.UIInputText(
                text=settings["players"][i].get("name", f"Игрок {i + 1}"),
                width=name_width,
                height=input_height,
                font_size=small_label_size,
                text_color=(255, 255, 255)
            )
            name_input.caret.color = (255, 255, 255)
            try:
                name_input.layout.selection_color = (80, 80, 80, 200)
            except Exception:
                pass
            name_input.player_index = i
            name_widget = name_input.with_background(texture=self.input_bg_texture).with_border(width=2, color=arcade.color.WHITE)
            player_box.add(name_widget.with_padding(right=15))
            
            figure_btn = arcade.gui.UIFlatButton(
                text=settings["players"][i]["figure"],
                width=figure_width,
                height=btn_height
            )
            figure_btn.player_index = i
            figure_btn.on_click = self.on_open_figure_dropdown
            player_box.add(figure_btn.with_padding(right=10))
            
            color = settings["players"][i]["color"]
            color_btn = arcade.gui.UIFlatButton(
                text=COLOR_NAMES.get(color, "?"),
                width=color_width,
                height=btn_height
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
            column_index = min(i // players_per_col, player_columns - 1)
            column_boxes[column_index].add(player_box.with_padding(bottom=row_spacing))
        
        for idx, col in enumerate(column_boxes):
            if idx < player_columns - 1:
                players_container.add(col.with_padding(right=section_spacing))
            else:
                players_container.add(col)
        
        main_box.add(players_container.with_padding(bottom=section_spacing))
        
        patterns = settings.get("win_patterns", [])
        total_patterns = len(patterns)
        
        pattern_header = arcade.gui.UIBoxLayout(vertical=False)
        pattern_label = arcade.gui.UILabel(
            text=f"Фигуры ({total_patterns}):",
            font_size=label_size,
            bold=True,
            text_color=(255, 255, 255)
        )
        pattern_header.add(pattern_label.with_padding(right=15))
        
        if total_patterns > self.MAX_VISIBLE_PATTERNS:
            prev_btn = arcade.gui.UIFlatButton(text="▲", width=max(26, int(30 * scale)), height=max(22, int(25 * scale)))
            prev_btn.on_click = self.on_pattern_scroll_up
            pattern_header.add(prev_btn.with_padding(right=5))
            
            next_btn = arcade.gui.UIFlatButton(text="▼", width=max(26, int(30 * scale)), height=max(22, int(25 * scale)))
            next_btn.on_click = self.on_pattern_scroll_down
            pattern_header.add(next_btn)
        
        main_box.add(pattern_header.with_padding(top=row_spacing, bottom=row_spacing))
        
        self.pattern_buttons = []
        start_idx = self.pattern_scroll_offset
        end_idx = min(start_idx + self.MAX_VISIBLE_PATTERNS, total_patterns)
        
        for i in range(start_idx, end_idx):
            pattern = patterns[i]
            pattern_box = arcade.gui.UIBoxLayout(vertical=False)
            
            toggle_btn = arcade.gui.UIFlatButton(
                text="✓" if pattern.get("enabled", True) else "✗",
                width=max(30, int(35 * scale)),
                height=max(24, int(28 * scale))
            )
            toggle_btn.pattern_index = i
            toggle_btn.on_click = self.on_toggle_pattern
            pattern_box.add(toggle_btn.with_padding(right=8))
            
            name_text = pattern.get("name", f"Фигура {i+1}")
            if len(name_text) > 12:
                name_text = name_text[:10] + ".."
            name_label = arcade.gui.UILabel(
                text=name_text,
                font_size=tiny_label_size,
                text_color=(255, 255, 255)
            )
            pattern_box.add(name_label.with_padding(right=10))
            
            edit_btn = arcade.gui.UIFlatButton(text="✎", width=max(26, int(30 * scale)), height=max(24, int(28 * scale)))
            edit_btn.pattern_index = i
            edit_btn.on_click = self.on_edit_pattern
            pattern_box.add(edit_btn.with_padding(right=5))
            
            if total_patterns > 1:
                delete_btn = arcade.gui.UIFlatButton(text="✗", width=max(26, int(30 * scale)), height=max(24, int(28 * scale)))
                delete_btn.pattern_index = i
                delete_btn.on_click = self.on_delete_pattern
                pattern_box.add(delete_btn)
            
            self.pattern_buttons.append({
                "toggle_btn": toggle_btn,
                "name_label": name_label,
                "index": i
            })
            
            main_box.add(pattern_box.with_padding(bottom=max(4, int(6 * scale))))
        
        add_pattern_btn = arcade.gui.UIFlatButton(text="+ Добавить", width=max(110, int(120 * scale)), height=max(26, int(30 * scale)))
        add_pattern_btn.on_click = self.on_add_pattern
        main_box.add(add_pattern_btn.with_padding(bottom=row_spacing))
        
        self.error_label = arcade.gui.UILabel(
            text="",
            font_size=small_label_size,
            text_color=arcade.color.RED
        )
        main_box.add(self.error_label.with_padding(bottom=section_spacing))
        
        buttons_box = arcade.gui.UIBoxLayout(vertical=False)
        
        save_button = arcade.gui.UIFlatButton(text="Сохранить", width=max(140, int(160 * scale)), height=max(45, int(55 * scale)))
        save_button.on_click = self.on_save_click
        buttons_box.add(save_button.with_padding(right=25))
        
        back_button = arcade.gui.UIFlatButton(text="Назад", width=max(140, int(160 * scale)), height=max(45, int(55 * scale)))
        back_button.on_click = self.on_back_click
        buttons_box.add(back_button)
        
        main_box.add(buttons_box.with_padding(top=section_spacing))
        
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(main_box, anchor_x="center", anchor_y="center")
        self.manager.add(anchor)
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.setup_ui()
        self.manager.enable()
    
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.dropdown_active = False
        self.setup_ui()
    
    def on_hide_view(self):
        self.manager.disable()
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.draw_dropdown()
    
    def draw_dropdown(self):
        if not self.dropdown_active or not self.dropdown_items or self.dropdown_anchor is None:
            return
        
        self.dropdown_rects = []
        anchor_x, anchor_y = self.dropdown_anchor
        item_height = self.dropdown_item_height
        gap = self.dropdown_gap
        item_width = self.dropdown_figure_width if self.dropdown_type == "figure" else self.dropdown_color_width
        
        total_height_single = len(self.dropdown_items) * item_height + max(0, len(self.dropdown_items) - 1) * gap
        max_height = min(self.window.height * 0.6, total_height_single)
        columns = 1
        if total_height_single > max_height:
            columns = int(total_height_single // max_height) + 1
        columns = max(1, min(columns, len(self.dropdown_items)))
        rows = (len(self.dropdown_items) + columns - 1) // columns
        
        total_height = rows * item_height + max(0, rows - 1) * gap
        total_width = columns * item_width + max(0, columns - 1) * gap
        
        margin = 10
        top_y = anchor_y
        if top_y - total_height < margin:
            top_y = min(self.window.height - margin, anchor_y + total_height)
        
        left_x = anchor_x - total_width / 2
        if left_x < margin:
            left_x = margin
        if left_x + total_width > self.window.width - margin:
            left_x = self.window.width - margin - total_width
        
        for i, item in enumerate(self.dropdown_items):
            col = i % columns
            row = i // columns
            center_x = left_x + col * (item_width + gap) + item_width / 2
            center_y = top_y - row * (item_height + gap) - item_height / 2
            self.dropdown_rects.append((center_x - item_width / 2, center_y - item_height / 2, item_width, item_height))
            
            rect = arcade.Rect.from_kwargs(x=center_x, y=center_y, width=item_width, height=item_height)
            arcade.draw_rect_filled(rect, arcade.color.DARK_GRAY)
            arcade.draw_rect_outline(rect, arcade.color.WHITE, 1)
            
            if self.dropdown_type == "figure":
                arcade.draw_text(
                    item, center_x, center_y,
                    arcade.color.WHITE, int(item_height * 0.6),
                    anchor_x="center", anchor_y="center"
                )
            else:
                color_tuple = item
                swatch_rect = arcade.Rect.from_kwargs(
                    x=center_x - item_width / 2 + 14,
                    y=center_y,
                    width=16,
                    height=16
                )
                arcade.draw_rect_filled(swatch_rect, color_tuple)
                arcade.draw_text(
                    COLOR_NAMES.get(color_tuple, "?"),
                    center_x + 10, center_y,
                    arcade.color.WHITE, int(item_height * 0.45),
                    anchor_x="center", anchor_y="center"
                )

    def get_scale(self):
        scale = min(self.window.width / 1024, self.window.height / 768)
        return max(0.75, min(1.2, scale))

    def get_player_columns(self, player_count: int):
        if self.window.width >= 1100:
            return 2
        if self.window.width >= 900 and player_count > 6:
            return 2
        return 1

    def ensure_players_capacity(self):
        settings = self.window.game_settings
        settings["player_count"] = max(2, min(MAX_PLAYERS, settings.get("player_count", 2)))
        players = settings.get("players", [])
        for i in range(len(players), MAX_PLAYERS):
            players.append({
                "name": f"Игрок {i + 1}",
                "figure": AVAILABLE_FIGURES[i],
                "color": AVAILABLE_COLORS[i]
            })
        for i in range(MAX_PLAYERS):
            if not players[i].get("name"):
                players[i]["name"] = f"Игрок {i + 1}"
            if players[i].get("figure") not in AVAILABLE_FIGURES:
                players[i]["figure"] = AVAILABLE_FIGURES[i % len(AVAILABLE_FIGURES)]
            if players[i].get("color") not in AVAILABLE_COLORS:
                players[i]["color"] = AVAILABLE_COLORS[i % len(AVAILABLE_COLORS)]
        settings["players"] = players
        self.ensure_unique_settings(update_ui=False)
    
    def on_mouse_press(self, x, y, button, modifiers):
        target_input = None
        for ps in self.player_settings:
            inp = ps.get("name_input")
            if inp and inp.rect.point_in_rect(x, y):
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
            other_idx = self.apply_unique_value(player_idx, "figure", new_figure)
            self.player_settings[player_idx]["figure_btn"].text = new_figure
            if other_idx is not None:
                self.player_settings[other_idx]["figure_btn"].text = settings["players"][other_idx]["figure"]
        else:
            new_color = self.dropdown_items[index]
            other_idx = self.apply_unique_value(player_idx, "color", new_color)
            self.player_settings[player_idx]["color_btn"].text = COLOR_NAMES.get(new_color, "?")
            if other_idx is not None:
                other_color = settings["players"][other_idx]["color"]
                self.player_settings[other_idx]["color_btn"].text = COLOR_NAMES.get(other_color, "?")
        
        self.dropdown_active = False
        self.error_label.text = ""

    def apply_unique_value(self, player_idx, key, new_value):
        settings = self.window.game_settings
        player_count = settings["player_count"]
        players = settings["players"]
        old_value = players[player_idx][key]
        if new_value == old_value:
            return None
        other_idx = None
        for i in range(player_count):
            if i != player_idx and players[i][key] == new_value:
                other_idx = i
                break
        players[player_idx][key] = new_value
        if other_idx is not None:
            players[other_idx][key] = old_value
        return other_idx
    
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
        if self.dropdown_active and self.dropdown_type == "figure" and self.dropdown_player_index == idx:
            self.dropdown_active = False
            return
        
        self.dropdown_active = True
        self.dropdown_type = "figure"
        self.dropdown_player_index = idx
        self.dropdown_items = list(AVAILABLE_FIGURES)
        self.dropdown_anchor = (btn.rect.center_x, btn.rect.bottom - 6)
    
    def on_open_color_dropdown(self, event):
        btn = event.source
        idx = btn.player_index
        if self.dropdown_active and self.dropdown_type == "color" and self.dropdown_player_index == idx:
            self.dropdown_active = False
            return
        
        self.dropdown_active = True
        self.dropdown_type = "color"
        self.dropdown_player_index = idx
        self.dropdown_items = list(AVAILABLE_COLORS)
        self.dropdown_anchor = (btn.rect.center_x, btn.rect.bottom - 6)
    
    def on_decrease_width(self, event):
        settings = self.window.game_settings
        if settings["width"] > MIN_BOARD_SIZE:
            settings["width"] -= 1
            self.width_label.text = str(settings["width"])
    
    def on_increase_width(self, event):
        settings = self.window.game_settings
        if settings["width"] < MAX_BOARD_SIZE:
            settings["width"] += 1
            self.width_label.text = str(settings["width"])
    
    def on_decrease_height(self, event):
        settings = self.window.game_settings
        if settings["height"] > MIN_BOARD_SIZE:
            settings["height"] -= 1
            self.height_label.text = str(settings["height"])
    
    def on_increase_height(self, event):
        settings = self.window.game_settings
        if settings["height"] < MAX_BOARD_SIZE:
            settings["height"] += 1
            self.height_label.text = str(settings["height"])
    
    def on_decrease_players(self, event):
        settings = self.window.game_settings
        if settings["player_count"] > 2:
            settings["player_count"] -= 1
            self.error_label.text = ""
            self.setup_ui()
    
    def on_increase_players(self, event):
        settings = self.window.game_settings
        if settings["player_count"] < MAX_PLAYERS:
            settings["player_count"] += 1
            self.ensure_players_capacity()
            self.ensure_unique_settings(update_ui=False)
            self.setup_ui()
    
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
    
    def ensure_unique_settings(self, update_ui: bool = True):
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
                        if update_ui and i < len(self.player_settings):
                            self.player_settings[i]["figure_btn"].text = fig
                        break
            used_figures.add(settings["players"][i]["figure"])
            
            if current_color in used_colors:
                for col in AVAILABLE_COLORS:
                    if col not in used_colors:
                        settings["players"][i]["color"] = col
                        if update_ui and i < len(self.player_settings):
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
        for i in range(settings["player_count"]):
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
