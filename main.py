import arcade
import random

WIDTH, HEIGHT = 900, 600

PIPE_SPEED = -5
SPAWN_PIPE_TIME = 1.5

WIN_SCORE = 30

GRAVITY = .3
BIRD_POS_X, BIRD_POS_Y = 100, HEIGHT/2
BIRD_CHANGE_Y = 5
BIRD_CHANGE_ANGLE = 5
LIMIT_ANGLE = 45
DISTANCE = 150

MIN_PIPE_Y = 50
MAX_PIPE_Y = 300

SOUND_VOLUME = .1

class Animation(arcade.Sprite):
    i = 0
    time = 0
    def update_animation(self, delta_time):
        self.time += delta_time
        if self.time > .2:
            self.time = 0
            if self.i == len(self.textures) - 1:
                self.i = 0
            else:
                self.i += 1
            self.set_texture(self.i)
        
class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH,HEIGHT)
        self.bird = Bird()
        self.pipes = arcade.SpriteList()
        self.spawn_pipe_time = 0
        self.game_state = True
        self.score = 0

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(WIDTH/2, HEIGHT/2 , WIDTH, HEIGHT, arcade.load_texture('bg.png'))
        self.bird.draw()
        self.pipes.draw()
        arcade.draw_text(f'score: {int(self.score)}', WIDTH/2, HEIGHT - 100, arcade.color.AMARANTH_PINK, 30, anchor_x='center')
        if not self.game_state:
            if self.score >= WIN_SCORE:
                arcade.draw_text('Win', WIDTH/2, HEIGHT/2, arcade.color.AMARANTH_PINK, 80, anchor_x='center')
            else:
                arcade.draw_texture_rectangle(WIDTH/2, HEIGHT/2, WIDTH/2, HEIGHT/4, arcade.load_texture('gameover.png'))

    def update(self, delta_time):
        if self.game_state:

            self.bird.update()
            self.pipes.update()

            self.bird.update_animation(delta_time)
            self.spawn_pipe(delta_time)

            for pipe in arcade.check_for_collision_with_list(self.bird, self.pipes):
                self.game_state = False
                arcade.play_sound(arcade.load_sound('audio/hit.wav'), SOUND_VOLUME)    

            if self.score >= WIN_SCORE:
                self.game_state = False

    def on_key_press(self, symbol, modifiers):

        if symbol == arcade.key.SPACE:
            self.bird.change_y = BIRD_CHANGE_Y
            self.bird.change_angle = BIRD_CHANGE_ANGLE
            arcade.play_sound(arcade.load_sound('audio/wing.wav'), SOUND_VOLUME)

    def spawn_pipe(self, delta_time):

        self.spawn_pipe_time += delta_time
        if self.spawn_pipe_time > SPAWN_PIPE_TIME:
            self.spawn_pipe_time = 0
            pipe_bottom = Pipe(False)
            pipe_bottom.center_x = WIDTH
            pipe_bottom.top = random.randint(MIN_PIPE_Y, MAX_PIPE_Y)
            self.pipes.append(pipe_bottom)
            pipe_top = Pipe(True)
            pipe_top.center_x = WIDTH
            pipe_top.bottom = pipe_bottom.top + DISTANCE
            self.pipes.append(pipe_top)

class Bird(Animation):
    def __init__(self):
        super().__init__('bird/bluebird-midflap.png')

        self.append_texture(arcade.load_texture('bird/redbird-downflap.png'))
        self.append_texture(arcade.load_texture('bird/yellowbird-upflap.png'))

        self.set_position(BIRD_POS_X, BIRD_POS_Y)

    def update(self):
        self.center_y += self.change_y
        self.change_y -= GRAVITY

        self.angle += self.change_angle
        self.change_angle -= GRAVITY

        if self.top >= HEIGHT:
            self.top = HEIGHT
        elif self.bottom <= 0:
            self.bottom = 0

        if self.angle > LIMIT_ANGLE:
            self.angle = LIMIT_ANGLE
        if self.angle < -LIMIT_ANGLE:
            self.angle = -LIMIT_ANGLE

class Pipe(arcade.Sprite):
    def __init__(self, flip):
        super().__init__('pipe.png', .3, flipped_vertically=flip)
        self.change_x = PIPE_SPEED
    def update(self):
        self.center_x += self.change_x

        if self.right <= 0:
            self.kill()
            game.score += .5
            arcade.play_sound(arcade.load_sound('audio/point.wav'), SOUND_VOLUME)

game = Game()
arcade.run()