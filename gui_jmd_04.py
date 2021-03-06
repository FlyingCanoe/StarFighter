# Starfighter par ... au cvm, automne 2021
import random
import time
from helper import *
from tkinter import *


class Menu:
    def __init__(self, parent):
        self.vue = parent
        self.btn = Button(parent.cadre, text="Démarrer partie")
        self.btn.bind("<Button-1>", self.demmarerPartie)
        self.btn.pack()

    def pack_forget(self):
        self.btn.pack_forget()

    def pack(self):
        self.btn.pack()

    def demmarerPartie(self, evt):
        self.vue.demmarerPartie(evt)


class EcranDeJeu:
    def __init__(self, parent, partie):
        self.vue = parent
        self.canevas = Canvas(self.vue.cadre, width=400, height=400, bg="chartreuse2")
        self.tailleX=partie.dimX
        self.tailleY=partie.dimY
        self.canevas.config(width=self.tailleX, height=self.tailleY, bg="cyan")
        self.canevas.bind("<Motion>", self.vue.deplacer)
        self.canevas.bind("<Button>", self.vue.creerObus)

    def pack(self):
        self.canevas.pack()

    def pack_forget(self):
        self.canevas.pack_forget()

    def afficherPartie(self, partie):
        self.canevas.delete(ALL)
        vais=partie.vaisseau
        bord=vais.taille/2
        #self.canevas.create_rectangle(vais.x-bord, vais.y-bord, vais.x+bord, vais.y+bord, fill="red")
        self.canevas.create_polygon(vais.x, vais.y-bord, vais.x+bord, vais.y+bord, vais.x-bord, vais.y+bord, fill="red")
        for i in partie.vaisseau.obus:
            bord1=i.taille/2
            self.canevas.create_oval(i.x - bord1, i.y - i.taille, i.x + bord1, i.y + i.taille, fill="pink")
        for i in partie.ufos:
            bord=i.taille/2
            self.canevas.create_oval(i.x-bord, i.y-bord, i.x+bord, i.y+bord, fill="yellow")
            for j in i.projectiles:
                bord1=j.taille/2
                self.canevas.create_oval(j.x - bord1, j.y - j.taille, j.x + bord1, j.y + j.taille, fill="green")

##VUE#######
class Vue():
    def __init__(self, parent):
        self.parent=parent
        self.root=Tk() #Tk() est la fonction d'initialisation de l'environnement graphique, et comme effet secondaire, crée une fenêtre, qu'on met dans root
        self.root.title("Bienvenue")
        self.cadre = None
        self.menu = None
        self.ecran_de_jeu = None
        self.creerCadrePrincipal()

    def creerCadrePrincipal(self):
        self.cadre=Frame(self.root)
        self.menu = Menu(self)
        self.menu.pack()
        self.cadre.pack()

    def initialiserPartie(self, partie):
        self.menu.pack_forget()
        self.ecran_de_jeu = EcranDeJeu(self, partie)
        self.ecran_de_jeu.pack()

    def creerObus(self,evt):
        self.parent.creerObus()

    def demmarerPartie(self, evt): #evt est l'event créé par .bind()
        self.parent.demmarerPartie()

    def afficherPartie(self, partie):
        self.canevas.delete(ALL)
        vais=partie.vaisseau
        bord=vais.taille/2
        #self.canevas.create_rectangle(vais.x-bord, vais.y-bord, vais.x+bord, vais.y+bord, fill="red")
        self.canevas.create_polygon(vais.x, vais.y-bord, vais.x+bord, vais.y+bord, vais.x-bord, vais.y+bord, fill="red")
        for i in partie.vaisseau.obus:
            bord1=i.taille/2
            self.canevas.create_oval(i.x - bord1, i.y - i.taille, i.x + bord1, i.y + i.taille, fill="pink")
        for i in partie.ufos:
            bord=i.taille/2
            self.canevas.create_oval(i.x-bord, i.y-bord, i.x+bord, i.y+bord, fill="yellow")

    def deplacer(self, evt):
        x=evt.x
        y=evt.y
        self.parent.deplacer(x, y)

    def game_over(self):
        self.ecran_de_jeu.pack_forget()
        self.menu.pack()
        pass

##MODELE###########
class Starfighter():
    def __init__(self, parent):
        self.parent=parent
        self.partie=None
        self.nbrUfoParNiveau=5

    def demarrerPartie(self):
        self.partie=Partie(self)

    def deplacer(self, x, y):
        self.partie.deplacer(x, y)

    def jouerCoup(self):
        self.partie.jouerCoup()

