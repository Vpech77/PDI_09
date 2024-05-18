####################################################
#  Création de l'image modele et masque sur QGIS   #
#  Par l'équipe LostInSwamp                        #
####################################################

from qgis.core import QgsProject, QgsSvgMarkerSymbolLayer

############################## Création du masque ##############################

##1 : Creation d'une grille recouvrant le region que l'on souhaite etudier, ici Ourq. 

processing.run("native:creategrid", 
                {'TYPE':2,
                'EXTENT':'672299.450000000,755604.300000000,6883498.000000000,6924036.000000000 [EPSG:2154]',
                'HSPACING':10,'VSPACING':10,'HOVERLAY':0,'VOVERLAY':0,
                'CRS':QgsCoordinateReferenceSystem('EPSG:2154'),
                'OUTPUT':'grilleOurq.shp'})

#TYPE: Specifie le type de grille à creer. Dans cet exemple, 2 correspond à une grille rectangulaire (polygone).
#EXTENT: Definit l'etendue spatiale de la grille à creer, specifiee sous forme de coordonnees xmin, ymin, xmax, ymax dans le système de coordonnees specifie (EPSG:2154). Ici, nous avons choisi de calculer l'etendu à partir de la couche route de la BD TOPO, une couche qui recouvre toute la zone que l'on souhaite etudier.
#HSPACING et VSPACING: Definissent l'espacement horizontal et vertical entre les lignes de la grille. On a decide de mettre 10 km pour les deux.
#HOVERLAY et VOVERLAY: Contrôlent le chevauchement horizontal et vertical des cellules de la grille.
#CRS: Specifie le système de reference spatial (CRS) de la grille.
#OUTPUT: Chemin vers le fichier de sortie contenant la grille creee.

""" 
Une fois la grille obtenue, on change son style pour qu'on obtienne un grand 
rectangle noir qui sera le fond de notre masque
"""

coucheGrille = QgsVectorLayer("grilleOurq.shp", "grilleOurq", "ogr")
# coucheGrille.loadNamedStyle('D:/carte_ancienne_2006/Qgis/stylemasque.qml')
# QgsProject.instance().addMapLayer(coucheGrille)

#2 : On repare la geometrie de la couche zone_veget_aquatique car celle ci etait invalide. 

processing.run("native:fixgeometries", 
                {'INPUT':'D:/carte_ancienne_2006/Qgis/zone_veget_aquatique.shx|layername=zone_veget_aquatique',
                'METHOD':1,
                'OUTPUT':'marais.shp'})

#INPUT: Chemin vers le fichier SHP contenant la couche avec des geometries incorrectes.
#METHOD: Methode utilisee pour reparer les geometries incorrectes. Dans cet exemple, 1 correspond à la methode "Fixer les geometries invalides".
#OUTPUT: Chemin vers le fichier de sortie contenant la couche avec les geometries reparees.

#3: Maintenant, on va recuperer les zones de marais se trouvant dans la grille que nous avons cree.

processing.run("native:clip", 
                {'INPUT':'marais.shp',
                'OVERLAY':'grilleOurq.shp',
                'OUTPUT':'maraisZoneOurq.shp'})

#INPUT: Chemin vers le fichier SHP contenant la couche à decouper, c'est à dire la couche qui contient tous les marais present en France Metropolitaine.
#OVERLAY: Chemin vers le fichier SHP contenant la couche servant de masque pour le decoupage, c'est à dire la couche que nous avons obtenu lors de la première etape.
#OUTPUT: Chemin vers le fichier de sortie contenant la couche decoupee.On obtient une couche ne contenant que les marais present dans notre zone d'etude, c'est à dire dans la region de l'Ourcq


    
#4 : Ajouter des points aleatoirement sur la couche marais qui corrrespondront aux pictogrammes de marais par la suite

processing.run("qgis:randompointsinsidepolygons", 
                {'INPUT':'maraisZoneOurq.shp',
                'STRATEGY':1,'VALUE':5e-05,'MIN_DISTANCE':70,
                'OUTPUT':'pointaleatoire.shp'})


#INPUT: Chemin vers le fichier SHP contenant la couche des polygones dans lesquels generer les points aleatoires, c'est à dire la couche generee lors de l'etape precedente.
#STRATEGY: Strategie utilisee pour generer les points aleatoires. Dans cet exemple, 1 correspond à la strategie "Points aleatoires uniformement repartis à l'interieur de chaque polygone".
#VALUE: Contrôle la densite des points aleatoires generes. Il specifie le nombre moyen de points par unite de surface. Dans cet exemple, 5e-05 indique une densite relativement faible de points.
#MIN_DISTANCE: Distance minimale entre les points generes. Cela garantit qu'aucun point ne sera genere à une distance inferieure à cette valeur de tout autre point ou bordure de polygone. Dans cet exemple, la distance minimale est definie à 70 unites (la valeur depend de l'unite de mesure utilisee dans votre système de coordonnees).
#OUTPUT: Chemin vers le fichier de sortie contenant la couche des points aleatoires generes.



