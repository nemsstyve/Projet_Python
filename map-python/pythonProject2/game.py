import pygame
import pytmx
import pyscroll

from player import Player


class Game:
    def __init__(self):  # se lance des le debut, cree la page, charger la carte, #generer le perso, dessiner les calque

        self.map = 'village'
        self.screen = pygame.display.set_mode((1600, 900))
        pygame.display.set_caption("ton ptn de daron")

        tmx_data = pytmx.util_pygame.load_pygame('map-village.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        self.walls = []  # pour les collisions

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

        #  changement de zone
        chemin_gauche = tmx_data.get_object_by_name('chemin_gauche')
        self.chemin_gauche_rect = pygame.Rect(chemin_gauche.x, chemin_gauche.y, chemin_gauche.width,
                                              chemin_gauche.height)

    def handle_input(self):  # deplacement

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
            print("haut")
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
            print("bas")
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
            print("gauche")
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')
            print("droite")

    def switch_house(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("ton ptn de daron")

        tmx_data = pytmx.util_pygame.load_pygame('chemin-gauche.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        self.walls = []  # pour les collisions

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

        #  changement de zone
        chemin_gauche = tmx_data.get_object_by_name('sortie-village-gauche')
        self.chemin_gauche_rect = pygame.Rect(chemin_gauche.x, chemin_gauche.y, chemin_gauche.width,
                                              chemin_gauche.height)

        #  point de spawn
        spawn_chemin_gauche = tmx_data.get_object_by_name('spawn-village-gauche')
        self.player.position[0] = spawn_chemin_gauche.x - 15
        self.player.position[1] = spawn_chemin_gauche.y - 20

    def switch_world(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("ton ptn de daron")

        tmx_data = pytmx.util_pygame.load_pygame('map-village.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        self.walls = []  # pour les collisions

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

        #  changement de zone
        chemin_gauche = tmx_data.get_object_by_name('sortie-village-gauche')
        self.chemin_gauche_rect = pygame.Rect(chemin_gauche.x, chemin_gauche.y, chemin_gauche.width,
                                              chemin_gauche.height)

        spawn_chemin_gauche = tmx_data.get_object_by_name('sortie-chemin-gauche')
        self.player.position[0] = spawn_chemin_gauche.x + 150
        self.player.position[1] = spawn_chemin_gauche.y

    def update(self):
        self.group.update()

        #  verif entrer dans la maison
        if self.map == 'village' and self.player.feet.colliderect(self.chemin_gauche_rect):
            self.switch_house()
            self.map = 'chemin-gauche'

        if self.map == 'chemin-gauche' and self.player.feet.colliderect(self.chemin_gauche_rect):
            self.switch_world()
            self.map = 'village'
            print("tamere")

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):  # = fps/ allumer / quit

        clock = pygame.time.Clock()

        running = True

        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)
        pygame.quit()
