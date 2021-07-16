from random import randint
import time

motsfrancais = []
file = open('repertoire_francais_tout.txt','r')
for ligne in file:
    motsfrancais.append(ligne.strip(' \n'))
for mot in motsfrancais:
    if len(mot) <= 2:
        motsfrancais.remove(mot)
        
def ajouter_mot(dic,mot):
    if mot == '':
        dic['.'] = {}
    else:
        c = mot[0]
        if c not in dic.keys():
            dic[c] = {}
        ajouter_mot(dic[c],mot[1:])

def dictionnaire(L):
    dic = {}
    for mot in L:
        ajouter_mot(dic,mot)
    return dic

motsfrancais = dictionnaire(motsfrancais)

def est_dans(dic,mot):
    if mot == '':
        if '.' in dic.keys():
            return True
        else:
            return False
    else:
        c = mot[0]
        if c not in dic.keys():
            return False
        return est_dans(dic[c],mot[1:])

def tirage(n):
    lettres=['A','A','A','A','A','E','E','E','E','E','I','I','I','I','I','O','O','O','O','O','U','U','U','U','U','B','B','C','C','D','D','F','F','G','G','H','H','L','L','M','M','N','N','P','P','R','R','S','S','T','T','K','J','Q','V','W','X','Y','Z']
    liste = []
    for i in range(n):
        liste += [lettres[randint(0,58)]]
    return liste

def grille(n):
    tableau = []
    for i in range(n):
        tableau.append(tirage(n))
    return tableau

def affgrille(tableau):
    n = len(tableau)
    sep = '+'
    for i in range(n):
        sep += '---+'
    print(sep)
    for ligne in tableau:
        lettres = '| '
        for lettre in ligne:
            lettres += lettre
            lettres += ' | '
        print(lettres)
        print(sep)
        
def casemot(gr,tab):
    mot = ''
    for x,y in tab:
        mot += gr[x][y]
    return mot
        
def recherche(G,i,j,dic,tab,n):
    accessibles = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)]
    liste = []
    mot = casemot(G,tab)
    if '.' in dic:
        liste += [mot]
    for c in accessibles:
        x,y = c
        if x>=0 and x<n and y>=0 and y<n and (x,y) not in tab:
            if G[x][y] in dic:
                liste += recherche(G,x,y,dic[G[x][y]],tab+[(x,y)],n)
    return liste

def motsgrille(gr):
    liste = []
    for i in range(len(gr)):
        for j in range(len(gr)):
            liste += recherche(gr,i,j,motsfrancais[gr[i][j]],[(i,j)],len(gr))
    liste.sort()
    liste_finale = [liste[0]]
    for i in range(1,len(liste)):
        if liste[i] != liste_finale[len(liste_finale)-1]:
            liste_finale.append(liste[i])
    return liste_finale
    
# \033[2K -> clear line
# \033[2J -> clear terminal (Spyder)
# \033c -> clear terminal (bash)

def jeu():
    n = '-'
    print('\033c')
    while not n.isnumeric():
        n = input('Taille de la grille : ')
    n = int(n)
    play = True
    temps = 60.0 * (n-1)
    while play:
        gr = grille(n)
        mots_trouves = []
        mots = motsgrille(gr)
        deb = time.time()
        while time.time() - deb < temps:
            print('\033c')
            affgrille(gr)
            print('\n' + str(int(temps - time.time() + deb)) + ' secondes restantes',end='\n\n')
            for m in mots_trouves:
                print(m)
            mot = input().upper()
            if mot in mots:
                mots_trouves.append(mot)
            elif mot == '^C':
                break
            else:
                print('\033[2K')
        print('\n\033cScore : %s%%' % (int(len(mots_trouves)/len(mots)*10000)/100))
        print('\nMots trouves :')
        mots_trouves.sort()
        for mot in mots_trouves:
            print(mot,end='\t')
        print('\n\nMots non trouves :')
        for mot in mots:
            if mot not in mots_trouves:
                print(mot,end='\t')
        r = input('\nRecommencer ? (y/n) ')
        play = r == 'y'

if __name__ == '__main__':
    jeu()