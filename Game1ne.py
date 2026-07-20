

#SAMSON BLIKSTEN is the greatest to ever do it

import os
import platform
import random
import time

script_dir = os.path.dirname(os.path.abspath(__file__))

try:
    import pygame
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    pygame.mixer.init()
    if pygame.mixer.get_init() is None:
        raise RuntimeError("pygame mixer failed to initialize")

    def _load_sound(fname):
        path = os.path.join(script_dir, fname)
        if os.path.isfile(path):
            try:
                return pygame.mixer.Sound(path)
            except Exception as _e:
                print(f"Failed to load sound {path}:", _e)
        else:
            print(f"Sound file not found: {path}")
        return None

    missile_sound = _load_sound("missile.mp3")
    crash_sound = _load_sound("explosion.mp3")
    if missile_sound is None:
        print("Warning: missile audio not available")
    if crash_sound is None:
        print("Warning: explosion audio not available")
except Exception as e:
    print("Audio disabled:", e)
    missile_sound = None
    crash_sound = None


def _play_sound(sound_obj, frequency=1000, duration_ms=180):
    if sound_obj is not None:
        try:
            sound_obj.play()
            return
        except Exception:
            pass

    if platform.system() == "Windows":
        try:
            import winsound
            winsound.Beep(frequency, duration_ms)
        except Exception:
            pass

#import the Turtle module
import turtle
screen = turtle.Screen()
screen.setup(800, 800)
screen.title("Space Game")
turtle.fd(0)
#set the animation speed to the maximum
turtle.speed(0)
#change the background color
turtle.bgcolor("black")
#Change the background image
turtle.bgpic(os.path.join(script_dir, "starfield.GIF"))  # GIF, PNG, or PPM format
#hide default turtle
turtle.ht()
#this saves memory
turtle.setundobuffer(1)
#use a normal redraw rate so the game feels smooth instead of too fast
turtle.tracer(1)

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        #boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
         
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() <-290:
            self.sety(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

    def is_collision(self, other):
        if (self.xcor() >= other.xcor() - 20) and \
           (self.xcor() <= other.xcor() + 20) and \
           (self.ycor() >= other.ycor() - 20) and \
           (self.ycor() <= other.ycor() + 20):
            return True
        else:
            return False


class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape,color, startx, starty)
        self.speed = 4
        self.lives = 3

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
            self.rt(45)

    def accelerate(self):
            self.speed += 1
            
    def decelerate(self):
            self.speed -= 1



class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape,color, startx, starty)
        self.speed = 4
        self.setheading(random.randint(0, 360))








class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape,color, startx, starty)
        self.speed = 4
        self.setheading(random.randint(0, 360))

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape,color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.5, outline=None)
        self.speed = 20
        self.status = "ready"
        self.hideturtle()
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.showturtle()
            self.status = "firing"
            try:
                if 'missile_sound' in globals() and missile_sound is not None:
                    _play_sound(missile_sound, frequency=1200, duration_ms=120)
            except Exception:
                pass

    def move(self):
        if self.status == "ready":
            self.goto(-1000, 1000)
                                      
        if self.status == "firing": 
            self.fd(self.speed)                    

            #border check
            if self.xcor() < -290 or self.xcor() > 290 or \
               self.ycor() < -290 or self.ycor() > 290:
                self.hideturtle()
                self.status = "ready"
                self.goto(-1000, 1000)


class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
         #draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "score: %s" 
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg % self.score, font=("Arial", 16, "normal"))

#create game border
game = Game()

#draw the game border
game.draw_border()

#Show the game status
game.show_status()

#Create my sprites
player = Player("triangle", "white", 0, 0)
#enemy = Enemy("hexagon", "red", -100, 0)
missile = Missile("obtuse", "yellow", 0, 0)
#ally = Ally("square", "blue", 100, 0)

enemies = []
for i in range(6):
    enemies.append(Enemy("hexagon", "red", -100, 0))

allies = []
for i in range(6):
    allies.append(Ally("square", "blue", 100, 0))



#keyboard bindings
screen.onkey(player.turn_left, "Left")
screen.onkey(player.turn_right, "Right")
screen.onkey(player.accelerate, "Up")
screen.onkey(player.decelerate, "Down")
screen.onkey(missile.fire, "space")
screen.listen()


#main game loop
while True:
    turtle.update()

    player.move()
    missile.move()

    for enemy in enemies:
        enemy.move()

        # check for a collision between the player and this enemy
        if player.is_collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score += 100
            game.show_status()

        # check for a collision between the missile and this enemy
        if missile.status == "firing" and missile.is_collision(enemy):
            # play crash sound if available
            try:
                if 'crash_sound' in globals() and crash_sound is not None:
                    _play_sound(crash_sound, frequency=900, duration_ms=220)
            except Exception:
                pass

            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            # increase the score
            game.score += 100
            game.show_status()

    for ally in allies:
        ally.move()

        # check for a collision between the missile and each ally (friendly fire)
        if missile.status == "firing" and missile.is_collision(ally):
            # play explosion sound if available
            try:
                if 'crash_sound' in globals() and crash_sound is not None:
                    _play_sound(crash_sound, frequency=900, duration_ms=220)
            except Exception:
                pass

            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            # decrease the score for hitting an ally
            game.score -= 50
            game.show_status()

        # check for a collision between the player and each ally
        if player.is_collision(ally):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            # decrease the score
            game.score -= 50
            game.show_status()





time.sleep(0.03)

delay = input("press enter to finish. > ")                        