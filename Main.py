import pygame
import time
import random

pygame.init()

LIGHTBLUE = (153, 255, 255)
BLACK = (  0,  0,  0)
WHITE = (255, 255, 255)
LIGHTYELLOW = (245, 229, 130)
PINK = (204, 153, 255)
GREY = (235, 230, 204)

font1 = pygame.font.SysFont("calibri", 35)
font2 = pygame.font.SysFont("vivaldi", 40)
font3 = pygame.font.SysFont("comicsansms", 40)

win_width = 460
win_height = 600

win = pygame.display.set_mode((win_width, win_height))

inPlay = True
page = "Start"
mousePos = (0,0)
block_list = []
block_pos_list = []
waitForResponse = False
able_to_move = True
moved_this_time = False
score = 0
f = open("record.txt", "r")
best_score = int(f.readlines()[0].strip("\n"))

class Block:

    def __init__(self, length, thickness, number, pos, occupied=False, getByMerged=False):
        self.length = length
        self.thickness = thickness
        self.number = number
        self.pos = pos
        self.occupied = occupied
        self.getByMerged = getByMerged

    def draw(self, size, block_length):
        rect = pygame.Rect(self.pos, (block_length, block_length))
        if self.occupied == False:
            pygame.draw.rect(win, BLACK, rect, self.thickness)
        else:
            if self.number == 2:
                pygame.draw.rect(win, (217, 217, 217), rect)
            elif self.number == 4:
                pygame.draw.rect(win, (255, 230, 230), rect)
            elif self.number == 8:
                pygame.draw.rect(win, (255, 153, 102), rect)
            elif self.number == 16:
                pygame.draw.rect(win, (255, 102, 26), rect)
            elif self.number == 32:
                pygame.draw.rect(win, (255, 153, 102), rect)
            elif self.number == 64:
                pygame.draw.rect(win, (204, 68, 0), rect)
            elif self.number == 128:
                pygame.draw.rect(win, (255, 150, 153), rect)
            elif self.number == 256:
                pygame.draw.rect(win, (255, 150, 0), rect)
            elif self.number == 512:
                pygame.draw.rect(win, (255, 255, 0), rect)
            elif self.number == 1024:
                pygame.draw.rect(win, (204, 255, 153), rect)
            elif self.number == 2048:
                pygame.draw.rect(win, (153, 255, 51), rect)

        if self.occupied == True:
            font = self.adjustFont(block_length)
            text_surface = font.render(str(self.number), True, BLACK)
            width = text_surface.get_width()
            height = text_surface.get_height()
            text_pos = Button.center((block_length, block_length), (width, height), True, True, self.pos)
            win.blit(text_surface, (self.pos[0]+text_pos[0]+4, self.pos[1]+text_pos[1]+3))

    @staticmethod
    def horizontalCheck(index, size):
        global block_list

        if index%size != 0:
            while block_list[index-1].occupied == False:
                block_list[index], block_list[index-1] = block_list[index-1], block_list[index]

    @staticmethod
    def verticalCheck(index, size):
        global block_size

        if index >= size:
            while block_list[index-size].occupied == False:
                block_list[index], block_list[index-size] = block_list[index-size], block_list[index]


    def move(self, direction, index, size):
        global block_list

        moved = False

        if direction == "up":
            switchCount = 0
            numberDuplicate = block_list[index].number
            while index >= size:
                if block_list[index-size].occupied == False:
                    block_list[index-size].number = block_list[index].number
                    block_list[index-size].occupied = True
                    block_list[index].occupied = False
                    block_list[index].number = 0
                    block_list[index].draw(size, block_list[index].length)
                    block_list[index-size].draw(size, block_list[index].length)
                    if index+size < len(block_list):
                        rect = pygame.Rect(block_list[index+size].pos, (self.length, self.length))
                        pygame.draw.rect(win, LIGHTYELLOW, rect)
                        block_list[index+size].draw(size, block_list[index].length)
                    pygame.display.update()
                    index -= size
                    moved = True
                else:
                    if block_list[index-size].number == block_list[index].number:
                        moved = True
                        if index > 2*size - 1:
                            if block_list[index-size].number == block_list[index-2*size].number:
                                if block_list[index-size].getByMerged == False and block_list[index-2*size].getByMerged == False:
                                     self.merge("up", index-size, size)
                                     block_list[index-2*size].getByMerged = True
                            else:
                                if block_list[index].getByMerged == False and block_list[index-size].getByMerged == False:
                                    self.merge("up", index, size)
                                    block_list[index-size].getByMerged = True
                        else:
                            if block_list[index].getByMerged == False and block_list[index-size].getByMerged == False:
                                self.merge("up", index, size)
                                block_list[index-size].getByMerged = True
                    index -= size
        #    block_list[index-size*switchCount], block_list[index] = block_list[index], block_list[index-size*switchCount]
        elif direction == "down":
            switchCount = 0
            numberDuplicate = block_list[index].number
            while index >= size:
                if block_list[index-size].occupied == False:
                    block_list[index-size].number = block_list[index].number
                    block_list[index-size].occupied = True
                    block_list[index].occupied = False
                    block_list[index].number = 0
                    block_list[index].draw(size, block_list[index].length)
                    block_list[index-size].draw(size, block_list[index].length)
                    if index+size < len(block_list):
                        rect = pygame.Rect(block_list[index+size].pos, (self.length, self.length))
                        pygame.draw.rect(win, LIGHTYELLOW, rect)
                        block_list[index+size].draw(size, block_list[index].length)
                    pygame.display.update()
                    index -= size
                    moved = True
                else:
                    if block_list[index-size].number == block_list[index].number:
                        moved = True
                        if index > 2*size - 1:
                            if block_list[index-size].number == block_list[index-2*size].number:
                                if block_list[index-size].getByMerged == False and block_list[index-size].getByMerged == False:
                                     self.merge("down", index-size, size)
                                     block_list[index-2*size].getByMerged = True
                            else:
                                if block_list[index].getByMerged == False and block_list[index-size].getByMerged == False:
                                    self.merge("down", index, size)
                                    block_list[index-size].getByMerged = True
                        else:
                            if block_list[index].getByMerged == False and block_list[index-size].getByMerged == False:
                                self.merge("down", index, size)
                                block_list[index-size].getByMerged = True
                    index -= size
        #    block_list[index+size*switchCount], block_list[index] = block_list[index], block_list[index+size*switchCount]

        elif direction == "left":
            numberDuplicate = block_list[index].number
            while index%size > 0:
                if block_list[index-1].occupied == False:
                    block_list[index-1].number = block_list[index].number
                    block_list[index-1].occupied = True
                    block_list[index].occupied = False
                    block_list[index].number = 0
                    block_list[index].draw(size, block_list[index].length)
                    block_list[index-1].draw(size, block_list[index].length)
                    if (index+1)%size != 0:
                        rect = pygame.Rect(block_list[index+1].pos, (self.length, self.length))
                        pygame.draw.rect(win, LIGHTYELLOW, rect)
                        block_list[index+1].draw(size, block_list[index].length)
                    pygame.display.update()
                    index -= 1
                    moved = True
                else:
                    if block_list[index-1].number == block_list[index].number:
                        moved = True
                        if (index-1)%size != 0:                 #  and (index+2)//size < (index+2)/size
                            if block_list[index-2] == block_list[index-1]:
                                if block_list[index-1].getByMerged == False and block_list[index-2].getByMerged == False:
                                    self.merge("left", index+1, size)
                                    block_list[index-2].getByMerged = True
                            #        if block_list[index-1].occupied == True:            # go back and check any blocks left
                            #            index -= 2
                            else:
                                if block_list[index].getByMerged == False and block_list[index-1].getByMerged == False:
                                    self.merge("left", index, size)
                                    block_list[index-1].getByMerged = True
                        else:
                            if block_list[index].getByMerged == False and block_list[index-1].getByMerged == False:
                                self.merge("left", index, size)
                                block_list[index-1].getByMerged = True
                    index -= 1

        elif direction == "right":
        #    index = size**2 - 1 - index

            numberDuplicate = block_list[index].number
            while index%size > 0:
                if block_list[index-1].occupied == False:
                    block_list[index-1].number = block_list[index].number
                    block_list[index-1].occupied = True
                    block_list[index].occupied = False
                    block_list[index].number = 0
                    block_list[index].draw(size, block_list[index].length)
                    block_list[index-1].draw(size, block_list[index].length)
                    if (index+1)%size != 0:
                        rect = pygame.Rect(block_list[index+1].pos, (self.length, self.length))
                        pygame.draw.rect(win, LIGHTYELLOW, rect)
                        block_list[index+1].draw(size, block_list[index].length)
                    pygame.display.update()
                    index -= 1
                    moved = True
                else:
                    if block_list[index-1].number == block_list[index].number:
                        moved = True
                        if (index-1)%size != 0:                 #  and (index+2)//size < (index+2)/size
                            if block_list[index-2] == block_list[index-1]:
                                if block_list[index-1].getByMerged == False and block_list[index-2].getByMerged == False:
                                    self.merge("right", index-1, size)
                                    block_list[index-2].getByMerged = True
                            #        if block_list[index-1].occupied == True:            # go back and check any blocks left
                            #            index -= 2
                            else:
                                if block_list[index].getByMerged == False and block_list[index-1].getByMerged == False:
                                    self.merge("right", index, size)
                                    block_list[index-1].getByMerged = True
                        else:
                            if block_list[index].getByMerged == False and block_list[index-1].getByMerged == False:
                                self.merge("right", index, size)
                                block_list[index-1].getByMerged = True
                    index -= 1

        return moved


    def merge(self, direction, index, size):
        global block_list
        global score

        if direction == "up":
            block_list[index-size].number += block_list[index].number
            Block.verticalCheck(index, size)

        elif direction == "down":
            block_list[index-size].number += block_list[index].number
            Block.verticalCheck(index, size)

        elif direction == "left":
            block_list[index-1].number += block_list[index].number
            Block.horizontalCheck(index, size)

        elif direction == "right":
            block_list[index-1].number += block_list[index].number
            Block.horizontalCheck(index, size)

        score += block_list[index].number * 2
        block_list[index].occupied = False
        block_list[index].number = 0

    def adjustFont(self, block_length):
        fontSize = 1
        searching = True
        font4 = pygame.font.SysFont("verdana", fontSize)
        text_surface = font4.render(str(self.number), True, BLACK)
        width = text_surface.get_width()
        height = text_surface.get_height()
        while searching:
            if width < block_length and height < block_length:
                fontSize += 1
                font4 = pygame.font.SysFont("ebrima", fontSize)
                text_surface = font4.render(str(self.number), True, BLACK)
                width = text_surface.get_width()
                height = text_surface.get_height()
            else:
                searching = False
        return font4




