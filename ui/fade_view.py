import arcade


class FadeView(arcade.View):
    def __init__(self):
        super().__init__()
        self._fade_alpha = 0.0
        self._fade_speed = 0.0
        self._fade_enabled = False

    def start_fade_in(self, duration: float = 0.25):
        duration = max(0.01, float(duration))
        self._fade_alpha = 255.0
        self._fade_speed = 255.0 / duration
        self._fade_enabled = True

    def on_show_view(self):
        self.start_fade_in()

    def on_update(self, delta_time: float):
        if not self._fade_enabled:
            return
        self._fade_alpha = max(0.0, self._fade_alpha - self._fade_speed * float(delta_time))
        if self._fade_alpha <= 0.0:
            self._fade_enabled = False

    def draw_fade(self):
        if self._fade_alpha <= 0.0 or not self.window:
            return
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.window.width,
            self.window.height,
            (0, 0, 0, int(self._fade_alpha)),
        )

