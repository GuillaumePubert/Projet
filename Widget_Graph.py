import outil
from stl import mesh,main
from mpl_toolkits import mplot3d
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot
from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout
import numpy as np


class Widget_Graph(QWidget) :
    def __init__(self,lien='') :
        QWidget.__init__(self)
        self.fig = pyplot.figure()
        self.canvas = FigureCanvas(self.fig)
        axes=pyplot.axes()

        fichier=mesh.Mesh.from_file(lien)
        a=(fichier.vectors)
        normale=(fichier.normals)

        normale[7][0]=1  #Vecteur normal du fichié V dans le mauvais sens des x


        """baisser la présicion"""

        hauteur,nb_rep,liste=outil.Dichotomie(2,-4,0.0000001,a,normale,Rho=1000,masse=2000)
        outil.translation(2,a,hauteur)
        x=np.linspace(0,nb_rep,nb_rep)
        axes.plot(x,liste)
        #pyplot.show()
        self.canvas.draw()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

if __name__ == '__main__' :
    app=QApplication()
    window=Widget_Graph('V_HULL.stl')
    window.show()
    app.exec_()
