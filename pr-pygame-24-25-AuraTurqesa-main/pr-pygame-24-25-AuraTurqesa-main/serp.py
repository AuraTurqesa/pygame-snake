import pygame
import random
import time
import sys

# Mida del marc
amplada_marc = 720
altura_marc = 480

# Comprovació d'errors durant la inicialització
comprovacio_errors = pygame.init()
if comprovacio_errors[1] > 0:
    print(f'[!] Hi ha hagut {comprovacio_errors[1]} errors en inicialitzar el joc, sortint...')
    sys.exit(-1)
else:
    print('[+] Joc inicialitzat correctament')

# Inicialitzar la finestra del joc
pygame.display.set_caption('Menja Serps')
finestra_joc = pygame.display.set_mode((amplada_marc, altura_marc))

# Colors (R, G, B)
negre = pygame.Color(0, 0, 0)
blanc = pygame.Color(255, 255, 255)
vermell = pygame.Color(255, 0, 0)
verd = pygame.Color(0, 255, 0)

# Control de FPS
control_fps = pygame.time.Clock()
fps = 10  # Velocitat inicial del joc

# Variables del joc
posicio_serp = [100, 50]
cos_serp = [[100, 50], [90, 50], [80, 50]]

posicio_menjar = [
    random.randrange(1, (amplada_marc // 10)) * 10,
    random.randrange(1, (altura_marc // 10)) * 10
]
menjar_generat = True

direccio = 'DRETA'
canviar_a = direccio

puntuacio = 0

# Funció de fi del joc
def fi_del_joc():
    font = pygame.font.SysFont('times new roman', 90)
    missatge = font.render('HAS MORT', True, vermell)
    rect_missatge = missatge.get_rect()
    rect_missatge.midtop = (amplada_marc / 2, altura_marc / 4)
    finestra_joc.fill(negre)
    finestra_joc.blit(missatge, rect_missatge)
    mostrar_puntuacio(0, vermell, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Funció per mostrar la puntuació
def mostrar_puntuacio(opcio, color, font, mida):
    font_puntuacio = pygame.font.SysFont(font, mida)
    text_puntuacio = font_puntuacio.render('Puntuació: ' + str(puntuacio), True, color)
    rect_puntuacio = text_puntuacio.get_rect()
    if opcio == 1:
        rect_puntuacio.midtop = (amplada_marc / 10, 15)
    else:
        rect_puntuacio.midtop = (amplada_marc / 2, altura_marc / 1.25)
    finestra_joc.blit(text_puntuacio, rect_puntuacio)

# Lògica principal
while True:
    for esdeveniment in pygame.event.get():
        if esdeveniment.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif esdeveniment.type == pygame.KEYDOWN:
            if esdeveniment.key == pygame.K_UP or esdeveniment.key == ord('w'):
                canviar_a = 'AMUNT'
            if esdeveniment.key == pygame.K_DOWN or esdeveniment.key == ord('s'):
                canviar_a = 'AVALL'
            if esdeveniment.key == pygame.K_LEFT or esdeveniment.key == ord('a'):
                canviar_a = 'ESQUERRA'
            if esdeveniment.key == pygame.K_RIGHT or esdeveniment.key == ord('d'):
                canviar_a = 'DRETA'
            if esdeveniment.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Evitar que la serp es mogui en direcció oposada immediatament
    if canviar_a == 'AMUNT' and direccio != 'AVALL':
        direccio = 'AMUNT'
    if canviar_a == 'AVALL' and direccio != 'AMUNT':
        direccio = 'AVALL'
    if canviar_a == 'ESQUERRA' and direccio != 'DRETA':
        direccio = 'ESQUERRA'
    if canviar_a == 'DRETA' and direccio != 'ESQUERRA':
        direccio = 'DRETA'

    # Moviment de la serp
    if direccio == 'AMUNT':
        posicio_serp[1] -= 10
    if direccio == 'AVALL':
        posicio_serp[1] += 10
    if direccio == 'ESQUERRA':
        posicio_serp[0] -= 10
    if direccio == 'DRETA':
        posicio_serp[0] += 10

    # Mecanisme de creixement de la serp
    cos_serp.insert(0, list(posicio_serp))
    if posicio_serp == posicio_menjar:
        puntuacio += 1
        fps *= 1.05  # Augmenta la velocitat un 5%
        menjar_generat = False
    else:
        cos_serp.pop()

    # Generar menjar
    if not menjar_generat:
        posicio_menjar = [
            random.randrange(1, (amplada_marc // 10)) * 10,
            random.randrange(1, (altura_marc // 10)) * 10
        ]
    menjar_generat = True

    # Gràfics
    finestra_joc.fill(negre)
    for bloc in cos_serp:
        pygame.draw.rect(finestra_joc, verd, pygame.Rect(bloc[0], bloc[1], 10, 10))
    pygame.draw.rect(finestra_joc, blanc, pygame.Rect(posicio_menjar[0], posicio_menjar[1], 10, 10))

    # Condicions de fi del joc
    if posicio_serp[0] < 0 or posicio_serp[0] > amplada_marc - 10:
        fi_del_joc()
    if posicio_serp[1] < 0 or posicio_serp[1] > altura_marc - 10:
        fi_del_joc()
    for bloc in cos_serp[1:]:
        if posicio_serp == bloc:
            fi_del_joc()

    mostrar_puntuacio(1, blanc, 'consolas', 20)
    pygame.display.update()
    control_fps.tick(int(fps))  # Controla la velocitat amb l'FPS actualitzat
