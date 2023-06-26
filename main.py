#Developer: Mukesh Sabesan
import pygame
import math
import random
import time
pygame.init()


info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

WIN = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
pygame.display.set_caption("Aim Trainer") #sets name of window

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30
BG_COLOUR = (0, 25, 40)

LABEL_FONT = pygame.font.SysFont("fixedsys500c", 34)

class Target:
    MAX_SIZE = 30
    COLOR = "blue"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self, mode):
       # if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
         #   self.grow = False
        
        if self.grow:
            if mode == 0:
                self.size = self.MAX_SIZE
            elif mode == 1:
                self.size = self.MAX_SIZE - 10
            else:
                self.size = self.MAX_SIZE - 20
        else:
            self.size = 0

    def draw(self, win, mode):
        if mode == 0:
            pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        elif mode == 1:
            pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        else:
            pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        
      # pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.8)
      # pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
      # pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.4)
    
    def collide(self, x, y):
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.size
    
def draw(win, targets, mode):
    win.fill(BG_COLOUR)

    for target in targets:
        target.draw(win, mode)



def format_time(secs):
    milli = math.floor(int(secs*1000 % 1000)/ 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, elapsed_time, targets_pressed, mode, clicks):
    mode_dict = {0: "Easy",
                 1: "Medium",
                 2: "Hard"}
    
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, 50))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")
    mode_label = LABEL_FONT.render(f"Mode: {mode_dict[mode]}", 1, "black")
    try:
        accuracy_label = LABEL_FONT.render(f"Accuracy: {round(targets_pressed/clicks *100)}%", 1, "black")
    except ZeroDivisionError:
        accuracy_label = LABEL_FONT.render(f"Accuracy: 0%", 1, "black")
    

    win.blit(time_label, (5,5))
    win.blit(speed_label, (200,5))
    win.blit(hits_label, (450,5))
    win.blit(mode_label, (600,5))
    win.blit(accuracy_label, (800, 5))

def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill("grey")
    
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")
    try:
        accuracy_label = LABEL_FONT.render(f"Accuracy: {round(targets_pressed/clicks *100)}%", 1, "black")
    except ZeroDivisionError:
        accuracy_label = LABEL_FONT.render(f"Accuracy: 0%", 1, "black")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label),200))
    win.blit(hits_label, (get_middle(hits_label),300))
    win.blit(accuracy_label, (get_middle(time_label), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        
            if event.type == pygame.KEYDOWN:
                run = False
                break
            
def get_middle(surface):
    return WIDTH /2 - surface.get_width()/2
def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    mode = 0
    target_limit = 7
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_position = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + 50, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                if(len(targets) < target_limit):
                    targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
            
        for target in targets:
           target.update(mode)

           if click and target.collide(*mouse_position):
                targets.remove(target)
                targets_pressed += 1

        if mode == 1:
            target_limit = 9
        if mode == 2:
            target_limit = 11

        if (targets_pressed >= 100 and targets_pressed <= 199):
            mode = 1
        if(targets_pressed >= 200):
            mode = 2
        if(elapsed_time > 60 and mode != 2):
            mode = 1

        if(elapsed_time >= 90):
            end_screen(WIN, elapsed_time, targets_pressed, clicks)

      
        draw(WIN, targets, mode)
        draw_top_bar(WIN, elapsed_time, targets_pressed, mode, clicks)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()