import random
import datetime
import pygame
from suntime import Sun


class Kropka:
    def __init__(self):
        self.x = random.randint(0, szer)
        self.y = random.randint(0, wys)
        self.r = random.choice((5, 5, 5, 5, 10, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55))
        self.lx = random.random()
        self.ly = random.random()
        if pozTrud == 2:
            self.lx, self.ly = nowy_kierunek()
            self.lx *= 2
            self.ly *= 2
        self.kolor = rkol()

    def rysuj(self):
        if trybNocny == 0 or trybNocny == 2 and czyDzien_zmienna:
            rn = 0
        else:
            rn = 1
        pygame.draw.circle(screen, self.kolor, (self.x, self.y), self.r, rn * 3)
        if self.x < self.r:
            pygame.draw.circle(screen, self.kolor, (szer + self.x, self.y), self.r, rn * 3)
        if self.x > szer - self.r:
            pygame.draw.circle(screen, self.kolor, (self.x - szer, self.y), self.r, rn * 3)
        if self.y < self.r:
            pygame.draw.circle(screen, self.kolor, (self.x, wys + self.y), self.r, rn * 3)
        if self.y > wys - self.r:
            pygame.draw.circle(screen, self.kolor, (self.x, self.y - wys), self.r, rn * 3)

    def ruch(self, zx, zy):

        self.x += zx + self.lx
        self.y += zy + self.ly
        if self.x > szer:
            self.x -= szer
        if self.y > wys:
            self.y -= wys
        if self.x < 0:
            self.x += szer
        if self.y < 0:
            self.y += wys


class Player(Kropka):
    def __init__(self):
        self.x = szer / 2
        self.y = wys / 2
        self.r = 20
        self.kolor = (255, 0, 0)

    def ruch(self, zx, zy):
        global czyZyje
        for event in pygame.event.get():
            if e.type == CZYJUZDZIEN:
                global czyDzien_zmienna
                czyDzien_zmienna = czyDzien()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    instrukcja()
                if event.key == pygame.K_u:
                    ustawienia()
                    if not czyZyje:
                        for k in kropki:
                            k.kolor = rbw()
                if event.key in (pygame.K_UP, pygame.K_w, pygame.K_8):
                    zy = -3
                if event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_5):
                    zy = 3
                if event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_6):
                    zx = 3
                if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_4):
                    zx = -3
                if event.key == pygame.K_ESCAPE:
                    quit()
                if event.key == pygame.K_p:
                    pygame.mixer.music.pause()
                    if czyZyje:
                        pauza()
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.unpause()
                    if not czyZyje:
                        self.r = 20
                        for k in kropki:
                            k.r = random.choice((5, 5, 5, 5, 10, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55))
                    else:
                        self.r = min(20, self.r)
                    global punkt
                    punkt = 1
                    for k in kropki:
                        k.kolor = rkol()
                    self.kolor = (255, 0, 0)
                    czyZyje = True
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_w, pygame.K_8, pygame.K_DOWN, pygame.K_s, pygame.K_5):
                    zy = 0
                if event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_6, pygame.K_LEFT, pygame.K_a, pygame.K_4):
                    zx = 0
            elif event.type == pygame.QUIT:
                quit()
            elif event.type == ZMIANAKIERUNKU:
                global kierKropek
                if pozTrud != 0:
                    kierKropek = nowy_kierunek()
            elif event.type == GLOD:
                if czyZyje:
                    self.r -= 1
        self.x += zx
        self.y += zy
        if self.x > szer:
            self.x -= szer
        if self.y > wys:
            self.y -= wys
        if self.x < 0:
            self.x += szer
        if self.y < 0:
            self.y += wys

        return [zx, zy]

    def kolizja(self, kropka):
        if (kropka.x - self.x) ** 2 + (kropka.y - self.y) ** 2 <= (self.r + kropka.r) ** 2:
            return True
        else:
            return False


def kolor_tla():
    if trybNocny == 0 or trybNocny == 2 and czyDzien_zmienna:
        return 255, 255, 255
    else:
        return 0, 0, 0


def kolor_kontrast():
    if trybNocny == 0 or trybNocny == 2 and czyDzien_zmienna:
        return 0, 0, 0
    else:
        return 255, 255, 255


