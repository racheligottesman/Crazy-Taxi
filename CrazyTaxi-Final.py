#"I hereby certify that this program is solely the result of my own work and is 
#in compliance with the Academic Integrity policy of the course syllabus and the
#academic integrity policy of the CS department.”

import Draw
import random
import time

#approved global variables

ROAD_HEIGHT = 600
SCREEN_HEIGHT = 750

TAXI_LEFT = 100
TAXI_MIDDLE = 350
TAXI_RIGHT= 600

CAR_LEFT = 450
CAR_MIDDLE = 500
CAR_RIGHT = 550

#Draw a background of sand, sky, and a road
def drawBackground():
	sand = Draw.color(250, 214, 96)
	Draw.setBackground(sand) 
	road = Draw.color(165, 165, 165)
	Draw.setColor(road)
	Draw.filledPolygon([ROAD_HEIGHT, 100, 400, 100, 0, SCREEN_HEIGHT, 
						     1000, SCREEN_HEIGHT])
	sky = Draw.color(173, 216, 249)
	Draw.setColor(sky)
	Draw.filledRect(0,0,1000, 100)	

#this is the design of the cars. Width and Length are in propertion to carSize,
#with length being half of width. 
def carShape(x, y, width, length):
	#the base of the car:
	Draw.filledRect(x, y + length/2, width, length/2)
	Draw.filledRect(x + width/4, y, width/2, length/2)
	#the window:
	Draw.setColor(Draw.BLACK)
	Draw.filledRect(x + width/3, y + length/5, width/4, length/4)
	#these are the tires:
	Draw.filledOval(x, y + length, width/4, width/4)
	Draw.filledOval(x + width *.7, y + length, width/4, width/4)

#Draws a car in either the middle, left, or right. 
#The x-coordinate is dependant on the y coordinate to create the illusion that 
#the car is coming directly toward you while in reality is is moving diagonally
def drawCar(x, y, carSize, color):
	Draw.setColor(color)
	if x == CAR_MIDDLE:
		carShape(x - y/6, y, carSize, carSize/2)
	if x == CAR_LEFT:
		carShape(x - y/2, y, carSize, carSize/2)
	if x == CAR_RIGHT:
		carShape(x + y/6, y, carSize, carSize/2)

#Checks to see if any of the cars in the row directly in fron of the taxi are 
#in the same lane as the taxi
def taxiCollision(taxiTrack, bottomY, cars, taxiZ, totalDistance, totalCars, 
		  distanceBetweenCars, speed):
	#if the taxi is currently jumping:
	if not taxiZ:
		#check all possible y-coordinates of the cars
		for row in range(len(cars)):
			#if the y of the row coordinate is =  (25*speed) above
			#the current bottom of the frame (where the taxi is).
			#the distnce from the taxi must be in terms of speed
			#because bottomY is decreasing by speed
			if cars[row][0] == bottomY - (25*speed):
				#check all the cars in the colliding row
				for each in range(len(cars[row][1])):
					#if the the car is in the same lane 
					if cars[row][1][each][0] == taxiTrack: 
						return True	

def drawScreen(cars, timeRemaining, bottomY, taxiX, taxiZ, crash, level):
	Draw.clear()
	drawBackground()
	#draw the scoreboard:
	Draw.setColor(Draw.RED)
	Draw.setFontSize(24)
	Draw.string("Level: " + str(level), 10, 10)	
	Draw.string("Time Remaining: " + str(int(timeRemaining)) + 
		    "                  Distance Left: " + str(bottomY), 10, 50)
	#select which row of cars to print 
	for row in range(len(cars)):
		#carY is the y-coordinate of the car in regard to the screen 
		carY = SCREEN_HEIGHT - (bottomY - cars[row][0]) 
		#the size of the car is in proportion to its place on the screen
		#as it gets closer to the bottom it gets larger - 
		#so that it looks like it is coming toward you
		carSize = carY/3	
		#if the rows's y-coordinate is above the bottom of the screen
		#and the bottom of the car is below the top of the screen:
		if ( cars[row][0] < bottomY and
		(cars[row][0] + 0.5*carSize) >= (bottomY - ROAD_HEIGHT) ):
			#draw all the cars in the row
			for each in range(len(cars[row][1])):
				drawCar(cars[row][1][each][0], carY, 
					carSize, cars[row][1][each][1])
	#crash is a variable that is True if is currently a taxi collision
	if crash: 
		#Draw an explosion
		Draw.picture("crash.gif", taxiX, ROAD_HEIGHT )
	#Draw the texi at the bottom of the screen unless it is jumping
	Draw.picture("Taxi.gif", taxiX, ROAD_HEIGHT + taxiZ)

#this is the includes the begining, level up, and end screen. 
def textBox(level, timeRemaining, bottomY, result):
	Draw.clear()
	drawBackground()
	#draws a "textbox"
	Draw.filledRect(200,200,600,270)
	Draw.setFontSize(30)
	Draw.setColor(Draw.BLACK)	
	Draw.filledRect(230, 230, 540, 200)
	Draw.setColor(Draw.RED)	
	#if you lost 
	if result == "Lost": 
		Draw.string("Better Luck Next Time!" , 250, 250)
		Draw.string("Level: " + str(level), 250, 300)	
		Draw.string("Distance Left: " + str(bottomY), 250, 350)	
		Draw.show()	
	#before the first level instructions are shown
	elif level == 1:
		Draw.setColor(Draw.BLACK)			
		Draw.filledRect(200,200,600,500)
		Draw.setColor(Draw.RED)			
		Draw.string("Welcome to Crazy Taxi!", 240, 300) 
		Draw.string("Use right and left arrows to change lanes",240,350)
		Draw.string("Use up arrow to jump.", 240, 400)
		Draw.string("Avoid the cars!!",240, 450)
		Draw.string("If you hit a car you'll be bounced back.",240,500)
		Draw.string("Cover the distance before time runs out.",240, 550)
		Draw.show()				
		time.sleep(5)	

	#if you beat the level
	elif result == "Level":
		Draw.string("Level " + str(level) , 250, 250)
		Draw.show()				
		time.sleep(2)		
	#if you won the game
	elif result == "Win":
		Draw.string("congratulations!!!" , 250, 250)
		Draw.string("you beat the game ", 250, 350)	
		Draw.show()		

