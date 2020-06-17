import outil
from stl import mesh,main
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import numpy as np

def affichage_fichier_stl(lien) :
    figure= pyplot.figure()
    axes=mplot3d.Axes3D(figure)
    fichier=mesh.Mesh.from_file(lien)
    a=(fichier.vectors)
    normale=(fichier.normals)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(fichier.vectors))
    scale = fichier.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)
    #pyplot.show()
    return a,normale

def Chgt_Hauteur_Bateau(hauteur,a):
    for n in range(0,len(a)):
        a[n]+=hauteur
    return a

def Calcul_Surface_Facette(a,n):
    U=outil.calculVecteur(a[n][0],a[n][1])
    V=outil.calculVecteur(a[n][0],a[n][2])
    Surface_Facette=outil.norme(outil.produitVectoriel(U,V))
    return Surface_Facette

def Calcul_Surface_Totale(a):
    Surface_totale=0
    for n in range(0,len(a)): #on parcour pour le nombre de facettes
        Surface_Facette=Calcul_Surface_Facette(a,n)
        Surface_totale+=Surface_Facette #surface totale de la coque
    return Surface_totale

def Calcul_Hauteur_Facette(a,n):
        Hauteur_facette_n=outil.calculeHauteurFacette(a[n][0],a[n][1],a[n][2])
        return Hauteur_facette_n

def Facette_Immergee(a,n):
        if Calcul_Hauteur_Facette(a,n) <0:
            return True
        else:
            return False

def Calcul_VectF_Archimede(a,normale,Rho,g):
    Vect_Archimede=0
    for n in range(0,len(a)):
        if Facette_Immergee(a,n)==True:
            Vect_Archimede+=Rho*g*Calcul_Hauteur_Facette(a,n)*Calcul_Surface_Facette(a,n)*normale
        else:
            Vect_Archimede+=0
    return Vect_Archimede


def Calcul_VectFPoids(masse,g):
    Vect_Poids=(0,0,-1*masse*g)
    return Vect_Poids

def Norme_Poids(masse,g):
    NormePoids=np.linalg.norm(Calcul_VectFPoids(masse,g))
    return NormePoids

def Norme_Archimede(a,normale,Rho,g):
    Norme_Archimede=np.linalg.norm(Calcul_VectF_Archimede(a,normale,Rho,g))
    return Norme_Archimede


def Calcul_Force_Total(masse,g,a,normale,Rho):
    difference= Norme_Archimede(a,normale,Rho,g)-Norme_Poids(masse,g)
    return difference

rectangle='Rectangular_HULL.STL'
v='V_HULL.STL'
cylindre='Cylindrical_HULL.STL'
print(Calcul_Force_Total(1000,9.81,Chgt_Hauteur_Bateau(-0.5,affichage_fichier_stl(rectangle)[0]),affichage_fichier_stl(rectangle)[1],1000))
#print(Chgt_Hauteur_Bateau(-0.1,affichage_fichier_stl(lien)[0]))
#Calcul_VectF_Archimede(Chgt_Hauteur_Bateau(-0.9,affichage_fichier_stl(lien)[0]),affichage_fichier_stl(lien)[1],1000,9.81)
