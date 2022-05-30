import types
from unicodedata import name
from random import randint
import sys 

is_finished = False
Daniel = True
Styve = True
Coranthin = True
Bular = True
Dragon = True

class attack:
  def __init__(self,name,dmg,crit_chance,miss_chance, effect = None):
    self.name = name
    self.dmg = dmg
    self.crit_chance = crit_chance
    self.miss_chance = miss_chance
    self.effect = effect
  
  def calculate_damage(self):
    from random import randint
    R = randint(0,100)
    if R < self.crit_chance:
      return self.dmg * 2

    R = randint(0,100)
    if R < self.miss_chance:
      return 0
    
    return self.dmg

class attack_magic(attack):
  def __init__(self,name,dmg,crit_chance,miss_chance,mana_cost, effect = None):
    super().__init__(name,dmg,crit_chance,miss_chance, effect)
    self.mana_cost = mana_cost
  
  def calculate_damage(self,player):
    if player.mana >= self.mana_cost:
      player.mana -= self.mana_cost
      return super.calculate_damage()
    return 0

class status:
  def __init__(self,name,effect,duration):
    self.name = name
    self.effect = effect
    self.duration = duration
  
  def update_entity(self,entity):
    if self.effect == "Stun" and self.duration <= 0:
      entity.can_play = True
      return

    if self.effect == "Poison":
      entity.hp -= 1
    elif self.effect == "Regen":
      entity.hp += 1
    elif self.effect == "Stun":
      entity.can_play = False
    elif self.effect == "Berserk":
      entity.strength += 1
    self.duration -= 1

class Entity:
  def __init__(self,name,hp,strength,defense):
    self.name = name
    self.hp = hp
    self.mana = 100
    self.strength = strength
    self.defense = defense
    self.inventory = []
    self.attack_list = []
    self.equipped_weapon = None
    self.critical_chance = 1
    self.money = 0
    self.list_status = []
    self.can_play = True
    self.xp = 0
    self.is_dead = False

  def take_damage(self,amount):
    if amount > self.defense:
      amount -= self.defense
      self.hp -= amount 

  def equip(self, id_weapon):
    if self.equipped_weapon != None:
      self.desequip(self.equipped_weapon)

    self.equipped_weapon = self.inventory[id_weapon]
    self.strength += self.inventory[id_weapon].power

  def desequip(self, weapon):
    self.strength -= weapon.power

  def level_up(self):
    self.strength += 2
    self.defense += 2
    self.mana = 100
    self.hp = 100

# class Merchant(Entity):
#   def __init__(self,items,name,money):
#         if name == "Merchant" :
#             super().__init__(name,100,20,20)
#             self.money = money
#             self.inventory = items
#             self.inventory.append(Weapon("Epee",10,10))
#             self.inventory.append(Weapon("Arc",10,10))
#             self.inventory.append(Weapon("Baguette",10,10))
#             self.inventory.append(Weapon("Dague",10,10))
#         elif name == "Moving Merchant":
#             super().__init__(name,100,20,20)
#             self.money = money
#             self.inventory = items
#             self.inventory.append(Weapon("lance canon",10,10))
#             self.inventory.append(Weapon("DSR 50",10,10))
#             self.inventory.append(Weapon("Mjolnir",10,10))
#             self.inventory.append(Weapon("lame de Sept",10,10))
#         elif name == "Mom":
#             super().__init__(name,100,20,20)
#             self.money = money
#             self.inventory = items
#             self.inventory.append(Item("Potion de soin","heal",50,5))
  
#   def buy_item(self,player):
#     for i in range(len(self.inventory)):
#       print(i,"-",self.inventory[i].name,":",self.inventory[i].price)
#     print("choisissez un item")
#     choice = int(input())
#     Item = self.inventory[choice]
#     if player.money >= Item.price:
#       player.money -= Item.price
#       self.money += Item.price
#       player.inventory.append(Item)
#       self.inventory.remove(Item)
#     else:
#       print("Vous n'avez pas assez d'argent")

