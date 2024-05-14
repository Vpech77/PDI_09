# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:54:35 2024

@author: LostInSwamp
"""
import os
import imageio
from PIL import Image

def decouper_images(input_folder, output_folder, taille=254):
    """ 
    Cette fonction prend en entrée nos images normales en png (masque et carte) dans le fichier ./tiff/mask pour
    le masque et le fichier ./tiff/normal pour la carte. Le fichier de sortie et la taille de découpage de 254X254.
    
    En sortie nous obtenons nos images découpées dans le fichier ./png/normal pour les images de notre carte
    et le fichier ./png/mask pour notre image du masque.
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
    Cette fonction permet de passer d'une image couleur à une image binaire pour le masque.
    On met en entrée le fichier avec les masques découpés ./png/mask.
    En sortie, on obtient des images binaire en png dans le fichier ./png/mask_bw.

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
    Cette Fonction permet de renommer les fichier des images binaires par leur nom initial + _mask
    Celà est nécessaire pour que l'IA fonctionne.
    """
    
    fichiers = os.listdir(input_folder)
    for fichier in fichiers:
        input_path = os.path.join(input_folder, fichier)
        if os.path.isfile(input_path):
            nom, extension = os.path.splitext(fichier)
            nouveau_nom = nom + "_mask" + extension
            output_path = os.path.join(input_folder, nouveau_nom)
            os.rename(input_path, output_path)

def remove_mask_from_title(directory):
    for filename in os.listdir(directory):
        # Séparation du nom du fichier et de l'extension
        name, extension = os.path.splitext(filename)
        
        # Vérifier si "_mask" est présent dans le nom du fichier
        if "_mask" in name:
            # Construire le nouveau nom de fichier sans "_mask"
            new_name = name.replace("_mask", "")
            new_filename = new_name + extension
            
            # Ancien et nouveau chemin
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            
            # Renommer le fichier
            os.rename(old_path, new_path)
            print(f"Le fichier {filename} a été renommé en {new_filename}")


if __name__ == "__main__":

    #Style carte ancienne 1997

    input_folder = "./tif/normal2006"
    output_folder = "./png/Normal2006"

    input_folder_mask = "./tif/mask2006"
    output_folder_mask = "./png/mask"
    output_folder_mask_bw = "./png/mask_bw2006"



    """
    #Style carte ancienne 2007

    input_folder = "./tif/normal2007"
    output_folder = "./png/Normal2007"

    input_folder_mask = "./tif/mask2007"
    output_folder_mask = "./png/mask2007"
    output_folder_mask_bw = "./png/mask_bw2007"
    """

    #remove_mask_from_title(output_folder_mask_bw)
    # decouper_images(input_folder, output_folder)
    # decouper_images(input_folder_mask, output_folder_mask)
    # couleur_to_binaire(output_folder_mask, output_folder_mask_bw)
    renommer_fichiers(output_folder_mask_bw)


