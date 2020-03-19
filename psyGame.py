import pygame
import random
import math
from pygame import mixer
import time, os
from random import randint
import csv, json
import pygame_textinput
from datetime import datetime

pygame.init()
random.seed(a=0.2, version=2)

canvasWidth = 800
canvasHeight = 600
screen = pygame.display.set_mode((canvasWidth, canvasHeight))
screen.fill((0,0,0))
pygame.display.set_caption("Psy Game 1.0")
icon = pygame.image.load('icon.jpg')
pygame.display.set_icon(icon)
font = pygame.font.Font('freesansbold.ttf',32)

textinput = pygame_textinput.TextInput(text_color = (150, 255, 100),
cursor_color = (255,255,255), font_size = 42)
clock = pygame.time.Clock()
surface = pygame.display.set_mode((canvasWidth, canvasHeight))

class Particle:
    def __init__(self, surface, x, y, size, colour=(255,0,0), thickness = 0):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.thickness = thickness
        self.surface = surface

    def display(self):
        pygame.draw.circle(self.surface, self.colour, (self.x, self.y), self.size, self.thickness)

class Box:
    def __init__(self, surface, x, y, size, colour=(255,0,0), thickness = 0):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.thickness = thickness
        self.surface = surface

    def display(self):
        pygame.draw.circle(self.surface, self.colour, self.x, self.y, self.size, self.thickness)

def isCollision (particleX, particleY, courserX, courserY):
    distance = math.sqrt(math.pow((particleX-courserX),2) + math.pow((particleY-courserY),2))
    if distance < 25:
        return True
    else: 
        return False

def show_score(x, y, score):
    scoreText = font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(scoreText,(x,y))

def show_trial(blockCureent,trialcurrent):
    scoreText = font.render("Block: " + str(blockCureent) + ", Trial: " + str(trialcurrent), True, (255,255,255))
    screen.blit(scoreText,(0,0))

def get_trial_length():
    trialLength = random.uniform(3,5)
    return trialLength



## Configs
subjectID = ''
amplitude = 100
length = 50.0
slow = 10
particleNumber = 5
trialNumber = 5
blockNumber = 2
randDelay = 1000
randLevelY = 0
randLevelX = 0
partcleSize = 20

variables = {}
variables['amplitude'] = amplitude
variables['length'] = length
variables['slow'] = slow
variables['randDelay'] = randDelay
variables['randLevelY'] = randLevelY
variables['randLevelX'] = randLevelX
variables['partcleSize'] = partcleSize

with open("variables.txt", "w") as file:
    file.write(json.dumps(variables))


particleFieldnames = ['subjectID', 'block', 'trial', 'randDelay', 'randLevelX',
'randLevelY', 'partcleSize','xPos', 'yPos']
filename = 'particle_result.csv'
result = {'subjectID':subjectID, 'block':0, 'trial':0, 
'randDelay':randDelay,'randLevelX':randLevelX,'randLevelY':randLevelY,
'partcleSize':partcleSize,'xPos':0,'yPos':0}
for i in range(particleNumber):
    keyTextX = 'Particle_'+str(i)+'_X'
    keyTextY = 'Particle_'+str(i)+'_Y'
    result.update({keyTextX:float('nan'),keyTextY:float('nan')})
    particleFieldnames = particleFieldnames+[keyTextX,keyTextY]
if not os.path.exists(filename):
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=particleFieldnames)
        writer.writeheader()


RTFieldnames = ['subjectID', 'block', 'trial', 'trialLen', 'RTTime', 'trialTime', 
'trialScore']
filename = 'RT_result.csv'
if not os.path.exists(filename):
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=RTFieldnames)
        writer.writeheader()

RTResult = {'subjectID':subjectID, 'block':0, 'trial':0, 'trialLen':0.0, 'RTTime':0.0,
'trialTime':0.0, 'trialScore':0}



particleList = list(range(particleNumber))
running = True
t0 = time.time()
tm = t0
click = 0
courserPos = (0,0)
totalScore = 0
trialcurrent = 1
blockCureent = 1
randY = [0]*particleNumber
randX = [0]*particleNumber
nextPage = False
scorePage = False
startPage = True
trialStart = True
trialTime = 0
RTSet = False