# 5: Modifier le style  des points pour obtenir dans un premier temps les pictogrammes de marais bleus. Pour cela, on commence par cloner la couche des points aleatoires pour lui donner un nouveau nom

chemin_couche_points = 'pointaleatoire.shp'

# On commence par charger la couche de points aleatoires 
couche_points = QgsVectorLayer(chemin_couche_points, 'Point aleatoire', 'ogr')

# On cree une copie de la couche

couche_copie = couche_points.clone()

# On donne un nouveau nom à cette nouvelle couche
    
nom_couche_copie = 'pointaleatoirepictobleus'
   
couche_copie.setName(nom_couche_copie)
    
# On ajoute cette couche au projet

QgsProject.instance().addMapLayer(couche_copie)

layer = QgsVectorLayer("pointaleatoirepictobleus.shp", "pointaleatoirepictobleus", "ogr")

layer.loadNamedStyle('D:/carte_ancienne_2006/Qgis/stylepicto.qml')

#loadNamedStyle(): Methode pour charger un style predefini à partir d'un fichier QML specifie.

QgsProject.instance().addMapLayer(layer)

#addMapLayer(layer): Methode pour ajouter la couche specifiee au projet QGIS.



# 5: Modifier le style  des points pour obtenir les pictogrammes blancs et donc creer notre masque . On utilise la même methode que pour les pictogrammes bleus

#dans un premier temps, on clone la couche contenant les points aleatoires,dans le but que les pictogrammes bleus et les pictogrammes blancs soient positionnes exactement au même endroit

chemin_couche_points1 = 'pointaleatoire.shp'

# On commence par charger la couche de points aleatoires 
couche_points1 = QgsVectorLayer(chemin_couche_points1, 'Point aleatoire', 'ogr')

# On cree une copie de la couche

couche_copie1 = couche_points1.clone()

# On donne un nouveau nom à cette nouvelle couche
    
nom_couche_copie1 = 'pointaleatoirepictoblancs'
   
couche_copie.setName(nom_couche_copie1)
    
# On ajoute cette couche au projet

QgsProject.instance().addMapLayer(couche_copie1)

#Une fois cette nouvelle couche obtenue, on peut lui appliquer le style des pictogrammes de marais blancs

couche2 = QgsVectorLayer("pointaleatoirepictoblancs.shp", "pointaleatoirepictoblancs", "ogr")

couche2.loadNamedStyle('D:/carte_ancienne_2006/Qgis/stylepictoblanc.qml')

#loadNamedStyle(): Methode pour charger un style predefini à partir d'un fichier QML specifie.

QgsProject.instance().addMapLayer(couche2)



## 6 Une fois que nous avons toutes les couches qui nous interessent, nous allons pouvoir realiser la carte correspondant à la carte normal = une carte IGN avec des pictogrammes de marais et une carte representant le masque de la carte "normale" = un fond noir avec les pictogrammes blancs pour ensuite pouvoir les exporter de QGIS


###Premier cas = l'image "normale" = carte IGN et pictogrammes bleus


# Recuperer l'instance du projet QGIS
project = QgsProject.instance()

# On parcours toutes les couches du projet
for layer in project.mapLayers().values():
    # on verifie si le nom de la couche correspond à celui des pictogrammes bleue ou celui du fond de carte IGN
    if layer.name() == 'pointaleatoirepictobleus' or layer.name() == 'SCAN25TOUR':
        # On ajoute la couche à la liste des couches à afficher
        project.layerTreeRoot().addLayer(layer)
    else:
        # On recuperer le nœud de la couche dans l'arbre des couches
        layer_tree_node = project.layerTreeRoot().findLayer(layer.id())
        # On rend les couches qui ne correspondent pas aux pictogrammes, ni au fond de carte IGN non visible
        if layer_tree_node:
            layer_tree_node.setItemVisibilityChecked(False)



### Deuxième cas = le masque de l'image "normale"

for layer in project.mapLayers().values():
    # on verifie si le nom de la couche correspond à celui des pictogrammes bleue ou celui du fond de carte IGN
    if layer.name() == 'pointaleatoirepictoblancs' or layer.name() == 'grilleOurq':
        # On ajoute la couche à la liste des couches à afficher
        project.layerTreeRoot().addLayer(layer)
    else:
        # On recuperer le nœud de la couche dans l'arbre des couches
        layer_tree_node = project.layerTreeRoot().findLayer(layer.id())
        # On rend les couches qui ne correspondent pas aux pictogrammes, ni au fond de carte IGN non visible
        if layer_tree_node:
            layer_tree_node.setItemVisibilityChecked(False)

