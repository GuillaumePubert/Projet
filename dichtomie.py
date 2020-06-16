import stl
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
   # pyplot.show()
    return a,normale



def CalculForce(a,normale,hauteur):
    F_Archimede=0 #N
    F_Pression=0 #N
    Rho=1000 #g/L
    g=9.81 #m/s²
    Stot=0
    Stot_dans_eau=0
    Nb_facettes_dans_eau=0
    for n in range(0,len(a)): #on parcour pour le nombre de facettes

        """ajustement de la hauteur de la coque """
        a[n][0][2]+=hauteur
        a[n][1][2]+=hauteur
        a[n][2][2]+=hauteur

        """Calcule de la surface total et de chaque facette"""
        V=(a[n][1][0]-a[n][0][0],a[n][1][1]-a[n][0][1],a[n][1][2]-a[n][0][2])
        W=(a[n][2][0]-a[n][0][0],a[n][2][1]-a[n][0][1],a[n][2][2]-a[n][0][2])
        Ds=np.linalg.norm(np.cross(V,W))/2
        Stot+=Ds #surface totale de la coque

        DsVec=Ds*normale[n]

        """Calcule de la hauteur d'une facette """
        Zfk=(a[n][0][2]+a[n][1][2]+a[n][2][2])/3
        # print(a[i][0][2],a[i][0][2],a[i][0][2])

        """condition pour que une facette soit compté comme immergé """
        if Zfk <0:
            Stot_dans_eau+=Ds
            Nb_facettes_dans_eau+=1
            F_Archimede+=Rho*g*Zfk*Ds
            print(Zfk,Ds)
        else : F_Archimede+=0
        """calcule de la force de pression de la coque"""
        masse=160 #g
        F_Pression=masse*g
    return F_Pression,F_Archimede,Stot,Nb_facettes_dans_eau,Stot_dans_eau



#affichage_fichier_stl('V_HULL.stl')
print(CalculForce(affichage_fichier_stl('Rectangular_HULL.stl')[0],affichage_fichier_stl('Rectangular_HULL.stl')[1],-0.02))