while running:
    surface.fill((0,50,50))
    events = pygame.event.get()
    currentTime = time.time()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     click = event.button
            # courserPos = event.pos
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RIGHT and nextPage == True:
                nextPage = False
                t0 = currentTime
                tm = t0
            elif event.key == pygame.K_SPACE and (trialTime > 0 and RTSet == False):
                responseTime = trialTime
                RTSet = True
                print('response: ' + str(round(responseTime,2)))
                

    if nextPage:
        nextText = font.render("Press [RIGHT ARROW] to go next", True, (150,255,100))
        screen.blit(nextText,(int(canvasWidth/2)-200,int(canvasHeight/2)-10))
        nextText = font.render("Press [ESCAPE] to exit", True, (150,255,100))
        screen.blit(nextText,(int(canvasWidth/2)-200,int(canvasHeight/2)+30))
    
    if scorePage:
        show_score(0,0,totalScore)
    
    if startPage:
        # Feed it with events every frame
        # textinput.update(events)
        # Blit its surface onto the screen
        nextText = font.render("Input Subject ID: ", True, (150,255,100))
        screen.blit(nextText,(10,10))
        screen.blit(textinput.get_surface(), (290, 10))

        pygame.display.update()
        if textinput.update(events):
            subjectID = textinput.get_text()
            print('Subject ID: '+ subjectID)
            nextPage = True
            startPage = False
            dateTime = datetime.now()
            particleFilename = (subjectID + "_particle_result_" + str(dateTime.year) + 
            str(dateTime.month) + str(dateTime.day) + str(dateTime.hour) 
            + str(dateTime.minute) + str(dateTime.second) + ".csv")
            RTFilename = (subjectID + "_RT_result_" + str(dateTime.year) + 
            str(dateTime.month) + str(dateTime.day) + str(dateTime.hour) 
            + str(dateTime.minute) + str(dateTime.second) + ".csv")
            print(particleFilename)
            print(RTFilename)
            
            if not os.path.exists(particleFilename):
                with open(particleFilename, mode='w', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=particleFieldnames)
                    writer.writeheader()
            
            if not os.path.exists(RTFilename):
                with open(RTFilename, mode='w', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=RTFieldnames)
                    writer.writeheader()



 
        clock.tick(30)
        


    courserPos = pygame.mouse.get_pos()
    if (blockCureent <= blockNumber) and nextPage == False and startPage == False:
        result['block'] = blockCureent
        if trialStart == True:
            trialStartTime = currentTime
            trialStart = False
            responseTime = float('nan')
            trialLength = get_trial_length()
            score = 0
            RTSet = False
        if trialcurrent <= trialNumber:
            result['trial'] = trialcurrent
            trialTime = currentTime-trialStartTime
            if trialTime < 1:
                surface.fill((50,50,50))
            for i in range(particleNumber):
                keyTextX = 'Particle_'+str(i)+'_X'
                keyTextY = 'Particle_'+str(i)+'_Y'
                result.update({keyTextX:float('nan'),keyTextY:float('nan')})
            if (len(particleList) > 0) and (trialTime<trialLength):
                t1 = currentTime
                tp = int(round((t1-t0)*1000))
                t = (tp / int(slow))  % (canvasWidth+particleNumber*50) # scale and loop time
                tn = t1
                randActive = False
                if (tn-tm)*1000 > randDelay:
                    randActive = True
                collisionList = []
                for i in particleList:
                    if randActive:
                        randY[i] = randint(0,randLevelY)
                        randX[i] = randint(0,randLevelX)
                    particleX = t-i*50
                    particleY = math.sin(particleX/length) * amplitude + (canvasHeight/2)       # scale sine wave
                    ranparticleY= int(particleY) + randY[i] 
                    ranparticleX = int(particleX) + randX[i]                  # needs to be int
                    firstPerticle = Particle(surface,ranparticleX,ranparticleY,partcleSize)
                    firstPerticle.display()
                    keyTextX = 'Particle_'+str(i)+'_X'
                    keyTextY = 'Particle_'+str(i)+'_Y'
                    result.update({keyTextX:particleX,keyTextY:particleY})
                    # click = pygame.mouse.get_pressed()
                    # if click == 1:
                    collision = isCollision(ranparticleX,ranparticleY,courserPos[0],courserPos[1])
                    if collision:
                        collisionList = i
                        score += 1
                if collisionList in particleList:
                    particleList.remove(collisionList)
                
                if randActive:
                    tm = tn
                    randActive = False
                result.update({'subjectID': subjectID, 'block':blockCureent, 'trial':trialcurrent,
                'randDelay':randDelay, 'randLevelX':randLevelX,
                'randLevelY':randLevelY, 'partcleSize':partcleSize,
                'xPos':courserPos[0],'yPos':courserPos[1]})
                with open(particleFilename, mode='a', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=particleFieldnames)
                    writer.writerow(result)
                show_trial(blockCureent,trialcurrent)

                # click = 0
            else:
                RTResult.update({'subjectID':subjectID, 'block':blockCureent, 'trial':trialcurrent, 
                'trialLen':trialLength, 'RTTime':responseTime, 'trialTime': trialTime, 'trialScore':score})
                trialcurrent += 1
                particleList = list(range(particleNumber))
                t0 = currentTime
                trialStart = True
                totalScore += score
                with open(RTFilename, mode='a', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=RTFieldnames)
                    writer.writerow(RTResult)


        else:
            blockCureent += 1
            trialcurrent = 1
            nextPage = True
    elif blockCureent > blockNumber:
        scorePage = True
    
    pygame.display.update()

    dicts_from_file = []
    with open('variables.txt','r') as inf:
        for line in inf:
            dicts_from_file.append(eval(line))
    if len(dicts_from_file) > 0:
        variables = dicts_from_file[0]
        amplitude = int(variables['amplitude'])
        length = float(variables['length'])
        slow = int(variables['slow'])
        randDelay = int(variables['randDelay'])
        randLevelY = int(variables['randLevelY'])
        randLevelX = int(variables['randLevelX'])
        partcleSize = int(variables['partcleSize'])

pygame.quit()    