def czyDzien():
    s = Sun(52.21, 21.00)
    wschod_slonca = s.get_local_sunrise_time()
    zachod_slonca = s.get_local_sunset_time()
    teraz = datetime.datetime.now(tz=wschod_slonca.tzinfo)
    return wschod_slonca < teraz < zachod_slonca


def rkol():
    return random.randint(0, 240), random.randint(0, 240), random.randint(0, 240)


def rbw():
    t = random.randint(0, 200)
    return t, t, t


def rkod(T):
    wyn = []
    for i in T:
        i += random.randint(-40, 40)
        i = min(255, i)
        i = max(0, i)
        wyn.append(i)
    return tuple(wyn)


def rkod_slow(T):
    wyn = []
    for i in T:
        i += random.randint(-10, 10)
        i = min(255, i)
        i = max(0, i)
        wyn.append(i)
    return tuple(wyn)


def napisz(tekst, y, rozmiar=12, przes=0):
    cz = pygame.font.SysFont("Arial", rozmiar)
    if trybNocny == 0 or trybNocny == 2 and czyDzien_zmienna:
        rend = cz.render(tekst, True, (0, 0, 0))
    else:
        rend = cz.render(tekst, True, (255, 255, 255))

    screen.blit(rend, ((szer - rend.get_width()) / 2 + przes, y))


def napisz_dluzszy(tekst, rozmiar=12):
    L = tekst.split('\n')
    yp = (wys - len(L) * rozmiar * 1.5) / 2
    for i in range(len(L)):
        napisz(L[i], yp + i * 1.5 * rozmiar, rozmiar)


def nowy_kierunek():
    temp = random.random()
    if pozTrud == 2:
        temp *= 3 ** (1 / 2)
    temp2 = 3 - (temp * temp)
    temp2 = temp2 ** 1 / 2
    temp *= random.choice((-1, 1))
    temp2 *= random.choice((-1, 1))
    return [temp, temp2]


def pauza():
    temp = rkol()
    for k in kropki:
        k.kolor = (rkod(temp))
    gracz.kolor = (rkod(temp))
    b = True
    while b:
        # if un==0 or un==2 and czyDzien():

        screen.fill(kolor_tla())
        for k in kropki:
            k.rysuj()
        gracz.rysuj()
        napisz("Punkty: " + str(punkty), 50, 20, -500)
        napisz("To jest pauza ^-^", wys / 2 - 100, 40)
        napisz("Kliknij spację aby wrócić do gry", wys / 2 - 15, 40)
        napisz("Kliknij 'u' by przejść do ustawień", wys / 2 + 180, 30)
        napisz("Kliknij 'i' by zobaczyć instrukcję", wys / 2 + 240, 25)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == CZYJUZDZIEN:
                global czyDzien_zmienna
                czyDzien_zmienna = czyDzien()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_SPACE, pygame.K_p):
                    pygame.mixer.music.unpause()
                    b = False
                if e.key == pygame.K_u:
                    ustawienia()
                if e.key == pygame.K_i:
                    instrukcja()
            if e.type == pygame.QUIT:
                quit()
    for k in kropki:
        k.kolor = rkol()
    gracz.kolor = (255, 0, 0)


def instrukcja():
    while True:
        screen.fill(kolor_tla())
        for k in kropki:
            k.rysuj()
        gracz.rysuj()
        s = pygame.Surface((680, 620))
        s.set_alpha(120)
        s.fill((200, 200, 200))
        screen.blit(s, (szer / 2 - 340, wys / 2 - 360))
        pygame.draw.rect(screen, kolor_kontrast(), pygame.Rect(szer / 2 - 340, wys / 2 - 360, 680, 620), 3)
        tekst = """Instrukcja:
Witaj w grze w kropki! Twoje zadanie będzie 
polegać na zebraniu jak największej ilości 
punktów nie dając się przy tym pożreć ani nie 
przejadając się za bardzo. Punkty zdobywasz 
zjadając mniejsze kropki od siebie tym samym
zwiększając swój rozmiar. Sterujesz używając 
strzałek albo klawiszy 'wasd', aby zmniejszyć 
rozmiar do początkowego kliknij spację, aby 
zapauzować grę kliknij 'p', żeby wejść w usta-
wienia użyj 'u'. W ustawiniach możeszzmienić 
prędkość gry jak i włączyć tryb nocny ^^
Powodzenia :D

Kliknij 'i' aby wrócić"""
        napisz_dluzszy(tekst, 30)
        pygame.display.update()

        for event in pygame.event.get():
            if e.type == CZYJUZDZIEN:
                global czyDzien_zmienna
                czyDzien_zmienna = czyDzien()
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                elif event.key == pygame.K_i:
                    return
                elif event.key == pygame.K_u:
                    ustawienia()