class Monster(Entity):
  def __init__(self,monster_type):
    if monster_type == "Bandit Guerrier":
            super().__init__(monster_type,30,7,5)
            self.inventory.append(Weapon("Epee en Fer",15,0,10))

    elif monster_type == "Bandit Sorcier":
            super().__init__(monster_type,25,5,10)
            self.inventory.append(Weapon("Balai Magique",15,0,10))

    elif monster_type == "Bandit Assassin":
            super().__init__(monster_type,20,10,5)
            self.inventory.append(Weapon("Dague en Fer",15,0,10))

    elif monster_type == "Bandit Archer":
            super().__init__(monster_type,30,5,5)
            self.inventory.append(Weapon("Arc de Chasse",15,0,10))

    elif monster_type == "Bular":
            super().__init__(monster_type,100,10,15)
            self.inventory.append(Weapon("Epee de Bular",40,0,50))

    if monster_type == "Troll":
            super().__init__(monster_type,30,5,5)
            self.inventory.append(Weapon("Epee en Fer",20,0,50))

    elif monster_type == "Fee":
            super().__init__(monster_type,10,6,30)
            self.inventory.append(Weapon("Balai Magique",20,0,50))

    elif monster_type == "Gobellin":
            super().__init__(monster_type,10,20,30)
            self.inventory.append(Weapon("Dague en Fer",20,0,50))

    elif monster_type == "Squelette":
            super().__init__(monster_type,10,20,30)
            self.inventory.append(Weapon("Arc de Chasse",20,0,50))

    elif monster_type == "Dragon":
            super().__init__(monster_type,100,20,30)
            self.inventory.append(Weapon("Hache Nordique",50,0,100))

    elif monster_type == "Cloud":
            super().__init__(monster_type,100,40,30)
            self.inventory.append(Weapon("Buster Sword",30,0,100))

    elif monster_type == "Esio":
            super().__init__(monster_type,100,20,30)
            self.inventory.append(Weapon("Lame Secrete",30,0,100))

    elif monster_type == "Hanzo":
            super().__init__(monster_type,100,20,30)
            self.inventory.append(Weapon("Arc Tempete",30,0,100))

    elif monster_type == "Morgana":
            super().__init__(monster_type,100,20,30)
            self.inventory.append(Weapon("Cape de Morgana",30,0,100))

    # elif monster_type == "Styve":
    #         super().__init__(monster_type,100,20,30)
    #         self.inventory.append(Weapon("Heragrim",50,0,500))

    # elif monster_type == "Daniel":
    #         super().__init__(monster_type,100,10,30)
    #         self.inventory.append(Weapon("Judgment Sword",40,0,5))

    # elif monster_type == "Coranthin":
    #         super().__init__(monster_type,100,20,30)
    #         self.inventory.append(Weapon("double ring",50,0,5))

    self.inventory.append(Item("Potion de soin","heal",10,5))
    self.inventory.append(Item("Potion de soin","heal",10,5))
    self.inventory.append(Item("Potion de soin","heal",10,5))
    self.equip(0)

  def Loot(self):
    from random import randint
    return self.inventory[randint(0,len(self.inventory)-1)]

class Player(Entity):
  def __init__(self,name,type_adventurer):
    self.type_adenturer = type_adventurer
    if type_adventurer == "Warrior":
            super().__init__(name,100,20,20)
            self.inventory.append(Weapon("Sword",10,10,1))

    elif type_adventurer == "Assassin":
            super().__init__(name,50,20,10)
            self.inventory.append(Weapon("Dagger",10,20,1))

    elif type_adventurer == "Wizard":
            super().__init__(name,100,20,20)
            self.inventory.append(Weapon("sweeps",10,5,1))

    elif type_adventurer == "Archer":
            super().__init__(name,60,20,20)
            self.inventory.append(Weapon("arc",10,7,1))
    self.equip(0)

  def open_inventory(self):
    for i in range(len(self.inventory)):
      print(i+1,":",self.inventory[i].name)
    print("Quel objet voulez vous utiliser ?")
    choice = int(input())
    item = self.inventory[choice-1]
    if type(item) == Weapon:
      self.equip(choice-1)
    elif type(item) == Item:
      item.use(self)
      self.inventory.pop(choice-1)

  def fight_inventory(self):
    for i in range(len(self.inventory)):
      print(i+1,":",self.inventory[i].name)
    print("Quel objet voulez vous utiliser ?")
    choice = int(input())
    item = self.inventory[choice-1]
    if type(item) == Weapon:
      self.equip(choice-1)
    elif type(item) == Item:
      item.use(self)
      self.inventory.pop(choice-1)


