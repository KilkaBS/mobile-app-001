from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class PongPaddle(Widget):
    score = NumericProperty(0)  # Очки игрока

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

class PongBall(Widget):
    # Скорость движения шарика по двум осям
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # Условный вектор
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # Движение шарика
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)  # Связь с шариком
    player1 = ObjectProperty(None)  # Игрок 1
    player2 = ObjectProperty(None)  # Игрок 2

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(*vel).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()  # Движение шара в каждом направлении

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # Отскок шарика по оси Y
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1  # Инвертирование скорости по оси Y

        # Проверка пересечения левой и правой границы
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(-4, 0))  # Подача мяча в сторону проигравшего игрока

        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(4, 0))  # Подача мяча в сторону проигравшего игрока

    # Прикосновение к экрану
    def on_touch_move(self, touch):
        # Игрок 1 касается только левой стороны
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y

        # Игрок 2 наоборот, правой
        if touch.x > self.width * 2 / 3:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60)  # 60 FPS
        return game

if __name__ == "__main__":
    PongApp().run()