def ustawienia():
    b2 = True
    w = 1
    global pozTrud
    pt = pozTrud
    global trybNocny
    while b2:
        screen.fill(kolor_tla())
        for k in kropki:
            k.rysuj()
        gracz.rysuj()
        s = pygame.Surface((400, 120))
        s.set_alpha(120)
        s.fill((200, 200, 200))
        screen.blit(s, (szer / 2 - 200, wys / 2 - 262))
        s = pygame.Surface((400, 120))
        s.set_alpha(120)
        s.fill((200, 200, 200))
        screen.blit(s, (szer / 2 - 200, wys / 2 - 102))
        if w == 1:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(szer / 2 - 200, wys / 2 - 262, 400, 120), 3)
            pygame.draw.rect(screen, kolor_kontrast(), pygame.Rect(szer / 2 - 200, wys / 2 - 102, 400, 120), 3)
        else:
            pygame.draw.rect(screen, kolor_kontrast(), pygame.Rect(szer / 2 - 200, wys / 2 - 262, 400, 120), 3)
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(szer / 2 - 200, wys / 2 - 102, 400, 120), 3)
        napisz("Poziom trudności:", wys / 2 - 235, 25)
        napisz("    łatwy,     średni,     trudny", wys / 2 - 195, 25)
        napisz("Tryb nocny:", wys / 2 - 75, 25)
        napisz("    nie,     tak,     auto", wys / 2 - 35, 25)
        napisz("Kliknij 'u' aby wyjść z ustawień ^^", wys / 2 + 100, 25)
        if pozTrud == 0:
            pygame.draw.circle(screen, (255, 0, 0), (szer / 2 - 142, wys / 2 - 180), 10, 0)
        if pozTrud == 1:
            pygame.draw.circle(screen, (255, 0, 0), (szer / 2 - 42, wys / 2 - 180), 10, 0)
        if pozTrud == 2:
            pygame.draw.circle(screen, (255, 0, 0), (szer / 2 + 70, wys / 2 - 180), 10, 0)
        if trybNocny == 0:
            pygame.draw.circle(screen, (255, 0, 0), (szer / 2 - 103, wys / 2 - 20), 10, 0)
        if trybNocny == 1:
            pygame.draw.circle(screen, (255, 0, 0), (szer / 2 - 25, wys / 2 - 20), 10, 0)
        if trybNocny == 2:
            # TUTAJ AUTO ZGADUJĘ xd
            pygame.draw.circle(screen, (255, 0, 0), (szer / 2 + 52, wys / 2 - 20), 10, 0)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == CZYJUZDZIEN:
                global czyDzien_zmienna
                czyDzien_zmienna = czyDzien()
            if e.type == pygame.QUIT:
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    quit()
                if e.key in (pygame.K_UP, pygame.K_DOWN):
                    w = (w + 1) % 2
                if e.key == pygame.K_RIGHT:
                    if w == 1:
                        pozTrud = (pozTrud + 1) % 3
                    else:
                        trybNocny = (trybNocny + 1) % 3
                if e.key == pygame.K_LEFT:
                    if w == 1:
                        pozTrud = (pozTrud - 1) % 3
                    else:
                        trybNocny = (trybNocny - 1) % 3
                if e.key == pygame.K_u:
                    if pt != pozTrud:
                        kropki.clear()
                        for i in range(0, 20):
                            kropki.append(Kropka())
                        global kierKropek
                        kierKropek = (0, 0)
                        global punkty
                        punkty = 0
                    return


pygame.init()
szer = 1200
wys = 750
screen = pygame.display.set_mode((szer, wys))
pygame.display.set_caption("Kropki the Game")

pygame.mixer.music.load("Intro.mp3")
pygame.mixer.music.play()

czyZyje = True
kierKropek = [0, 0]
punkt = 1
highScore = 0
pozTrud = 1  # 0-łatwy, 1-średni ,2-trudny
trybNocny = 2  # 0-dzienny, 1-nocny, 2-automatyczny
ruchGracza = [0, 0]

