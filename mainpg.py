#source: https://drive.google.com/file/d/0Bw3wtkey64tEcnpwdEpES2FvM28/view
import pygame
import time
import random
import rospy
import datetime
from std_msgs.msg import String
from random import randint

pygame.init()

display_width = 1920
display_height = 1080

# colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

startTime = 0
endTime = 0

font = pygame.font.SysFont('OpenSans-Regular.ttf', 35)

gameDisplay = pygame.display.set_mode((display_width,display_height))
#pygame.display.toggle_fullscreen()
pygame.display.set_caption('Picture Puzzle Game')
clock = pygame.time.Clock()
# background pics
background = pygame.image.load('background-azul.jpg')
backgroundGameLoop = pygame.image.load('blue.png')
# base pics
spring = pygame.image.load('bird.jpg')
winter = pygame.image.load('flower.jpg')
fall = pygame.image.load('apple.jpg')
summer = pygame.image.load('sun.jpg')
airplane = pygame.image.load('airplane.jpg')
avocado = pygame.image.load('avocado.jpg')
banana = pygame.image.load('banana.jpg')
boat = pygame.image.load('boat.jpg')
cherry = pygame.image.load('cherry.jpg')
dog = pygame.image.load('dog.jpg')
elephant = pygame.image.load('elephant.jpg')
fox = pygame.image.load('fox.jpg')
house = pygame.image.load('house.jpg')
light = pygame.image.load('light.jpg')
orange = pygame.image.load('orange.jpg')
penguin = pygame.image.load('penguin.jpg')
raccoon = pygame.image.load('raccoon.jpg')
raspberry = pygame.image.load('raspberry.jpg')
strawberry = pygame.image.load('strawberry.jpg')
whale = pygame.image.load('whale.jpg')
tree = pygame.image.load('tree.jpg')
tree2 = pygame.image.load('tree2.jpg')
greenapple = pygame.image.load('apple_green.jpg')
parrot = pygame.image.load('parrot.jpg')
rocket = pygame.image.load('rocket.jpg')

gameIcon = pygame.image.load('pictureIcon.png')
pygame.display.set_icon(gameIcon)

#random number array for behaviors
num_behaviors = 7
#list of num_behaviors random numbers, from 1 to num_behaviors
rand_behaviors = random.sample(range(1, num_behaviors), num_behaviors-1)

behavior_done = False

# file for recording data about participant's session
file = open('logfile{}.txt'.format(datetime.datetime.today().strftime('%Y-%m-%d_%H:%M:%S')), 'w')

file_bestScore = open('highscores.txt', 'r')
l1_bestScore = file_bestScore.readline()
l2_bestScore = file_bestScore.readline()
file_bestScore = open('highscores.txt', 'w')

file.write("Behaviors:\n")
file.write(str(rand_behaviors))
file.write("\n\nLevel, Start Time (sec), End Time (sec), Duration (sec) \n")
file.write(str(time.time()))

#array for keeping track of number of times behaviors are played
plays = [0,0,0,0,0,0]

rospy.init_node('talker', anonymous=True)
match_pub = rospy.Publisher('behavior_number', String, queue_size = 1)

def talker():
    pub = rospy.Publisher('trigger', String, queue_size = 1)
    rate = rospy.Rate(1)
    msg = "level completed"
    rospy.loginfo(msg)
    pub.publish(msg)
    rate.sleep()

def quitgame():
    pygame.quit()

    quit()

def button(msg,x,y,w,h,ib_c,ab_c,it_c,at_c,action=None):
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > pos[0] > x and y+h > pos[1] > y:
        pygame.draw.rect(gameDisplay, ab_c,(x,y,w,h))
        text(msg,x+(w/2),y+(h/2),20,at_c,'OpenSans-Bold.ttf')
        if click[0] == 1 and action != None:
            output_startTime(1)
            action()
    else:
        pygame.draw.rect(gameDisplay, ib_c,(x,y,w,h))
        text(msg,x+(w/2),y+(h/2),20,it_c,'OpenSans-Bold.ttf')

def button_cont(msg,x,y,w,h,ib_c,ab_c,it_c,at_c):
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > pos[0] > x and y+h > pos[1] > y:
        pygame.draw.rect(gameDisplay, ab_c,(x,y,w,h))
        text(msg,x+(w/2),y+(h/2),20,at_c,'OpenSans-Bold.ttf')
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(gameDisplay, ib_c,(x,y,w,h))
        text(msg,x+(w/2),y+(h/2),20,it_c,'OpenSans-Bold.ttf')
    return False