class Item:
  def __init__(self,name,effect,power,price):
    self.name = name
    self.effect = effect
    self.power = power
    self.price = price

  def use(self,target):
    if self.effect == "heal":
      target.hp += self.power
    elif self.effect == "Str":
      target.strength += self.power

class Weapon(Item):
  def __init__(self, name, strength_bonus, critical_chance, price):
    super().__init__(name,"Str",strength_bonus, price)
    self.critical_chance = critical_chance

  def use(self,target):
    super().use(target)
    target.critical_chance += self.critical_chance

def fight(hero, monster, place, zone, map):
    if monster.is_dead == True :
      print("Cet ennemi a deja ete vaincu")
    else :
      while hero.hp > 0 and monster.hp > 0 :
          print(hero.name, ":", hero.hp, "HP\t", monster.name, ":", monster.hp, "HP")
          print("Que voullez vous faire ?")
          print("1- Attack\n2- Mana\n3- Items")
          choise_player = int(input())
          while choise_player != 1 and choise_player != 2 and choise_player != 3 :
              print("Choix invalide")
              print("Que voullez vous faire ?")
              print("1- Attack\n2- Mana\n3- Items")
              choise_player = int(input())
          if choise_player == 3 :
              hero.fight_inventory()
          else :
              monster.take_damage(hero.strength)
          if monster.hp > 0 :
            hero.take_damage(monster.strength)
      if monster.hp < 1 :
        print(hero.name, ":", hero.hp, "HP\t", monster.name, ":", monster.hp, "HP")
        print(monster.name, "a ete vaincu")
        loot = monster.Loot()
        hero.inventory.append(loot)
        if monster.name == "Daniel" or monster.name == "Styve" or monster.name == "Coranthin" or monster.name == "Bular" or monster.name == "Dragon" :
          monster.is_dead = True
      elif hero.hp < 1 :
        print(hero.name, ":", hero.hp, "HP\t", monster.name, ":", monster.hp, "HP")
        print("Vous avez été vaincu")
        sys.exit()
    event(hero, place, zone, map)

def zone_change(zone) :
    count = 1
    for place in zone :
        print(count, "-", place)
        count += 1
    new_zone = int(input())
    while new_zone < 1 and new_zone > count-1 :
      print("Choix invalide")
      for place in zone :
        print(count, "-", place)
        count += 1
      new_zone = int(input())
    place = zone[new_zone-1]
    return place

def zone_ennemy(place) :
    if place == "Route" :
        ennemies = ["Bandit Guerrier", "Bandit Sorcier", "Bandit Assassin", "Bandit Archer"]
        number = randint(0,len(ennemies)-1)
        return ennemies[number]
    elif place == "Foret" :
        ennemies = ["Troll", "Fee", "Gobelin", "Squelette"]
        number = randint(0,len(ennemies)-1)
        return ennemies[number]
    elif place == "Grotte" :
      ennemies = ["Cloud", "Morgana", "Esio", "Hanzo"]
      number = randint(0,len(ennemies)-1)
      return ennemies[number]
    elif place == "Chateau" :
      if Dragon == True :
        return "Bular"
    elif place == "Foret Brulee" :
      if Dragon == True :
        return "Dragon"
    elif place == "Salle du Portail" :
      if Daniel == True :
        return "Daniel"
      elif Styve == True :
        return "Styve"
      elif Coranthin == True :
        return "Coranthin"

