import turtle, math, random


class SpaceCraft(turtle.Turtle):

    '''
    Purpose: Represents the player
    Instance variables: all turtle attributes, x position, y position, x velocity, y velocity, fuel - amount of fuel remaining, game - game instance spacecraft belongs to
    Methods: all turtle methods, move - simulates gravity on the spacecraft, thrust - moves spaceship forward, turn_left, turn_right, crash - animates a crash
    '''

    def __init__(self,xpos,ypos,xvel,yvel, game):
        turtle.Turtle.__init__(self)
        self.seth(90)
        self.speed(0)

        self.game = game
        self.vx = xvel
        self.vy = yvel
        self.fuel = 50

        self.color('red')
        self.penup()
        self.setpos(xpos,ypos)

    def move(self):
        self.vy -= 0.0486
        self.setpos(self.xcor() + self.vx, self.ycor() + self.vy)

        if self.xcor() < 0:
            self.setpos(999,self.ycor())

        if self.xcor() > 1000:
            self.setpos(1, self.ycor())


    def thrust(self):
        
        if self.fuel >= 1 and self.game.in_progress:
            self.fuel -= 1

            cos = math.cos(math.radians(self.heading()))
            sin = math.sin(math.radians(self.heading()))
            self.vx += cos
            self.vy += sin

            print('Fuel remaining: {}'.format(self.fuel))

        elif self.fuel == 0 and self.game.in_progress:
            turtle.color('white')
            turtle.ht()
            turtle.write('Out of fuel!')

    def turn_left(self):

        if self.fuel >= 1 and self.game.in_progress:
            self.fuel -= 1
            self.left(15)
            print('Fuel remaining: {}'.format(self.fuel))

        elif self.fuel == 0 and self.game.in_progress:
            turtle.color('white')
            turtle.ht()
            turtle.write('Out of fuel!')

    def turn_right(self):

        if self.fuel >= 1 and self.game.in_progress:
            self.fuel -= 1
            self.right(15)
            print('Fuel remaining: {}'.format(self.fuel))

        elif self.fuel == 0 and self.game.in_progress:
            turtle.color('white')
            turtle.ht()
            turtle.write('Out of fuel!')

    def crash(self):
        turtle.color('red')
        
        for i in range(1,17):
            turtle.ht()
            turtle.penup
            turtle.setpos(self.xcor(),self.ycor())
            
            turtle.seth(22.5*i)
            turtle.forward(5)
            turtle.pendown()
            turtle.forward(15)


class Asteroid(turtle.Turtle):

    '''
    Purpose: Represents an obstacle for the player to avoid
    Instance variables: all turtle attributes, game - game instance asteroid exists in, x position, y position, x velocity, y velocity
    Methods: all turtle methods, move - moves based on initial conditions and regulates collision, explosion - animates explosion, collide - manages collision
    '''

    def __init__(self,x,y,x_vel,y_vel,game):
        turtle.Turtle.__init__(self, 'circle')
        self.color('blue')

        self.vx = x_vel
        self.vy = y_vel
        self.penup()
        self.setpos(x,y)

    def move(self,game):
        
        if (self.xcor() < 0 or self.xcor() > 1000 or self.ycor() < 30 or self.ycor() > 1000) and game.in_progress:
            self.ht()
            game.obstacle_list.remove(self)

        self.setpos(self.xcor() + self.vx, self.ycor() + self.vy)
        self.collide(game)

        if self.xcor() < 0:
            self.setpos(999,self.ycor())

        if self.xcor() > 1000:
            self.setpos(1, self.ycor())

    def explosion(self):
        turtle.color('red')
        
        for i in range(1,17):
            turtle.ht()
            turtle.penup
            turtle.setpos(self.xcor(),self.ycor())
            
            turtle.seth(22.5*i)
            turtle.forward(5)
            turtle.pendown()
            turtle.forward(15)

    def collide(self, game):
        
        if abs(self.xcor() - game.player.xcor()) <= 25 and abs(self.ycor() - game.player.ycor()) <= 25:
            self.ht()
            game.obstacle_list.remove(self)
            game.player.ht()

            self.explosion()

            turtle.penup()
            turtle.setpos(450,500)
            turtle.color('white')
            turtle.ht()
            
            turtle.write('You crashed!')
            game.in_progress = False

    
class Game:
    
    '''
    Purpose: Represents the game running in a window
    Instance variables: all turtle attributes, obstacle_list - list of obstacles, in_progress - whether game is in progress or not
    Methods: all turtle methods, asteroids - creates asteroids, gameloop - runs game, background - sets background
    '''

    def __init__(self):
        turtle.setworldcoordinates(0, 0, 1000, 1000)
        turtle.delay(0)
        self.obstacle_list = []
        self.background()

        self.in_progress = True
        self.player = SpaceCraft(random.uniform(100,900),random.uniform(500,900),random.uniform(-5,5),random.uniform(-5,0),self) 
        self.gameloop()

        turtle.onkeypress(self.player.thrust, 'Up')
        turtle.onkeypress(self.player.turn_left, 'Left')
        turtle.onkeypress(self.player.turn_right, 'Right')

        turtle.listen()
        turtle.mainloop()

    def asteroids(self):

        if len(self.obstacle_list) < 20:
            turtle.ontimer(self.obstacle_list.append(Asteroid(random.uniform(0,1000),random.uniform(0,1000),random.uniform(-5,5),random.uniform(-5,5),self)),1)
        
    def gameloop(self):

        self.asteroids()

        for obstacle in self.obstacle_list:
            if self.in_progress:
                obstacle.move(self)

        if self.player.ycor() >= 30:
            self.player.move()
            
            turtle.ontimer(self.gameloop,30)

        elif abs(self.player.vx) < 4 and abs(self.player.vy) < 4 and self.in_progress and self.player.ycor() < 30:
            self.in_progress = False

            turtle.penup()
            turtle.setpos(450,500)
            turtle.color('white')
            turtle.ht()
            turtle.write('Successful landing!')

        else:
            self.player.ht()
            
            if self.in_progress:
                self.player.crash()
                
            self.in_progress = False
            
            turtle.penup()
            turtle.setpos(450,500)
            turtle.color('white')
            turtle.ht()
            turtle.write('You crashed!')

    def background(self):
        turtle.bgcolor('black')
        
        for i in range(15):
            turtle.setpos(random.uniform(10,990),random.uniform(10,990))
            turtle.penup()
            turtle.dot(random.uniform(2,10),'white')

        turtle.penup()
        turtle.setpos(500,-2000)
        turtle.dot(2330,'white')
        

game = Game()
