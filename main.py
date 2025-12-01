from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty, BooleanProperty
from random import randint

Window.clearcolor = (0, 0, 0, 1)
Window.size = (600, 400)

CELL = 20

class SnakeGame(Widget):
    snake = ListProperty()
    food = ListProperty()
    direction = ListProperty([1, 0])
    score = NumericProperty(0)
    running = BooleanProperty(True)
    speed = NumericProperty(7)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = int(self.width // CELL) if self.width else 30
        self.rows = int(self.height // CELL) if self.height else 20
        self.reset()
        Clock.schedule_interval(self.update, 1.0 / self.speed)
        self._touch_start = None

    def on_size(self, *args):
        self.cols = max(5, int(self.width // CELL))
        self.rows = max(5, int(self.height // CELL))
        self.reset()

    def reset(self):
        mid_x = self.cols // 2
        mid_y = self.rows // 2
        self.snake = [[mid_x, mid_y], [mid_x - 1, mid_y], [mid_x - 2, mid_y]]
        self.direction = [1, 0]
        self.place_food()
        self.score = 0
        self.running = True

    def place_food(self):
        while True:
            fx = randint(0, self.cols - 1)
            fy = randint(0, self.rows - 1)
            if [fx, fy] not in self.snake:
                self.food = [fx, fy]
                break

    def on_touch_down(self, touch):
        self._touch_start = (touch.x, touch.y)
        return True

    def on_touch_up(self, touch):
        if not self._touch_start:
            return True
        sx, sy = self._touch_start
        ex, ey = touch.x, touch.y
        dx = ex - sx
        dy = ey - sy
        if abs(dx) > abs(dy):
            if dx > 20 and self.direction != [-1, 0]:
                self.direction = [1, 0]
            elif dx < -20 and self.direction != [1, 0]:
                self.direction = [-1, 0]
        else:
            if dy > 20 and self.direction != [0, -1]:
                self.direction = [0, 1]
            elif dy < -20 and self.direction != [0, 1]:
                self.direction = [0, -1]
        self._touch_start = None
        return True

    def update(self, dt):
        if not self.running:
            return
        head = self.snake[0].copy()
        head[0] += self.direction[0]
        head[1] += self.direction[1]

        if head[0] < 0 or head[0] >= self.cols or head[1] < 0 or head[1] >= self.rows:
            self.game_over()
            return

        if head in self.snake:
            self.game_over()
            return

        self.snake.insert(0, head)

        if head == self.food:
            self.score += 1
            if self.score % 5 == 0:
                self.speed = min(20, self.speed + 1)
                Clock.unschedule(self.update)
                Clock.schedule_interval(self.update, 1.0 / self.speed)
            self.place_food()
        else:
            self.snake.pop()

        self.canvas.clear()
        self.draw()

    def draw(self):
        from kivy.graphics import Color, Rectangle
        with self.canvas:
            Color(1, 0, 0)
            Rectangle(pos=(self.food[0] * CELL, self.food[1] * CELL), size=(CELL - 1, CELL - 1))
            Color(0, 1, 0)
            for seg in self.snake:
                Rectangle(pos=(seg[0] * CELL + 1, seg[1] * CELL + 1), size=(CELL - 2, CELL - 2))

    def game_over(self):
        self.running = False
        Clock.schedule_once(lambda dt: self.reset(), 1.0)

class SnakeApp(App):
    def build(self):
        return SnakeGame()

if __name__ == "__main__":
    SnakeApp().run()
