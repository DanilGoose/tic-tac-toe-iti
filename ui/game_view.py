import arcade
import arcade.gui
from game.board import Board
from game.player import Player
from game.rules import GameRules
from game.player_db import record_game_result


class GameView(arcade.View):
    RUS_COLS = "АБВГДЕЖИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    def __init__(self, settings: dict):
        super().__init__()
        self.settings = settings
        self.board = None
        self.players = []
        self.rules = None
        self.manager = arcade.gui.UIManager()
        self.stats_recorded = False
        
        self.cell_size = 40
        self.grid_offset_x = 50
        self.grid_offset_y = 100
        self.sidebar_width = 180
        
        self.status_label = None
        self.current_player_label = None
        self.remaining_moves_label = None
        
        self.message = ""
        self.message_timer = 0
        
        self.game_time = 0
        self.timer_label = None
        
        self.grid_shape_list = None
        self.grid_labels_cache = None
        self.figures_dirty = True
        self.awaiting_check = False
        
        self.setup_game()
        self.setup_ui()
    
    def setup_game(self):
        self.board = Board(self.settings["width"], self.settings["height"])
        
        self.players = []
        for i in range(self.settings["player_count"]):
            player_data = self.settings["players"][i]
            player = Player(
                player_id=i,
                name=player_data.get("name", f"Игрок {i + 1}"),
                figure=player_data["figure"],
                color=player_data["color"]
            )
            self.players.append(player)
        
        win_patterns = self.settings.get("win_patterns")
        self.rules = GameRules(self.board, self.players, win_patterns)
        self.stats_recorded = False
        self.recalculate_layout()

    def record_stats_once(self):
        if self.stats_recorded:
            return
        winner_name = self.rules.winner.name if self.rules.winner else None
        record_game_result([player.name for player in self.players], winner_name)
        self.stats_recorded = True
    
    def recalculate_layout(self):
        min_cell_size = 8
        side_gap = 30
        outer_margin = 20

        self.sidebar_width = max(140, int(self.window.width * 0.22))

        cell_size = max(min_cell_size, int(self.cell_size) or min_cell_size)
        for _ in range(3):
            label_font_size = max(14, int(cell_size * 0.5))
            label_offset = max(14, int(label_font_size * 0.8))
            label_pad = label_offset + label_font_size // 2 + 4

            left_pad = label_pad + outer_margin
            bottom_pad = label_pad + outer_margin
            right_pad = outer_margin
            top_pad = outer_margin

            available_width = self.window.width - left_pad - side_gap - self.sidebar_width - right_pad
            available_height = self.window.height - top_pad - bottom_pad
            if available_width <= 0 or available_height <= 0:
                new_cell = min_cell_size
            else:
                max_cell_width = available_width // self.board.width
                max_cell_height = available_height // self.board.height
                new_cell = max(min_cell_size, min(max_cell_width, max_cell_height))

            if new_cell == cell_size:
                break
            cell_size = new_cell

        self.cell_size = cell_size
        label_font_size = max(14, int(self.cell_size * 0.5))
        label_offset = max(14, int(label_font_size * 0.8))
        label_pad = label_offset + label_font_size // 2 + 4

        grid_width = self.board.width * self.cell_size
        grid_height = self.board.height * self.cell_size

        left_pad = label_pad + outer_margin
        bottom_pad = label_pad + outer_margin
        right_pad = outer_margin
        top_pad = outer_margin

        total_width = left_pad + grid_width + side_gap + self.sidebar_width + right_pad
        extra_x = max(0, self.window.width - total_width)
        self.grid_offset_x = int(left_pad + extra_x // 2)

        total_height = bottom_pad + grid_height + top_pad
        extra_y = max(0, self.window.height - total_height)
        self.grid_offset_y = int(bottom_pad + extra_y // 2)
    
    def setup_ui(self):
        self.manager.clear()
        scale = min(self.window.width / 1024, self.window.height / 768)
        scale = max(0.75, min(1.2, scale))
        
        sidebar_x = self.grid_offset_x + self.board.width * self.cell_size + 30
        
        v_box = arcade.gui.UIBoxLayout()
        
        self.current_player_label = arcade.gui.UILabel(
            text="",
            font_size=int(20 * scale),
            text_color=(255, 255, 255)
        )
        v_box.add(self.current_player_label.with_padding(bottom=int(15 * scale)))
        
        self.remaining_moves_label = arcade.gui.UILabel(
            text="",
            font_size=int(18 * scale),
            text_color=(255, 255, 255)
        )
        v_box.add(self.remaining_moves_label.with_padding(bottom=int(10 * scale)))
        
        self.timer_label = arcade.gui.UILabel(
            text="Время: 0:00",
            font_size=int(16 * scale),
            text_color=(255, 255, 255)
        )
        v_box.add(self.timer_label.with_padding(bottom=int(20 * scale)))
        
        btn_width = max(120, int(140 * scale))
        btn_height = max(38, int(45 * scale))
        if self.awaiting_check:
            check_btn = arcade.gui.UIFlatButton(text="Проверить", width=btn_width, height=btn_height)
            check_btn.on_click = self.on_check_click
            v_box.add(check_btn.with_padding(bottom=int(12 * scale)))

            next_btn = arcade.gui.UIFlatButton(text="Далее", width=btn_width, height=btn_height)
            next_btn.on_click = self.on_next_click
            v_box.add(next_btn.with_padding(bottom=int(12 * scale)))
        else:
            confirm_btn = arcade.gui.UIFlatButton(text="Подтвердить", width=btn_width, height=btn_height)
            confirm_btn.on_click = self.on_confirm_click
            v_box.add(confirm_btn.with_padding(bottom=int(12 * scale)))

            undo_btn = arcade.gui.UIFlatButton(text="назад", width=btn_width, height=btn_height)
            undo_btn.on_click = self.on_undo_click
            v_box.add(undo_btn.with_padding(bottom=int(12 * scale)))

            menu_btn = arcade.gui.UIFlatButton(text="выход из игры", width=btn_width, height=btn_height)
            menu_btn.on_click = self.on_menu_click
            v_box.add(menu_btn)
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            v_box,
            anchor_x="left",
            anchor_y="top",
            align_x=sidebar_x,
            align_y=-int(50 * scale)
        )
        self.manager.add(anchor)
        
        self.update_labels()
    
    def update_labels(self):
        current = self.rules.get_current_player()
        self.current_player_label.text = f"Ход: {current.name} ({current.figure})"
        remaining = 0 if self.awaiting_check else self.rules.get_remaining_moves()
        self.remaining_moves_label.text = f"Осталось ходов: {remaining}"
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.manager.enable()
    
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.recalculate_layout()
        self.grid_shape_list = None
        self.setup_ui()
    
    def on_hide_view(self):
        self.manager.disable()
    
    def on_update(self, delta_time):
        if self.message_timer > 0:
            self.message_timer -= delta_time
            if self.message_timer <= 0:
                self.message = ""
        
        if not self.rules.game_over:
            self.game_time += delta_time
            minutes = int(self.game_time) // 60
            seconds = int(self.game_time) % 60
            if self.timer_label:
                self.timer_label.text = f"Время: {minutes}:{seconds:02d}"
    
    def on_draw(self):
        self.clear()
        self.draw_grid()
        self.draw_figures()
        self.draw_pending_moves()
        self.draw_winning_line()
        self.manager.draw()
        self.draw_message()
    
    def build_grid_cache(self):
        self.grid_shape_list = arcade.shape_list.ShapeElementList()
        
        for y in range(self.board.height + 1):
            start_x = self.grid_offset_x
            end_x = self.grid_offset_x + self.board.width * self.cell_size
            pos_y = self.grid_offset_y + y * self.cell_size
            line = arcade.shape_list.create_line(start_x, pos_y, end_x, pos_y, arcade.color.WHITE, 1)
            self.grid_shape_list.append(line)
        
        for x in range(self.board.width + 1):
            pos_x = self.grid_offset_x + x * self.cell_size
            start_y = self.grid_offset_y
            end_y = self.grid_offset_y + self.board.height * self.cell_size
            line = arcade.shape_list.create_line(pos_x, start_y, pos_x, end_y, arcade.color.WHITE, 1)
            self.grid_shape_list.append(line)
    
    def draw_grid(self):
        if self.grid_shape_list is None:
            self.build_grid_cache()
        
        self.grid_shape_list.draw()

        label_font_size = max(14, int(self.cell_size * 0.5))
        label_offset = max(14, int(label_font_size * 0.8))
        
        for x in range(self.board.width):
            col_label = self.RUS_COLS[x] if x < len(self.RUS_COLS) else f"{x+1}"
            pos_x = self.grid_offset_x + x * self.cell_size + self.cell_size // 2
            pos_y = self.grid_offset_y - label_offset
            arcade.draw_text(
                col_label,
                pos_x,
                pos_y,
                arcade.color.WHITE,
                label_font_size,
                anchor_x="center",
                anchor_y="center",
            )

        for y in range(self.board.height):
            row_label = str(y + 1)
            pos_x = self.grid_offset_x - label_offset
            pos_y = self.grid_offset_y + y * self.cell_size + self.cell_size // 2
            arcade.draw_text(
                row_label,
                pos_x,
                pos_y,
                arcade.color.WHITE,
                label_font_size,
                anchor_x="center",
                anchor_y="center",
            )
    
    def draw_figure_with_outline(self, text, center_x, center_y, color, font_size, alpha=255):
        outline_offset = max(1, font_size // 12)
        outline_color = (255, 255, 255, alpha)
        arcade.draw_text(
            text,
            center_x - outline_offset, center_y,
            outline_color,
            font_size,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        arcade.draw_text(
            text,
            center_x + outline_offset, center_y,
            outline_color,
            font_size,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        arcade.draw_text(
            text,
            center_x, center_y - outline_offset,
            outline_color,
            font_size,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        arcade.draw_text(
            text,
            center_x, center_y + outline_offset,
            outline_color,
            font_size,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        arcade.draw_text(
            text,
            center_x, center_y,
            (*color[:3], alpha),
            font_size,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
    
    def draw_figures(self):
        for y in range(self.board.height):
            for x in range(self.board.width):
                player_id = self.board.get_cell(x, y)
                if player_id is not None:
                    player = self.players[player_id]
                    center_x = self.grid_offset_x + x * self.cell_size + self.cell_size // 2
                    center_y = self.grid_offset_y + y * self.cell_size + self.cell_size // 2
                    font_size = int(self.cell_size * 0.6)
                    self.draw_figure_with_outline(
                        player.figure,
                        center_x, center_y,
                        player.color,
                        font_size
                    )
    
    def draw_pending_moves(self):
        current = self.rules.get_current_player()
        for x, y in self.rules.pending_moves:
            center_x = self.grid_offset_x + x * self.cell_size + self.cell_size // 2
            center_y = self.grid_offset_y + y * self.cell_size + self.cell_size // 2
            
            rect = arcade.Rect.from_kwargs(
                x=center_x,
                y=center_y,
                width=self.cell_size - 4,
                height=self.cell_size - 4
            )
            arcade.draw_rect_outline(rect, arcade.color.YELLOW, 2)
            
            font_size = int(self.cell_size * 0.5)
            self.draw_figure_with_outline(
                current.figure,
                center_x, center_y,
                current.color,
                font_size,
                alpha=128
            )
    
    def draw_winning_line(self):
        if self.rules.winning_cells:
            for x, y in self.rules.winning_cells:
                center_x = self.grid_offset_x + x * self.cell_size + self.cell_size // 2
                center_y = self.grid_offset_y + y * self.cell_size + self.cell_size // 2
                rect = arcade.Rect.from_kwargs(
                    x=center_x,
                    y=center_y,
                    width=self.cell_size - 2,
                    height=self.cell_size - 2
                )
                arcade.draw_rect_filled(rect, (0, 255, 0, 100))
                arcade.draw_rect_outline(rect, (0, 255, 0, 255), 3)
    
    def draw_message(self):
        if self.message:
            arcade.draw_text(
                self.message,
                self.window.width // 2,
                self.window.height - 30,
                arcade.color.YELLOW,
                18,
                anchor_x="center"
            )
    
    def show_message(self, text: str, duration: float = 2.0):
        self.message = text
        self.message_timer = duration
    
    def get_cell_from_mouse(self, x: int, y: int):
        cell_x = (x - self.grid_offset_x) // self.cell_size
        cell_y = (y - self.grid_offset_y) // self.cell_size
        
        if 0 <= cell_x < self.board.width and 0 <= cell_y < self.board.height:
            return int(cell_x), int(cell_y)
        return None
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.rules.game_over or self.awaiting_check:
            return
        
        cell = self.get_cell_from_mouse(x, y)
        if cell:
            cx, cy = cell
            success, msg = self.rules.add_pending_move(cx, cy)
            if not success:
                self.show_message(msg)
            self.update_labels()
    
    def on_key_press(self, key, modifiers):
        if self.awaiting_check:
            if key == arcade.key.ESCAPE:
                self.on_menu_click(None)
            return
        if key == arcade.key.ENTER:
            self.on_confirm_click(None)
        elif key == arcade.key.ESCAPE:
            self.on_menu_click(None)

    def on_confirm_click(self, event):
        if self.rules.game_over or self.awaiting_check:
            return

        success, msg = self.rules.confirm_turn()
        if success:
            self.awaiting_check = True
            self.setup_ui()
        else:
            self.show_message(msg)
        self.update_labels()

    def on_check_click(self, event):
        if self.rules.game_over:
            return

        success, _ = self.rules.check_winner()
        if success:
            self.record_stats_once()
            if self.settings.get("hide_board_on_win", True):
                from ui.result_view import ResultView
                result_view = ResultView(self.rules.winner, self.rules.is_draw, self.settings)
                self.window.show_view(result_view)
            else:
                self.show_game_over_ui()
            return
        self.rules.eliminate_last_player()
        if self.rules.is_draw or self.rules.game_over:
            self.record_stats_once()
            if self.settings.get("hide_board_on_win", True):
                from ui.result_view import ResultView
                result_view = ResultView(self.rules.winner, self.rules.is_draw, self.settings)
                self.window.show_view(result_view)
            else:
                self.show_game_over_ui()
            return
        self.rules.advance_turn()
        self.awaiting_check = False
        self.setup_ui()
        self.update_labels()

    def on_next_click(self, event):
        if self.rules.game_over:
            return
        self.rules.advance_turn()
        self.awaiting_check = False
        self.setup_ui()
        self.update_labels()

    def show_game_over_ui(self):
        self.record_stats_once()
        self.manager.clear()
        scale = min(self.window.width / 1024, self.window.height / 768)
        scale = max(0.75, min(1.2, scale))
        
        v_box = arcade.gui.UIBoxLayout()
        
        if self.rules.is_draw:
            result_text = "Ничья!"
            result_color = (255, 255, 100)
        else:
            result_text = f"Победил {self.rules.winner.name}!"
            result_color = self.rules.winner.color
        
        result_label = arcade.gui.UILabel(
            text=result_text,
            font_size=int(28 * scale),
            bold=True,
            text_color=result_color
        )
        v_box.add(result_label.with_padding(bottom=int(30 * scale)))
        
        btn_width = max(120, int(140 * scale))
        btn_height = max(38, int(45 * scale))
        new_game_btn = arcade.gui.UIFlatButton(text="Новая игра", width=btn_width, height=btn_height)
        new_game_btn.on_click = self.on_new_game_click
        v_box.add(new_game_btn.with_padding(bottom=int(15 * scale)))
        
        menu_btn = arcade.gui.UIFlatButton(text="В меню", width=btn_width, height=btn_height)
        menu_btn.on_click = self.on_menu_click
        v_box.add(menu_btn)
        
        sidebar_x = self.grid_offset_x + self.board.width * self.cell_size + 30
        
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            v_box,
            anchor_x="left",
            anchor_y="top",
            align_x=sidebar_x,
            align_y=-int(50 * scale)
        )
        self.manager.add(anchor)
    
    def on_new_game_click(self, event):
        from ui.game_view import GameView
        game_view = GameView(self.settings)
        self.window.show_view(game_view)
    
    def on_undo_click(self, event):
        self.rules.remove_last_pending_move()
        self.update_labels()
    
    def on_skip_click(self, event):
        if self.rules.game_over:
            return
        
        success, msg = self.rules.skip_turn()
        self.show_message(msg)
        self.update_labels()
    
    def on_menu_click(self, event):
        from ui.menu_view import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)