class Button:

    def __init__(self, text, buttonColor, textColor, fontNum):
        self.text = text
        self.buttonColor = buttonColor
        self.textColor = textColor
        self.fontNum = fontNum
        self.allTheButton = {}

    def generateRect(self, pos, landscape, portrait):
        if self.fontNum == 1:
            text_surface = font1.render(self.text, True, self.textColor)
        elif self.fontNum == 2:
            text_surface = font2.render(self.text, True, self.textColor)
        elif self.fontNum == 3:
            text_surface = font3.render(self.text, True, self.textColor)
        width = text_surface.get_width()
        height = text_surface.get_height()
        pos = Button.center((win_width, win_height), (width, height), landscape, portrait, pos)
        rect = pygame.Rect(pos, (width+10, height+10))

        self.allTheButton[self.text] = rect
        return rect, text_surface, pos

    def draw(self, pos, landscape, portrait):
        rect, text_surface, pos = self.generateRect(pos, landscape, portrait)
        pygame.draw.rect(win, self.buttonColor, rect)
        win.blit(text_surface, (pos[0]+5, pos[1]+5))

    @staticmethod
    def center(winSize, textSize, landscape, portrait, originalPos):          # winSize and textSize takes one tuple
        if landscape == True and portrait == True:
            return (winSize[0]/2-textSize[0]/2-5, winSize[1]/2-textSize[1]/2-5)
        elif landscape == True and portrait == False:
            return (winSize[0]/2-textSize[0]/2-5, originalPos[1])
        elif landscape == False and portrait == True:
            return (originalPos[0], winSize[1]/2-textSize[1]/2-5)
        else:
            return originalPos

    def isClicked(self, mousePos):
        rect = self.allTheButton[self.text]
        if rect.collidepoint(mousePos):
            return True
        else:
            return False



