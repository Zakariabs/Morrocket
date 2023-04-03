import pygame.mixer
import pygame 
import os
import random

pygame.font.init()  # we gaan de font inladen
pygame.mixer.init()  # we gaan de muziek inladen


WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Morrocket Game")

# Space achtergrond inladen
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "Space_BG_2.png")), (WIDTH, HEIGHT))


# we gaan de beelden inladen

RED_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png"))
UFO_SPACE_SHIP = pygame.image.load(os.path.join("assets", "ufo_enemy.png"))
BLUE_BATTLE_SHIP = pygame.image.load(
    os.path.join("assets", "Blue_battle_ship.png"))

# speler schip inladen
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "ufo.png"))
UFFO_SPACE_SHIP = pygame.image.load(os.path.join("assets", "Blue_battle_ship.png"))
# Lasers inladen
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))
SPECIAL_LASER = pygame.image.load(os.path.join("assets", "special_laser.png"))




# we gaan laser class maken
# zo kunnen we de lasers laten bewegen en laten verdwijnen als ze van het scherm zijn


enemy_laser_sound = pygame.mixer.Sound(
    "gamesound/laser_sound.wav")  # we gaan de laser geluid inladen
player_laser_sound = pygame.mixer.Sound(
    "gamesound/playersound.wav")  # we gaan de laser geluid inladen
collision_sound = pygame.mixer.Sound(
    "gamesound/collision_sound.wav")  # we gaan de closs geluid inladen
game_sound = pygame.mixer.Sound("gamesound/gamemusic.mp3")
enemy_laser_sound.set_volume(0.5)
game_sound.set_volume(0.6)


# we maken SHip class aan zodat we de player en enemy class kunnen aanroepen


class Ship:
    COOLDOWN = 30  # cooldown van de laser

    def __init__(self, x, y, health=100):
        self.x = x      # x positie van het schip
        self.y = y      # y positie van het schip
        self.health = health    # health van het schip
        self.ship_img = None  # we gaan de afbeelding van het schip inladen
        self.laser_img = None  # we gaan de afbeelding van de laser inladen
        self.lasers = []  # we gaan de lasers in een lijst zetten
        self.cool_down_counter = 0  # cooldown counter

    def draw(self, window):  # we gaan het schip tekenen
        # we gaan de afbeelding van het schip tekenen
        window.blit(self.ship_img, (self.x, self.y))
        self.self_lasers = self.lasers
        for laser in self.self_lasers:  # we gaan de lasers tekenen
            laser.draw(window)  # we gaan de laser tekenen
            # we gaan het laser geluid afspelen

    def move_lasers(self, vel, obj):  # we gaan de lasers laten bewegen
        self.cooldown()  # we gaan de cooldown functie aanroepen
        for laser in self.lasers:  # we gaan de lasers laten bewegen en kijken of ze van het scherm zijn
            laser.move(vel)  # we gaan de laser laten bewegen

            # als de laser van het scherm is dan verwijderen we de laser
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            # als de laser een object raakt dan verwijderen we de laser
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):  # we gaan de cooldown functie aanroepen om de cooldown van de laser te regelen
        # als de cooldown counter groter is dan de cooldown dan zetten we de cooldown counter op 0
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:  # als de cooldown counter groter is dan 0 dan zetten we de cooldown counter op 1
            self.cool_down_counter += 1

    def shoot(self):  # we gaan de laser laten schieten
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):  # we gaan de breedte van het schip returnen
        return self.ship_img.get_width()

    def get_height(self):  # we gaan de hoogte van het schip returnen
        return self.ship_img.get_height()