def text(msg, x, y, size, color, font, sysfont = False):
    if sysfont:
        font = pygame.font.SysFont(font,size)
    else: font = pygame.font.Font(font,size)
    TextSurf = font.render(msg, True, color)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((x),(y))
    gameDisplay.blit(TextSurf, TextRect)

def callback(data):
    if data.data == 'behavior completed':
        global behavior_done
        behavior_done = True
        return

def waiting_screen(n):
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(background, (00,00))
        # References to images used

        if n == 1:
            text('Great job! You completed level ' + str(n) + '.',(display_width/2),(display_height/2)-70,40,black,'OpenSans-Regular.ttf')
        else:
            text('Great job! You completed the game!',(display_width/2),(display_height/2)-70,40,black,'OpenSans-Regular.ttf')
        rate = rospy.Rate(1)
        rate.sleep()

        rate = rospy.Rate(1)
        if n == 0:
            msg = str(0)
        else:
            msg = str(rand_behaviors[n-1])
        #published number of random behavior to topic
        match_pub.publish(msg)
        rate.sleep()

        #subscribes to reward behavior, calls callback when published
        sub = rospy.Subscriber("kiwi", String, callback)
        if behavior_done:
            global behavior_done
            behavior_done = False
            return

        pygame.display.update()
        clock.tick(15)

def game_intro():
    print rand_behaviors
    pygame.mixer.music.pause()
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(background, (00,00))
        text('Picture Puzzle Game',display_width/2,display_height/4,60,black,'crackman.ttf')

        button("Start Game",(display_width/2)-100,585,200,100,white,black,black,white,game_loop)

        pygame.display.update()
        clock.tick(15)

def check_same(tile, choosen):
    l = []
    for i in range(len(tile)):
            if tile[i] == True:
                l.append(choosen[i])
    if len(l) == 2:
        return len(list(set(l))) != len(l)
    if len(l) == 4:
        return len(list(set(l))) != len(l) - 1
    elif len(l) == 6:
        return len(list(set(l))) != len(l) - 2
    else:
        return len(list(set(l))) != len(l) - 3

def l_random(level = 1):
    # 3 x 2
    # 4 x 2
    l=[[raspberry, orange, greenapple, avocado],[elephant, fox, raccoon, penguin]]
    l_final =[]
    while len(l_final) != len(l[level-1])*2:
        choice = l[level-1][random.randint(0,len(l[level-1])-1)]
        if l_final.count(choice) <= 1 : l_final.append(choice)
    return l_final

def output_startTime(level):
    seconds = time.time()
    file.write("{}, {}, ".format(level, seconds))
    global startTime
    startTime = float(seconds)

def output_endTime(level):
    seconds = float(time.time())
    global startTime
    file.write('{}, {}\n'.format(seconds, seconds - startTime))

def output_plays():
    translation = {1: 'dance', 2:'compliment', 3:'encouragement', 4:'sassy remark', 5:'joke', 6:'dance with music'}
    file.write("\n")
    for behavior in rand_behaviors:
        file.write("{}, ".format(translation[behavior]))

    file.write("\n")

    for count in plays:
        file.write("{}, ".format(count))

def displayTime(t0):
    time_string = "Your Time: {}".format((pygame.time.get_ticks()/1000) - (t0/1000))
    text = font.render(time_string, True, white)
    gameDisplay.blit(text, (display_width/6, display_height/8))

def displayHighScore(n):
    if(n == 1):
        score = "Best Time: " + str(l1_bestScore).strip('\n\r')
    else:
        score = "Best Time: " + str(l2_bestScore).strip('\n\r')
    text = font.render(score, True, white)
    gameDisplay.blit(text, (display_width/6, display_height/8 - 100))

def updateHighScore(n, score):
    global l1_bestScore
    global l2_bestScore
    print score
    if n == 1:
        if score < l1_bestScore:
            l1_bestScore = score
        file_bestScore.write(str(l1_bestScore) + '\n')
    else:
        if score < l2_bestScore:
            l2_bestScore = score
        file_bestScore.write(str(l2_bestScore) + '\n')

