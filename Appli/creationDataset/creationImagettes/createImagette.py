# -*- coding: utf-8 -*-
####################################################
#   Générer les imagettes du dataset               #
#                   Par l'équipe LostInSwamp       #
####################################################

##################### Import des librairies #####################
import os
import imageio
from PIL import Image

def decouper_images(input_folder, output_folder, taille=256):
    """ 
    Fonction qui prend en entrée un dossier contenant une image png (image de carte ou masque) et découpe ces images en imagettes de taille donnée et les mets dans le dossier de sortie indiqué en argument.

    :param str input_folder: nom du fichier contenant l'image à découper
    :param str output_folder: nom du fichier qui contiendra les imagettes      créees 
    :param int taille: taille des imagettes par défault égale à 256
    """
    fichiers = os.listdir(input_folder)
    for fichier in fichiers:
        if fichier.lower().endswith('.png'):
            input_path = os.path.join(input_folder, fichier)
            image = Image.open(input_path)
            largeur, hauteur = image.size
            nb_morceaux_largeur = (largeur + taille - 1) // taille
            nb_morceaux_hauteur = (hauteur + taille - 1) // taille
            for y in range(nb_morceaux_hauteur):
                for x in range(nb_morceaux_largeur):
                    x_debut = x * taille
                    y_debut = y * taille

                    x_fin = min((x + 1) * taille, largeur)
                    y_fin = min((y + 1) * taille, hauteur)

                    morceau = image.crop((x_debut, y_debut, x_fin, y_fin))
                    nom_morceau = f"{os.path.splitext(fichier)[0]}_{x}_{y}.png"
                    output_path = os.path.join(output_folder, nom_morceau)
                    morceau.save(output_path)

def couleur_to_binaire(input_folder, output_folder):
    """
    Fonction qui transforme toutes les images couleurs contenu dans le dossier
    donnée en entrée en images binaire en les mettant dans un autre dossier.

    :param str input_folder: nom du fichier contenant les images couleurs
    :param str output_folder: nom du fichier qui contiendra les images binaires
    """
    fichiers = os.listdir(input_folder)
    for fichier in fichiers:
        if fichier.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(input_folder, fichier)
            image = Image.open(input_path)
            image = image.convert("L")
            largeur, hauteur = image.size
            for y in range(hauteur):
                for x in range(largeur):
                    pixel = image.getpixel((x, y))
                    nouvelle_valeur = 0 if pixel < 50 else 255
                    image.putpixel((x, y), nouvelle_valeur)
            output_path = os.path.join(output_folder, fichier)
            image.save(output_path)

def renommer_fichiers(input_folder):
    """
    Fonction qui renomme les fichier des images binaires (masque) par leur nom initial en y ajoutant le suffixe '_mask'
    """
    fichiers = os.listdir(input_folder)
    for fichier in fichiers:
        input_path = os.path.join(input_folder, fichier)
        if os.path.isfile(input_path):
            nom, extension = os.path.splitext(fichier)
            nouveau_nom = nom + "_mask" + extension
            output_path = os.path.join(input_folder, nouveau_nom)
            os.rename(input_path, output_path)

if __name__ == "__main__":

    NameModele_png = "2007"
    NameMasque_png = NameModele_png + "masque"

    ################### Nom des fichiers ########################
    input_folder = "./modele"
    output_folder = "./tuile_modele"

    input_folder_mask = "./masque"
    output_folder_mask = "./tuile_masque_brut"
    output_folder_mask_bw = "./tuile_modele"

    ################### Début de la création du dataset ########################
    decouper_images(input_folder, output_folder)
    decouper_images(input_folder_mask, output_folder_mask)
    couleur_to_binaire(output_folder_mask, output_folder_mask_bw)
    renommer_fichiers(output_folder_mask_bw)


