from sense_hat import SenseHat
from time import sleep
import random


sense = SenseHat()
level = 0
r = [255,0,0]
g = [0,255,0]
b = [0,0,0]
w = [255,255,255]
plus_2 = [
  b,b,b,b,b,b,b,b,
  b,b,b,b,b,b,b,b,
  b,b,b,b,b,b,b,b,
  b,b,b,b,g,g,g,g,
  b,b,g,b,g,b,b,g,
  b,g,g,g,b,b,g,b,
  b,b,g,b,b,g,b,b,
  b,b,b,b,g,g,g,g,
  ]
minus_2 = [
  b,b,b,b,b,b,b,b,
  b,b,b,b,b,b,b,b,
  b,b,b,b,b,b,b,b,
  b,b,b,b,g,g,g,g,
  b,b,b,b,g,b,b,g,
  b,g,g,g,b,b,g,b,
  b,b,b,b,b,g,b,b,
  b,b,b,b,g,g,g,g,
  ]

class Catcher:
  def __init__(self):
    self.x = 0
    self.y = 3
    self.len = 2
    self.score = 0
    self.tries = 3
    self.score_needed = 6
  
  def display(self):
    blue = [0,0,255]
    sense.clear()
    if 0 <= level < 2:
      sense.set_pixel(self.x,self.y,blue)
      sense.set_pixel(self.x,self.y+1,blue)
    elif 2 <= level <= 4:
      if self.y > 5:
        self.y = 5
      self.len = 3
      sense.set_pixel(self.x,self.y,blue)
      sense.set_pixel(self.x,self.y+1,blue)
      sense.set_pixel(self.x,self.y+2,blue)
    sleep(.2)
  
  def increment(self):
    global level
    if self.score == self.score_needed:
      level += 1
      print('------------------------\nLevel: ' + str(level + 1))
      if level < 5:
        self.score = 0
        print('Score: ' + str(self.score))
        if 0 <= level < 2:
          self.tries = 3
        elif 2 <= level < 4:
          self.tries = 1
        elif level == 4:
          self.tries = 2
        print('Tries: ' + str(self.tries))
        self.score_needed = 6 + 2*level
        print('Score needed to pass level: ' + str(self.score_needed))
  
  def run(self):
    self.display()
    for event in sense.stick.get_events():
      if event.action == "pressed":
        if event.direction == "up" and self.y > 0: 
          self.y -= 1  
        elif event.direction == "down" and self.y < 6:
          self.y += 1 
    self.increment()
    self.display()

catcher = Catcher()

class Ball:
  def __init__(self):
    self.reset()
    self.speed = 0.15
  
  def display(self, color):
    if 0 <= self.x < 8 and 0 <= self.y < 8:
      sense.set_pixel(self.x,self.y,color)
      
  def reset(self):
    self.x = 7
    self.y = random.randint(0,7)
    self.xvel = -1
    self.yvel = 1
  
  def health_bar(self, ls):
    if 0 <= level < 2:
      tries = 3
    elif 2 <= level < 4:
      tries = 1
    elif level == 4:
      tries = 2
    for i in range(tries*2):
      if ls[i] != r:
        ls[i] = w
    for i in range(8,9+(tries*2)-1):
      if ls[i] != r:
        ls[i] = w
      
  def move(self):
    global level
    if self.x <= 7 and self.x > 0:
      self.x += self.xvel
      if self.x in (0,7):
        self.xvel = -self.xvel
      self.y += self.yvel
      if self.y in (0,7):
        self.yvel = -self.yvel
      if self.x == 1 and catcher.y - 1 <= self.y <= catcher.y + catcher.len:
        self.xvel = -self.xvel
        catcher.score += 2
        for i in range(catcher.tries*2):
          plus_2[i] = r
          plus_2[i+8] = r
        self.health_bar(plus_2)
        sense.set_pixels(plus_2)
        sleep(.75)
        for index, letter in enumerate(plus_2):
            if letter in (r, w):
                plus_2[index] = b
        print('Score: ' + str(catcher.score))
      if catcher.score == catcher.score_needed:
        if self.speed > 0.075 and level < 3:
          self.speed *= .5
        elif level == 3:
          self.speed == 0.075
        else:
          self.speed = 0.15
    else:
      catcher.score -= 2
      catcher.tries -= 1
      for i in range(catcher.tries*2):
        minus_2[i] = r
        minus_2[i+8] = r
      self.health_bar(minus_2)
      sense.set_pixels(minus_2)
      sleep(.75)
      for index, letter in enumerate(minus_2):
            if letter in (r, w):
                minus_2[index] = b
      if catcher.tries == 1:
        sense.show_message('One try left ', text_colour = [255,255,255], scroll_speed = 0.02)
      print('Score: ' + str(catcher.score))
      print('Tries: ' + str(catcher.tries))
      self.reset()
  
  def run(self, color):
    self.move()
    self.display(color)
    sleep(self.speed)


ball = Ball()
    
  
second_ball = None
third_ball = None
def new_ball():
  ball = Ball()
  return ball


game_on = True
level_up_msgs = 0
  
def initilize():
  sense.show_message('Pong', text_colour = [255,255,255], scroll_speed = 0.04)
  sleep(.5)
  for i in range(3,0,-1):
    sense.show_message(str(i), text_colour = [255,255,255], scroll_speed = 0.06)
  sleep(1)
  print('Score: ' + str(catcher.score))
  print('Tries: ' + str(catcher.tries))
  print('Score needed to pass level: ' + str(catcher.score_needed))
  
  
balls = [ball]

initilize()
while game_on:
    
  catcher.run()
  ball.run([255,0,0])
  
  if 2 <= level < 4 and second_ball == None:
    second_ball = new_ball()
    balls.append(second_ball)
  if level == 4 and third_ball == None:
    third_ball = new_ball()
    balls.append(third_ball)
  if second_ball != None:
    second_ball.run([0,255,0])
  if third_ball != None:
    third_ball.run([230,230,250])

  n = 0
  while n < len(balls):
    indices = [i for i, x in enumerate(balls) if x != balls[n]]
    for ball_ind in indices:
      if abs(balls[n].x-balls[ball_ind].x) == 1 or abs(balls[n].y-balls[ball_ind].y) == 1:
        balls[n].xvel = -balls[n].xvel
        balls[ball_ind].xvel = -balls[ball_ind].xvel
    n += 1
  
  if level_up_msgs < level and level != 5:
    sense.show_message('Level up!', text_colour = [255,255,255], scroll_speed = 0.03)
    level_up_msgs += 1
    if level == 2:
      sleep(.5)
      sense.show_message('One try!', text_colour = [255,255,255], scroll_speed = 0.03)
    elif level == 4:
      sleep(.5)
      sense.show_message('Last round', text_colour = [255,255,255], scroll_speed = 0.03)
  
  if level == 5:
    game_on = False
    sense.show_message('You Win!', text_colour = [255,255,255], scroll_speed = 0.03)
    
  if catcher.tries == 0:
    game_on = False
    sense.show_message('GAME OVER', text_colour = [255,255,255], scroll_speed = 0.03)
  
  if not game_on:
    sense.show_message('Score: ' + str(catcher.score), text_colour = [255,255,255], scroll_speed = 0.03)
    sleep(2)
    level = 0
    level_up_msgs = 0
    game_on = True
    catcher = Catcher()
    ball = Ball()
    initilize()