def game_loop(level = 1, oldchoosen = None, oldtile = None, old_x = None, t0 = 0):
    choosen = None
    # time.sleep(0.1)
    if old_x != None:
        x = old_x
    else:
        x = 1
    Won = None
    gameExit = False
    if oldtile != None:
        tile = oldtile[:]
    else:
        tile = [False, False, False, False, False, False, False, False]
    tile1 = tile[0]
    tile2 = tile[1]
    tile3 = tile[2]
    tile4 = tile[3]
    tile5 = tile[4]
    tile6 = tile[5]
    tile7 = tile[6]
    tile8 = tile[7]
    if oldchoosen != None:
        choosen = oldchoosen[:]
    else:
        choosen = l_random(level)

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #displayTime()
        #text('Time ' + str(pygame.time.get_ticks()/1000),display_width/2,display_height/8 ,35,white,'zerovelo.ttf')
        gameDisplay.blit(backgroundGameLoop,(0,0))
        displayTime(t0)
        displayHighScore(level)
        text('Level ' + str(level),display_width/2,display_height/8,35,white,'zerovelo.ttf')
        gameDisplay.blit(choosen[0],(660,280))
        gameDisplay.blit(choosen[1],(860,280))
        gameDisplay.blit(choosen[2],(1060,280))
        gameDisplay.blit(choosen[3],(660,480))
        gameDisplay.blit(choosen[4],(860,480))
        gameDisplay.blit(choosen[5],(1060,480))
        gameDisplay.blit(choosen[6],(760,680))
        gameDisplay.blit(choosen[7],(960,680))

        if (Won == True):
            if level == 1 and tile.count(True) == 8:
                updateHighScore(level, pygame.time.get_ticks()/1000)
                output_endTime(level)
                talker()
                waiting_screen(level)
                output_startTime(level+1)
                t0 = pygame.time.get_ticks()
                game_loop(level+1, t0 = t0)
            if level == 2 and tile.count(True) == 8:
                updateHighScore(level, pygame.time.get_ticks()/1000)
                talker()
                waiting_screen(level)
                game_intro()


            game_loop(level, choosen, tile, x, t0)
            Won = None

        if (Won == False):
            # time.sleep(0.4)
            game_loop(level, choosen, t0 = t0)

        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()


        if 860 > pos[0] > 660 and 480 > pos[1] > 280 and click[0] == 1:
             tile1 = True
        if 1060 > pos[0] > 860 and 480 > pos[1] > 280 and click[0] == 1:
             tile2 = True
        if 1260 > pos[0] > 1060 and 480 > pos[1] > 280 and click[0] == 1:
             tile3 = True
        #row 2
        if 860 > pos[0] > 660 and 680 > pos[1] > 480 and click[0] == 1:
             tile4 = True
        if 1060 > pos[0] > 860 and 680 > pos[1] > 480 and click[0] == 1:
             tile5 = True
        if 1260 > pos[0] > 1060 and 680 > pos[1] > 480 and click[0] == 1:
             tile6 = True
        #row3
        if 960 > pos[0] > 760 and 880 > pos[1] > 680 and click[0] == 1:
             tile7 = True
        if 1160 > pos[0] > 960 and 880 > pos[1] > 680 and click[0] == 1:
             tile8 = True


        tile = [tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8]
        #print tile
        if tile.count(True) > x:
            if check_same(tile, choosen) == True:
                Won = True
                x += 2
                match_pub.publish("matched " + str(x-1))
            else:
                match_pub.publish("lost")
                Won = False


        if not tile1: pygame.draw.rect(gameDisplay, white, (660,280,200,200))
        if not tile2: pygame.draw.rect(gameDisplay, white, (860,280,200,200))
        if not tile3: pygame.draw.rect(gameDisplay, white, (1060,280,200,200))
        if not tile4: pygame.draw.rect(gameDisplay, white, (660,480,200,200))
        if not tile5: pygame.draw.rect(gameDisplay, white, (860,480,200,200))
        if not tile6: pygame.draw.rect(gameDisplay, white, (1060,480,200,200))
        if not tile7: pygame.draw.rect(gameDisplay, white, (760,680,200,200))
        if not tile8: pygame.draw.rect(gameDisplay, white, (960,680,200,200))


        # horizontal
        pygame.draw.line(gameDisplay, black, (660,280),(1260,280),5)
        pygame.draw.line(gameDisplay, black, (660,480),(1260,480),5)
        pygame.draw.line(gameDisplay, black, (660,680),(1260,680),5)
        pygame.draw.line(gameDisplay, black, (760,880),(1160,880),5)
        # vertical
        pygame.draw.line(gameDisplay, black, (660,280),(660,680),5)
        pygame.draw.line(gameDisplay, black, (860,280),(860,680),5)
        pygame.draw.line(gameDisplay, black, (1060,280),(1060,680),5)
        pygame.draw.line(gameDisplay, black, (1260,280),(1260,680),5)
        pygame.draw.line(gameDisplay, black, (760,680),(760,880),5)
        pygame.draw.line(gameDisplay, black, (960,680),(960,880),5)
        pygame.draw.line(gameDisplay, black, (1160,680),(1160,880),5)

        pygame.display.update()
        clock.tick(100)

game_intro()
pygame.quit()
quit()