#this is the game play function
def playGame(totalDistance, totalTime, level, speed, totalCars, 
	     distanceBetweenCars):
	#the cars can be in any of these positions or colors
	position = [CAR_LEFT, CAR_MIDDLE, CAR_RIGHT]
	colors = [Draw.BLUE, Draw.PINK, Draw.YELLOW, Draw.CYAN]
	
	#generate a list of y-coordinates (rows) for the the cars 
	carRows = [i for i in range (0, totalDistance, distanceBetweenCars)]
	#for each row of cars generate a list of three cars at random positions
	#and random colors. The cars positions can be the same making it appear
	#as if there is only 1 or 2 cars some of the rows
	cars = [ [ carRows[i], [ [random.choice(position),random.choice(colors)] 
			    for i in range(3) ] ] for i in range(totalCars) ]
	timeRemaining =  totalTime
	taxiX =  TAXI_MIDDLE
	#because the taxi and the car have different x-coordinates for MIDDLE,
	#RIGHT, and LEFT, taxiTrack is a variable that will keep track of the 
	#Taxi's lane in terms of the Car's lane. This will allow 
	#the taxiCollision function to work
	taxiTrack = CAR_MIDDLE
	#bottomY refers to the current bottom of the screen in respect to the
	#total distance - it will continuously be lowered 
	bottomY = totalDistance
	#the taxi's height begins at zero - it is on the ground
	taxiZ = 0
	#fuel is the variable that allows the taxi to jump 
	fuel = 0
	crash = False
	
	textBox(level, timeRemaining, bottomY, "Level")
	#while there is still distance and time remaining
	while bottomY > 0 and timeRemaining > 0:
		
		#phase 1 - check for user input and adjust variables
		if Draw.hasNextKeyTyped():
			key = Draw.nextKeyTyped()
			#match the key pressed 
			#to the proper taxi lane and taxi track lane
			if key == "Left": 
				if  taxiX == TAXI_MIDDLE:
					taxiX = TAXI_LEFT
					taxiTrack = CAR_LEFT
				if  taxiX == TAXI_RIGHT:
					taxiX = TAXI_MIDDLE
					taxiTrack = CAR_MIDDLE
			if key == "Right":
				if  taxiX == TAXI_MIDDLE:
					taxiX = TAXI_RIGHT
					taxiTrack = CAR_RIGHT
				if  taxiX == TAXI_LEFT:
					taxiX = TAXI_MIDDLE
					taxiTrack = CAR_MIDDLE

			elif key == "Up":
				#if the taxi is on the ground
				if  taxiZ == 0:
					#add "fuel" to the taxi's tank. 
					#the taxi can only be jumping 
					#when it has fuel
					fuel = 100
				
		# phase 2 - update variable(s) for things that are moving
		bottomY -= speed
		#time decreases by an arbitrary number
		timeRemaining -= .015	
		#while there is fuel the taxi moves upward on the screen
		#but fuel is used up
		if fuel > 0:
			taxiZ -= 10
			fuel -= 5
		#taxiZ is restored and the taxi returns to its original height	
		elif taxiZ < 0:
			taxiZ += 10

		if taxiCollision(taxiTrack, bottomY, cars, taxiZ, 
				 totalDistance, totalCars, 
				 distanceBetweenCars, speed):
			#the rows of cars are pushed back in proportion to the
			#speed. Player is given another chance to avoid car
			bottomY +=  40 * speed
			#the crash variable will inform drawScreen
			crash = True	
			
		else: crash = False

		# phase 3 - re-render the canvase and show
		drawScreen(cars, timeRemaining, bottomY, 
			   taxiX, taxiZ, crash, level)
		Draw.show()
		if crash: time.sleep(.2)

		
	#if you ran out of time and did not complete the distance
	if timeRemaining <= 0 and bottomY >= timeRemaining: 
		#the lost screen will be shown
		textBox(level, timeRemaining, bottomY, "Lost")
		#This will let the main function know to stop runnung playGame
		return (False)
	
	else: return True
	
def main():
	Draw.setCanvasSize(1000, SCREEN_HEIGHT)
	totalTime = 20
	level = 1
	speed = 5 
	totalDistance = speed * 1000
	totalCars = 25
	distanceBetweenCars = (int(totalDistance/totalCars))
	#the game will run as long as play is True. 
	#play will be set to False is you louse
	play = True
	
	while level < 5 and play:
		#runs the game and checks to see if you lost
		if not playGame(totalDistance, totalTime, 
			    level, speed, totalCars, distanceBetweenCars): 
			play = False
		
		# update the variables for the next round	
		level += 1
		speed += 1
		totalDistance = speed * 1000
		distanceBetweenCars = (int(totalDistance/totalCars))
		timeTrack = totalTime 
	#after level 4 you win!
	if level == 5: textBox(level, totalTime, totalDistance, "Win")	
		
main()