punkty = 0
gracz = Player()
kropki = []
for i in range(20):
    k = Kropka()
    while szer / 2 - 50 < k.x < szer / 2 + 50 and wys / 2 - 50 < k.y < wys / 2 + 50:
        k = Kropka()
    kropki.append(k)

clock = pygame.time.Clock()

ZMIANAKIERUNKU = pygame.USEREVENT + 1
pygame.time.set_timer(ZMIANAKIERUNKU, 3000)
GLOD = pygame.USEREVENT + 2
pygame.time.set_timer(GLOD, 1000)
CZYJUZDZIEN = pygame.USEREVENT + 3
pygame.time.set_timer(CZYJUZDZIEN, 60000)

czyDzien_zmienna = czyDzien()

b1 = True
while b1:
    screen.fill(kolor_tla())
    for k in kropki:
        k.rysuj()
    gracz.rysuj()
    napisz("Kliknij spację aby zacząć grę ^^", wys / 2 + 100, 40)
    napisz("Kliknij 'u' by przejść do ustawień", wys / 2 + 180, 30)
    napisz("Kliknij 'i' by zobaczyć instrukcję", wys / 2 + 240, 25)
    s = pygame.Surface((800, 200))
    s.set_alpha(120)
    s.fill((200, 200, 200))
    screen.blit(s, (szer / 2 - 400, wys / 2 - 190))
    pygame.draw.rect(screen, kolor_kontrast(), pygame.Rect(szer / 2 - 400, wys / 2 - 190, 800, 200), 3)
    # Tytul()
    napisz("Gra w kropki", wys / 2 - 150, 120)
    napisz("by Alex Michalec", wys - 50, 20, 450)
    pygame.display.update()

    for e in pygame.event.get():
        if e.type == CZYJUZDZIEN:
            czyDzien_zmienna = czyDzien()
        if e.type == pygame.QUIT:
            quit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                b1 = False
            elif e.key == pygame.K_ESCAPE:
                quit()
            elif e.key == pygame.K_u:
                ustawienia()
            elif e.key == pygame.K_i:
                instrukcja()

pygame.mixer.music.stop()
pygame.mixer.music.unload()
pygame.mixer.music.load("Positive.mp3")
pygame.mixer.music.play(loops=-1)

while True:
    screen.fill(kolor_tla())
    ruchGracza = gracz.ruch(*ruchGracza)
    for k in kropki:
        k.ruch(*kierKropek)

    for k in kropki:
        if czyZyje and gracz.kolizja(k):
            if k.r < gracz.r:
                punkty += punkt
                gracz.r += 5
                temp = k.r
                kropki.remove(k)
                kropki.append(Kropka())
                kropki[-1].r = temp
            elif k.r > gracz.r:
                TP = punkty
                punkty = 0
                gracz.r = 20
                gracz.kolor = (240, 240, 240)
                for k in kropki:
                    k.kolor = rbw()
                czyZyje = False

    gracz.rysuj()
    for k in kropki:
        k.rysuj()
    if gracz.r > 600 or not czyZyje:
        pygame.mixer.music.pause()
        punkt = 0
        punkty = 0
        if TP > highScore:
            highScore = TP
        napisz("Your score: " + str(TP), 160, 20)
        napisz("High score: " + str(highScore), 200, 18)
        if czyZyje:
            napisz("Za bardzo się obżarłeś ^^", wys / 2 - 100, 40)
        napisz("Kliknij spację by zacząć jeszcze raz", wys / 2 - 15, 40)
        napisz("Kliknij 'u' by przejść do ustawień", wys / 2 + 180, 30)
        napisz("Kliknij 'i' by zobaczyć instrukcję", wys / 2 + 240, 25)
    else:
        napisz("Punkty: " + str(punkty), 50, 20, -500)
        TP = punkty
    if not czyZyje:
        napisz("Przegrałeś, ktoś cię zjadł :c", wys / 2 - 100, 40)

    pygame.display.update()
    clock.tick(180)

"""
MUSIC:

Staying Positive by spinningmerkaba (c) copyright 2019 
Licensed under a Creative Commons Attribution Noncommercial  (3.0) license.
http://dig.ccmixter.org/files/jlbrock44/59438 Ft: greg_baumont

and

B Calm Violin Track by Dimitri Artemenko (c) copyright 2007 
Licensed under a Creative Commons Attribution license. 
http://dig.ccmixter.org/files/stringfactory/8751 
"""
