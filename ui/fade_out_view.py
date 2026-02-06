import arcade


class FadeOutView(arcade.View):
    def __init__(self, from_view: arcade.View, to_view: arcade.View, duration: float = 0.25):
        super().__init__()
        self.from_view = from_view
        self.to_view = to_view
        self.duration = max(0.01, float(duration))
        self.alpha = 0.0

    def on_draw(self):
        if self.from_view:
            self.from_view.on_draw()
        if self.window:
            arcade.draw_lbwh_rectangle_filled(
                0,
                0,
                self.window.width,
                self.window.height,
                (0, 0, 0, int(self.alpha)),
            )

    def on_update(self, delta_time: float):
        self.alpha = min(255.0, self.alpha + 255.0 * float(delta_time) / self.duration)
        if self.alpha >= 255.0 and self.window:
            self.window.show_view(self.to_view)

    def on_mouse_press(self, x, y, button, modifiers):
        return

    def on_key_press(self, key, modifiers):
        return