# we gaan de player class aanmaken zodat we de player kunnen aanroepen in het spel en de functies van de ship class kunnen gebruiken


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        # we gaan de mask van het schip aanmaken zodat we de collision kunnen regelen met de laser en het schip
        self.mask = pygame.mask.from_surface(self.ship_img)
        # we gaan de max health van het schip aanmaken zodat we de healthbar kunnen tekenen in het spel
        self.max_health = health

    def move_lasers(self, vel, objs):  # we gaan de lasers laten bewegen en kijken of ze van het scherm zijn en of ze een object raken en verwijderen ze als ze van het scherm zijn of als ze een object raken
        self.cooldown()  # we gaan de cooldown functie aanroepen
        for laser in self.lasers:  # we gaan de lasers laten bewegen en kijken of ze van het scherm zijn en of ze een object raken en verwijderen ze als ze van het scherm zijn of als ze een object raken
            laser.move(vel)

            # als de laser van het scherm is dan verwijderen we de laser
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:                       # als de laser niet van het scherm is dan kijken we of de laser een object raakt
                for obj in objs:
                    # als de laser een object raakt dan verwijderen we het object
                    if laser.collision(obj):

                        objs.remove(obj)
                        if laser in self.lasers:  # als de laser een object raakt dan verwijderen we de laser
                            self.lasers.remove(laser)

    def draw(self, window):  # we gaan het schip tekenen
        # we gaan de draw functie van de ship class aanroepen om het schip te tekenen
        super().draw(window)

        self.healthbar(window)  # we gaan de healthbar tekenen in het spel

    def healthbar(self, window):  # we gaan de healthbar tekenen in het spel
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() -
                         20, self.ship_img.get_width(), 10))  # we gaan de gele healthbar tekenen in het spel
        pygame.draw.rect(window, (255, 255, 0), (self.x, self.y + self.ship_img.get_height() - 20, self.ship_img.get_width()
                         * (self.health/self.max_health), 10))  # we gaan de groene healthbar tekenen in het spel als


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):  # we gaan de laser tekenen
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):  # we gaan de laser laten bewegen door de y as
        self.y += vel

    def off_screen(self, height):  # we gaan kijken of de laser van het scherm is
        # als de laser niet meer op het scherm is dan returnen we True om de laser te verwijderen
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):  # we gaan kijken of de laser een object raakt
        # we gaan de collide functie aanroepen en kijken of de laser en het object elkaar raken
        return collide(self, obj)


class Enemy(Ship):  # we gaan de enemy class aanmaken zodat we de enemy kunnen aanroepen in het spel en de functies van de ship class kunnen gebruiken

    # we gaan de kleuren van de enemy aanmaken zodat we de enemy kunnen aanmaken in verschillende kleuren
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
        "ufo": (UFO_SPACE_SHIP, RED_LASER)
    }

    # we gaan de init functie aanmaken zodat we de enemy kunnen aanmaken in het spel
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        # we gaan de kleur van de enemy aanmaken zodat we de enemy kunnen aanmaken in verschillende kleuren
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        # we gaan de mask van het schip aanmaken zodat we de collision kunnen regelen met de laser en het schip
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):  # we gaan de enemy laten bewegen
        self.y += vel  # we gaan de y positie van de enemy veranderen zodat de enemy naar beneden beweegt

    def shoot(self):  # we gaan de laser laten schieten
        if self.cool_down_counter == 0:  # als de cooldown counter 0 is dan zetten we de cooldown counter op 1
            # we gaan de laser beam centreren op het schip
            laser = Laser(self.x-20, self.y, self.laser_img)
            # we gaan de laser toevoegen aan de lasers lijst zodat we de laser kunnen tekenen in het spel
            self.lasers.append(laser)
            # we gaan de cooldown counter op 1 zetten zodat de laser niet te snel kan schieten
            self.cool_down_counter = 1