def generateGridPosList(size, win_width, win_height):       # size refers to how many rows and columns
    pos_list = []
    block_width = (win_width*2/3-5*(size+1)) / size
    block_height = block_width
    for i in range(size**2):               # generate size**2 blocks
        pos_list.append((win_width/6+5*(i%size)+block_width*(i%size), win_height-360+block_height*(i//size)+5*(i//size)))
    return pos_list, block_width

def generateNumber(size):
    num1 = random.randint(0,8)
    num2 = random.randint(0,size**2-1)
    if num1 == 0:
        return 4, num2
    else:
        return 2, num2

def listRecover(aList):
    recoveredList = []
    stringForCombine = ""
    for item in aList:
        if item.isnumeric() == True or item == ".":
            stringForCombine += item
        else:
            if stringForCombine != "":
                recoveredList.append(stringForCombine)
            stringForCombine = ""
    for i,num in enumerate(recoveredList):
        if "." in num:
            recoveredList[i] = float(num)
        else:
            recoveredList[i] = int(num)
    return recoveredList

def classListCopy(theList):
    newList = []
    for object in theList:
        length = object.length
        thickness = object.thickness
        number = object.number
        pos = object.pos
        occupied = object.occupied
        getByMerged = object.getByMerged
        newObject = Block(length,thickness,number,pos,occupied,getByMerged)
        newList.append(newObject)
    return newList



def draw_start_menu(page):
    global best_score
    global block_list
    global block_length
    global block_pos_list
    global score
    global waitForResponse

    image = pygame.image.load(r'C:\Study\VS Code\Pygames\2048\2048.png')
    image = pygame.transform.scale(image, (win_width, win_height))
    win.blit(image, (0,0))
    startButton = Button("New Game", GREY, BLACK, 2)
    startButton.draw((0,400), True, False)
    continueButton = Button("Continue", GREY, BLACK, 2)
    continueButton.draw((0,450), True, False)
    if startButton.isClicked(mousePos):
        page = "choosingMood"
        print ("cm clicked")
        time.sleep(0.3)
        return page, False
    elif continueButton.isClicked(mousePos):
        f = open("record.txt", "r")
        lines = f.readlines()
        best_score = lines[0].strip("\n")
        block_length = float(lines[1].strip("\n"))
        thickness = int(lines[2].strip("\n"))
        num_list = listRecover(lines[3])
        pos_list = listRecover(lines[4])
        occupied_list = listRecover(lines[5])
        getByMerged_list = listRecover(lines[6])
        score = int(lines[7].strip("\n"))
        for i,num in enumerate(num_list):
            block_pos_list.append((pos_list[i*2],pos_list[i*2+1]))
            block_list.append(Block(block_length, thickness, num, block_pos_list[i], occupied_list[i], getByMerged_list[i]))
        f.close()
        size = int(len(block_list) ** (1/2))
        page = "play" + str(size)
        print ("p clicked", page)
        time.sleep(0.3)
        return page, True
    else:
        return page, False


def draw_choosing_window(page):
    global block_length
    global block_pos_list

    titleButton = Button("Choose the mood", LIGHTYELLOW, BLACK, 3)
    titleButton.draw((0,50), True, False)
    twoByTwoButton = Button("2 * 2", GREY, BLACK, 3)
    twoByTwoButton.draw((0,180), True, False)
    threeByThreeButton = Button("3 * 3", GREY, BLACK, 3)
    threeByThreeButton.draw((0, 280), True, False)
    fourByFourButton = Button("4 * 4", GREY, BLACK, 3)
    fourByFourButton.draw((0,380), True, False)
    eightByEightButton = Button("8 * 8", GREY, BLACK, 3)
    eightByEightButton.draw((0, 480), True, False)
    if twoByTwoButton.isClicked(mousePos):
        page = "play2"
        print ("p2 clicked")
        block_pos_list,block_length = generateGridPosList(2, win_width, win_height)     # block width/height/length are the same

    elif threeByThreeButton.isClicked(mousePos):
        page = "play3"
        print ("p3 clicked")
        block_pos_list,block_length = generateGridPosList(3, win_width, win_height)

    elif fourByFourButton.isClicked(mousePos):
        page = "play4"
        print ("p4 clicked")
        block_pos_list,block_length = generateGridPosList(4, win_width, win_height)

    elif eightByEightButton.isClicked(mousePos):
        page = "play8"
        print ("p8 clicked")
        block_pos_list,block_length = generateGridPosList(8, win_width, win_height)

    if block_pos_list != []:
        for block_pos in block_pos_list:
            block_list.append(Block(block_length, 2, 0, block_pos))

    return page


def draw_game_window():
    global score
    global best_score
    global best
    global block_length
    global mousePos
    global block_list_duplicate
    global block_list

    block_list_copy = block_list[:]

    undoButton = Button("Undo", GREY, BLACK, 1)
    undoButton.draw((100, 115), False, False)
    if undoButton.isClicked(mousePos):
        print (block_list[14].number, block_list_duplicate[14].number)
        block_list_copy = classListCopy(block_list_duplicate)
        print ("")
    scoreButton = Button("Score: "+str(score), LIGHTYELLOW, BLACK, 1)
    scoreButton.draw((240, 115), False, False)
    best = score
    bestButton = Button("Best: "+str(best_score), LIGHTYELLOW, BLACK, 1)
    bestButton.draw((240, 65), False, False)
    size = len(block_list)**(1/2)
    length = block_length*(size) + 5*(size+1)
    rect = pygame.Rect((block_pos_list[0][0]-5, block_pos_list[0][1]-5),(length, length))
    pygame.draw.rect(win, BLACK, rect, 3)


    if page == "play2":
        for block in block_list:
            block.draw(2, block_length)

    elif page == "play3":
        for block in block_list:
            block.draw(3, block_length)

    elif page == "play4":
        for block in block_list:
            block.draw(4, block_length)

    elif page == "play8":
        for block in block_list:
            block.draw(8, block_length)

    return block_list_copy



def redraw_game_window(page, block_list, waitForResponse):
    global block_pos_list
    global block_length
    global moved_this_time

    win.fill(LIGHTYELLOW)

    if page == "Start":
        page, waitForResponse = draw_start_menu(page)


    elif page == "choosingMood":
        page = draw_choosing_window(page)

    elif page == "play2":
        block_list = draw_game_window()
        while not waitForResponse:
            number1, number2 = generateNumber(2)
            if block_list[number2].occupied == False:
                block_list[number2].number = number1
                block_list[number2].occupied = True
                waitForResponse = True
        moved_this_time = False

    elif page == "play3":
        block_list = draw_game_window()
        while not waitForResponse:
            number1, number2 = generateNumber(3)
            if block_list[number2].occupied == False:
                block_list[number2].number = number1
                block_list[number2].occupied = True
                waitForResponse = True
        moved_this_time = False

    elif page == "play4":
        block_list = draw_game_window()
        while not waitForResponse:
            number1, number2 = generateNumber(4)
            if block_list[number2].occupied == False:
                block_list[number2].number = number1
                block_list[number2].occupied = True
                waitForResponse = True
        moved_this_time = False

    elif page == "play8":
        block_list = draw_game_window()
        while not waitForResponse:
            number1, number2 = generateNumber(8)
            if block_list[number2].occupied == False:
                block_list[number2].number = number1
                block_list[number2].occupied = True
                waitForResponse = True
        moved_this_time = False


    pygame.display.update()

    return page, block_list, waitForResponse

while inPlay:
    page, block_list, waitForResponse = redraw_game_window(page, block_list, waitForResponse)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False

        if event.type == pygame.MOUSEBUTTONDOWN:
             mousePos = pygame.mouse.get_pos()
        else:
            mousePos = (0,0)

        if event.type == pygame.KEYDOWN:
            block_list_duplicate = classListCopy(block_list)
            print ("before", block_list[14].number, "----------------")
            if event.key == pygame.K_DOWN:
                waitForResponse = False
                block_list.reverse()
                for i,block in enumerate(block_list):
                    if block.occupied == True:
                        able_to_move = block.move("down", i, int(len(block_list)**(1/2)))
                        if able_to_move == True:
                            moved_this_time = True
                block_list.reverse()

            elif event.key == pygame.K_UP:
                waitForResponse = False
                for i,block in enumerate(block_list):
                    if block.occupied == True:
                        able_to_move = block.move("up", i, int(len(block_list)**(1/2)))
                        if able_to_move == True:
                            moved_this_time = True

            elif event.key == pygame.K_RIGHT:
                waitForResponse = False
                block_list.reverse()
                for i,block in enumerate(block_list):
                    if block.occupied == True:
                        able_to_move = block.move("right", i, int(len(block_list)**(1/2)))
                        if able_to_move == True:
                            moved_this_time = True
                block_list.reverse()

            elif event.key == pygame.K_LEFT:
                waitForResponse = False
                for i,block in enumerate(block_list):
                    if block.occupied == True:
                        able_to_move = block.move("left", i, int(len(block_list)**(1/2)))
                        if able_to_move == True:
                            moved_this_time = True
            else:
                waitForResponse = True

            print (block_list[14].number)
            print ("Another list", block_list_duplicate[14].number)

            if moved_this_time == False:
                waitForResponse = True

            for block in block_list:
                if block.getByMerged == True:
                    block.getByMerged = False

pygame.quit()

f = open("record.txt", "r")
content = f.readlines()
f.close()
f = open("record.txt", "w")
if score > int(content[0]):
    content[0] = str(score)+"\n"

block_number_list = []
block_pos_list = []
block_occupied_list = []
block_getByMerged_list = []

for block in block_list:
    block_length = block.length
    block_thickness = block.thickness
    block_number_list.append(block.number)
    block_pos_list.append(block.pos)
    block_occupied_list.append(int(block.occupied))
    block_getByMerged_list.append(int(block.getByMerged))

content[1] = str(block_length)+"\n"
content[2] = str(block_thickness)+"\n"
content[3] = str(block_number_list)+"\n"
content[4] = str(block_pos_list)+"\n"
content[5] = str(block_occupied_list)+"\n"
content[6] = str(block_getByMerged_list)+"\n"
content[7] = str(score)

for line in content:
    f.write(line)
f.close()