class Partie():
    def __init__(self, parent):
        self.parent=parent
        self.niveau = 0
        self.dimX=400
        self.dimY=600
        vaisX=self.dimX/2
        vaisY=self.dimY*0.8
        self.vaisseau=Vaisseau(self, vaisX, vaisY)
        self.ufos=[]
        self.ufosMorts=[]
        self.creerNiveau()

    def deplacer(self, x, y):
        self.vaisseau.deplacer(x, y)

    def jouerCoup(self):
        self.jouerCoupObus()
        self.jouerCoupUfos()
        if not self.ufos:
            self.creerNiveau()

    def jouerCoupObus(self):
        for i in self.vaisseau.obus:
            i.deplacer()
            if i.y <= -i.taille:
                self.vaisseau.obusMort.append(i)
        self.vaisseau.supprimeObus()

    def jouerCoupUfos(self):
        for i in self.ufos:
            i.deplacer()
        #self.verifierCollision()
        for i in self.ufosMorts:
            self.ufos.remove(i)
        self.ufosMorts = []

    def verifierCollision(self):
        for i in self.ufos:
            for j in self.vaisseau.obus:
                ufox0, ufoy0, ufox1, ufoy1 = i.hitbox()
                obusx0, obusy0, obusx1, obusy1 = j.hitbox()
                if (obusx0 >= ufox0 and obusx0 <= ufox1) or (obusx1 >= ufox0 and obusx1 <= ufox1):
                    if (ufoy0 >= obusy0 and ufoy0 <=obusy1) or (ufoy1 >= obusy0 and ufoy1 <= obusy1):
                        self.ufosMorts.append(i)
                        self.vaisseau.obusMort.append(j)

    def creerNiveau(self):
        self.niveau+=1
        self.ufos=[]
        nbrUfos=self.niveau * self.parent.nbrUfoParNiveau
        for i in range(nbrUfos):
            x = random.randrange(self.dimX)
            y = -10
            self.ufos.append(Ufo(self, x, y))

    def creerObus(self):
        self.vaisseau.creerObus()

    def supprimerUfos(self):
        for i in self.ufosMorts:
            self.ufos.remove(i)
        self.ufosMorts = []


class Vaisseau:
    def __init__(self, parent, x, y):
        self.parent=parent
        self.taille=30
        self.x=x
        self.y=y
        self.obus=[]
        self.obusMort=[]

    def deplacer(self, x, y):
        self.x=x
        self.y=y

    def creerObus(self):
        self.obus.append(Obus(self, self.x, self.y))

    def supprimeObus(self):
        for i in self.obusMort:
            self.obus.remove(i)
        self.obusMort = []

    def hitbox(self):
        x0=self.x-(self.taille/2)
        y0=self.y-(self.taille/2)
        x1=self.x+(self.taille/2)
        y1=self.y+(self.taille/2)
        return x0, y0, x1, y1


class Obus:
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y-(self.parent.taille/2)
        self.vitesse = 10
        self.taille = 4

    def deplacer(self):
        self.y -= self.vitesse

    def hitbox(self):
        x0=self.x-(self.taille/2)
        y0=self.y-(self.taille/2)
        x1=self.x+(self.taille / 2)
        y1=self.y+(self.taille / 2)
        return x0, y0, x1, y1


class Ufo:
    def __init__(self, parent, x, y):
        self.parent=parent
        self.taille=16
        self.vitesse=6
        self.x=x
        self.y=y
        self.cibleX=0
        self.cibleY=0
        self.angle=0
        self.trouvercible()

    def trouvercible(self):
        self.cibleX = random.randrange(self.parent.dimX)
        self.cibleY = self.parent.dimY+10
        self.angle = Helper.calcAngle(self.x, self.y, self.cibleX, self.cibleY)

    def deplacer(self):
        self.x, self.y = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
        distanceRestante = Helper.calcDistance(self.x, self.y, self.cibleX, self.cibleY)
        if distanceRestante < self.vitesse:
            self.parent.ufosMorts.append(self)

    def deplacer1(self):
        x=random.randrange(-self.taille, self.taille) #-(self.taille/2)
        y=random.randrange(-self.taille, self.taille) #-(self.taille/2)
        self.x+=x
        self.y+=y

    def hitbox(self):
        x0 = self.x-((self.taille/2))
        y0 = self.y-((self.taille/2))
        x1 = self.x+((self.taille/2) )
        y1 = self.y+((self.taille/2))
        return x0, y0, x1, y1

##CONTROLEUR#######
class Controleur():
    def __init__(self):
        self.vue=Vue(self)
        self.modele=Starfighter(self)
        self.partie=None
        self.vue.root.mainloop() #Démarre l'application avec environnement graphique


    def demmarerPartie(self):
        self.modele.demarrerPartie()
        self.partie = self.modele.partie
        self.vue.initialiserPartie(self.partie)
        self.vue.afficherPartie(self.partie)
        self.vue.root.after(50, self.jouerCoup)

    def jouerCoup(self):
        self.modele.jouerCoup()
        self.vue.afficherPartie(self.partie)
        if self.partie_en_cours == True:
            self.vue.root.after(16, self.jouerCoup)

    def deplacer(self, x, y):
        self.modele.deplacer(x, y)
        self.vue.afficherPartie(self.partie)

    def creerObus(self):
        self.partie.creerObus()

if __name__ == '__main__':
    c=Controleur() #Crée une instance (un objet) de la classe controleur
    print("FIN")