def collide(obj1, obj2):  # we gaan kijken of de laser en het schip elkaar raken
    # we gaan de offset van de x positie van de laser en het schip berekenen zodat we de collision kunnen regelen
    offset_x = obj2.x - obj1.x
    # we gaan de offset van de y positie van de laser en het schip berekenen zodat we de collision kunnen regelen
    offset_y = obj2.y - obj1.y
    # we gaan kijken of de laser en het schip elkaar raken en als ze elkaar raken dan returnen we True en als ze elkaar niet raken dan returnen we False
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():      # we gaan de main functie aanmaken zodat we het spel kunnen aanroepen
    run = True   # we gaan de run variabele aanmaken zodat we het spel kunnen aanroepen
    FPS = 60     # we gaan de fps aanmaken zodat we de snelheid van het spel kunnen aanpassen
    level = 0    # we gaan de level aanmaken zodat we de level kunnen aanpassen in het spel
    lives = 5   # we gaan de lives aanmaken zodat we de lives kunnen aanpassen in het spel
    # we gaan de font aanmaken zodat we de tekst kunnen aanpassen in het spel
    main_font = pygame.font.SysFont("Arial", 50)
    # we gaan de font aanmaken zodat we de tekst kunnen aanpassen in het spel
    lost_font = pygame.font.SysFont("Arial", 60)

    enemies = []     # we gaan de enemies lijst aanmaken zodat we de enemies kunnen aanmaken in het spel
    # we gaan de wave length aanmaken zodat we de enemies kunnen aanmaken in het spel
    wave_length = 5
    enemy_vel = 1.5    # we gaan de enemy velocity aanmaken zodat we de snelheid van de enemies kunnen aanpassen in het spel

    player_vel = 5   # we gaan de player velocity aanmaken zodat we de snelheid van het schip kunnen aanpassen in het spel
    laser_vel = 10    # we gaan de laser velocity aanmaken zodat we de snelheid van de laser kunnen aanpassen in het spel

    # we gaan het schip aanmaken zodat we het schip kunnen aanroepen in het spel
    player = Player(300, 630)
    player_2 = Player(300, 630)
    # we gaan de clock aanmaken zodat we de snelheid van het spel kunnen aanpassen
    clock = pygame.time.Clock()

    lost = False    # we gaan de lost variabele aanmaken zodat we de tekst kunnen aanpassen in het spel
    lost_count = 0  # we gaan de lost count aanmaken zodat we de tekst kunnen aanpassen in het spel

    def redraw_window():    # we gaan de redraw window functie aanmaken zodat we de tekst en de schepen kunnen tekenen in het spel
        WIN.blit(BG, (0, 0))  # we gaan de achtergrond tekenen in het spel
        # we gaan de tekst tekenen in het spel
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        # we gaan de lives label tekenen in het spel
        WIN.blit(lives_label, (10, 10))
        # we gaan de level label tekenen in het spel
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)  # we gaan de enemies tekenen in het spel

        player.draw(WIN)  # we gaan de spelers tekenen in het spel
        player_2.draw(WIN) # we gaan de 2de speler tekenen in het spel

        if lost:  # als de speler verloren heeft dan gaan we de tekst tekenen in het spel
            lost_label = lost_font.render(
                "JE HEBT VERLOREN", 1, (255, 255, 255))
            # we gaan de lost label tekenen in het midden v/t spel
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        # we gaan de display updaten zodat we de tekst en de schepen kunnen tekenen in het spel
        pygame.display.update()

    # we gaan de main loop aanmaken zodat we het spel kunnen aanroepen
    while run:
        clock.tick(FPS)  # we gaan de snelheid van het spel aanpassen
        redraw_window()  # we gaan de redraw window functie aanroepen zodat we de tekst en de schepen kunnen tekenen in het spel

        if lives <= 0 or player.health <= 0:  # als de lives of de health van het schip 0 is dan gaan we de lost variabele op True zetten
            lost = True
            # we gaan de lost count op 1 zetten zodat we de tekst kunnen aanpassen in het spel
            lost_count += 1

        if lost:  # als de speler verloren heeft dan gaan we de tekst tekenen in het spel
            if lost_count > FPS * 3:  # als de lost count groter is dan 3 seconden dan gaan we de run variabele op False zetten zodat we het spel kunnen afsluiten
                run = False
            else:
                continue

        if len(enemies) == 0:  # als de enemies 0 zijn dan gaan we de level op 1 zetten en de wave length op 5 zetten zodat we de enemies kunnen aanmaken in het spel
            level += 1  # we gaan de level met 1 verhogen
            wave_length += 5  # we gaan de wave length met 5 verhogen
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(
                    ["ufo", "blue",  "red", "green"]))  # we gaan de enemies aanmaken in het spel
                # we gaan de enemies toevoegen aan de enemies lijst
                enemies.append(enemy)

        for event in pygame.event.get():  # we gaan de events aanmaken zodat we het spel kunnen afsluiten
            if event.type == pygame.QUIT:  # als we op het kruisje klikken dan gaan we de run variabele op False zetten zodat we het spel kunnen afsluiten
                quit()
        # we gaan de keys aanmaken zodat we het schip kunnen besturen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:  # pijltje naar links
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:  # pijltje naar rechts
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:  # pijltje naar boven
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # pijltje naar beneden
            player.y += player_vel
        if keys[pygame.K_SPACE]:  # schietknop spatiebalk
            player.shoot()
            player_laser_sound.play()  # We laten het schietgeluid afspelen nadat er werd geschoten

        if keys[pygame.K_a] and player_2.x - player_vel > 0:  # pijltje naar links
            player_2.x -= player_vel
        if keys[pygame.K_d] and player_2.x + player_vel + player_2.get_width() < WIDTH:  # pijltje naar rechts
            player_2.x += player_vel
        if keys[pygame.K_w] and player_2.y - player_vel > 0:  # pijltje naar boven
            player_2.y -= player_vel
        if keys[pygame.K_s] and player_2.y + player_vel + player_2.get_height() + 15 < HEIGHT:  # pijltje naar beneden
            player_2.y += player_vel
        if keys[pygame.K_LSHIFT]:  # schietknop spatiebalk
            player_2.shoot()
            player_laser_sound.play()  # We laten het schietgeluid afspelen nadat er werd geschoten

        for enemy in enemies[:]:  # we gaan de enemies aanmaken in het spel
            # we gaan de enemy velocity aanmaken zodat we de snelheid van de enemies kunnen aanpassen in het spel
            enemy.move(enemy_vel)
            # we gaan de enemy lasers aanmaken zodat we de lasers van de enemies kunnen aanpassen in het spel
            enemy.move_lasers(laser_vel, player)
            enemy.move_lasers(laser_vel, player_2)
            # we gaan de enemy laser sound afspelen zodat we een geluid horen als de enemy schiet
            # we gaan de random.randrange gebruiken zo dat de enemies 50% kans hebben om te schieten
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
                # We laten het schietgeluid van de vijanden afspelen na dat ze hebben geschoten
                enemy_laser_sound.play()

            if collide(enemy, player):  # als de enemy en de player elkaar raken dan gaan we de health van de player met 10 verminderen en de enemy verwijderen uit de enemies lijst
                collision_sound.play()
                player.health -= 10
                enemies.remove(enemy)

            if collide(enemy, player_2):  # als de enemy en de player elkaar raken dan gaan we de health van de player met 10 verminderen en de enemy verwijderen uit de enemies lijst
                collision_sound.play()
                player_2.health -= 10
                enemies.remove(enemy)
            # als de enemy onderaan het scherm is dan gaan we de lives met 1 verminderen en de enemy verwijderen uit de enemies lijst
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1  # we gaan de lives met 1 verminderen
                # we gaan de enemy verwijderen uit de enemies lijst
                enemies.remove(enemy)

        # we gaan de player lasers aanmaken zodat we de lasers van de player kunnen aanpassen in het spel
        player.move_lasers(-laser_vel, enemies)
        player_2.move_lasers(-laser_vel, enemies)
        # we gaan de player laser sound afspelen zodat we een geluid horen als de player schiet


def menu():
    # we gaan de titel font aanmaken zodat we de titel kunnen aanpassen in het spel
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:  # we gaan de main menu loop aanmaken zodat we het spel kunnen aanroepen
           
        WIN.blit(BG, (0, 0))  # we gaan de achtergrond tekenen in het spel
        # we gaan de titel label aanmaken zodat we de titel kunnen aanpassen in het spel
        title_label = title_font.render(
            "Click om te starten", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        # we gaan de display updaten zodat we de tekst en de schepen kunnen tekenen in het spel
        pygame.display.update()
            
        for event in pygame.event.get():    # we gaan de events aanmaken zodat we het spel kunnen afsluiten
            
            if event.type == pygame.QUIT:  # als we op het kruisje klikken dan gaan we de run variabele op False zetten zodat we het spel kunnen afsluiten
                run = False

            # als we op de muis klikken dan gaan we de main functie aanroepen zodat we het spel kunnen aanroepen
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_sound.play() 
                main()
                
                
    pygame.quit()


menu()