def event(Hero, place, zone, map) :
  while is_finished == False :
    if place == "Foret Brulee" or place == "Salle du portail" or place == "Chateau" :
        print("Un puissant ennemi est face a vous")
        print("Que voullez vous faire ?")
        print("1- Changer de zone\n2- Combattre\n3- Inventaire")
        choise = int(input())
        while choise < 1 and choise > 3 :
          print("Choix invalide")
          print("Que voullez vous faire ?")
          print("1- Changer de zone\n2- Combattre\n3- Inventaire")
          choise = int(input())
        if choise == 1 :
            place = zone_change(zone)
            zone = map[place]
            event(Hero, place, zone, map)
        elif choise == 2 :
            choise_ennemy = zone_ennemy(place)
            ennemy = Monster(choise_ennemy)
            if ennemy.is_dead == False :
              fight(Hero, ennemy, place, zone, map)
            else :
              print("Cet ennemi a deja ete vaincu")
        elif choise == 3 :
            Hero.fight_inventory()
    elif place == "Village" :
      print("Que voullez vous faire ?")
      print("1- Changer de zone\n2- Inventaire")
      choise = int(input())
      while choise < 1 and choise > 2 :
          print("Choix invalide")
          print("Que voullez vous faire ?")
          print("1- Changer de zone\n2- Inventaire")
          choise = int(input())
      if choise == 1 :
          place = zone_change(zone)
          zone = map[place]
          event(Hero, place, zone, map)
      elif choise == 2 :
          Hero.open_inventory()
    else :
        print("Que voullez vous faire ?")
        print("1- Changer de zone\n2- Fouller la zone\n3- Inventaire")
        choise = int(input())
        while choise < 1 and choise > 3 :
          print("Choix invalide")
          print("Que voullez vous faire ?")
          print("1- Changer de zone\n2- Fouller la zone\n3- Inventaire")
          choise = int(input())
        if choise == 1 :
            place = zone_change(zone)
            zone = map[place]
            event(Hero, place, zone, map)
        elif choise == 2 :
            choise_ennemy = zone_ennemy(place)
            ennemy = Monster(choise_ennemy)
            fight(Hero, ennemy, place, zone, map)
        elif choise == 3 :
            Hero.open_inventory()

def begin(zone, Map) :
  print("Bonjour, qui etes vous ?")
  print("1- Un Guerrier\n2- Un Mage\n3- Un Assassin\n4- Un Archer")
  choise_class = int(input())
  while choise_class < 1 and choise_class > 4 :
    print("Choix Invalide")
    print("Qui etes vous ?")
    print("1- Un Guerrier\n2- Un Mage\n3- Un Assassin\n4- Un Archer")
    choise_class = int(input())
  if choise_class == 1 :
    player_class = "Warrior"
  elif choise_class == 2 :
    player_class = "Wizard"
  elif choise_class == 3 :
    player_class = "Assassin"
  elif choise_class == 4 :
    player_class = "Archer"
  print("Et comment t'appelles-tu heros ?")
  player_name = input()
  Hero = Player(player_name, player_class)
  print("Ravi de te rencontrer", player_name, ", mais on a pas de temps a perdre, va sauver le Royaume")
  print("Voilà un petit quelque chose pour t'aider\n")
  print("Vous avez reçu", Hero.inventory[0].name)
  input("Appuiez sur entrer pour continuer")
  print("Essaie de l'equiper")
  input("Appuiez sur entrer pour ouvrir l'inventaire")
  Hero.fight_inventory()
  Hero.inventory.append(Item("Potion de soin","heal",50,5))
  print("Vous etes pres a partir\nBon voyage", Hero.name)
  input("Appuiez sur entrer pour continuer")
  place = "Village"
  event(Hero, place, zone, Map)



Map = {
    "Village" : ["Route", "Foret", "Grotte"],
    "Foret" : ["Foret Brulee", "Village"],
    "Grotte" : ["Salle du portail", "Village"],
    "Route" : ["Chateau", "Village"],
    "Chateau" : ["Route"],
    "Salle du portail" : ["Grotte"],
    "Foret Brulee" : ["Foret"]
}

zone = Map["Village"]
begin(zone, Map)

