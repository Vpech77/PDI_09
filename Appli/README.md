# 🐣 Guide d'utilisateur 🐣 
L’équipe LostInSwamp est ravie de vous présenter Swampy, notre application créée avec énormément de passion.
Si vous voulez détecter des pictogrammes dans des images de cartes anciennes grâce à du deep learning, eh bien, Swampy est fait pour vous! Grâce à notre application, vous pouvez non seulement générer des jeux d’entraînement essentiels pour créer votre modèle, mais aussi créer votre propre modèle de deep learning avec les hyperparamètres que vous souhaitez! Amazing! ヽ(^o^)丿

# ⭐ Générez votre dataset ⭐

# 🌟 Créer votre propre modèle de deep learning 🌟

Dans le dossier *modeleDeepLearning*, vous avez tous ce qu'il vous faut pour entraîner votre modele et le tester sur les images de cartes anciennes que vous voulez. 

## 🖥️ Avec un environnement local 🖥️

### Entraînement du modèle

- Le dossier *Dataset* contient le premier dataset de base de l'équipe LostInSwamp et est composé de deux dossiers : *images* qui contient les images modèles et *annotations* qui contient les masques de ces images modèles. Si vous voulez utiliser un autre dataset, remplacez ce dossier par votre propre dossier Dataset et respecter l'arborescence du dossier en gardant les mêmes noms de dossier.

- C'est avec le script python *model_training.py* que vous allez entraîner votre modèle. Vous pouvez définir les hyperparamètres du modèle en modifiant dans le script les valeurs : ligne 26 pour le **batch size** et ligne 27 pour l'**epoch**. Et vous n'avez plus qu'à exécuter le code.
  - Votre modèle entrainé est directement sauvegardé dans le dossier *model* et prend automatiquement le nom **unet_<batch_size>batch_<epoch>epoch.keras**
  - Dans le dossier *output_training*, est généré automatiquement le dossier **unet_<batch_size>batch_<epoch>epoch_results** lié à l'entrainement de votre modèle et contient donc :
      - le csv et le dataframe contenant les paramètres de performances du modèle
      - le graphique de ses performances
      - une image résultat généré après chaque epoch : pour chaque epoch, le modèle s'entraîne avec toutes les images du jeu d'entrainement et tire au hasard une image dans le jeu de validation et après son entrainement se teste avec, c'est cette image qui est générée.

### Entraînement du modèle

- C'est avec le script *model_testing* que vous allez tester votre modèle. Tout d'abord, définissez dans le script, ligne 17 le nom du modèle que vous voulez tester et qui se trouve dans le dossier *model* ainsi que le nom du dossier contenant les images à tester, ce dossier doit se trouver dans le dossier *imgCartesAnciennes*. Ce dossier *imgCartesAnciennes* contient deux dossiers d'imagettes de cartes anciennes.
- Les images résultats du test se retrouvent automatiquement dans le dossier *output_testing*

## 🌐 Avec un environnement virtuel 🌐
Voici le lien pour accéder au google colab : https://colab.research.google.com/drive/1nLMtVMuyCFf0LCDyIR7ITDeoW9_fsttq?usp=sharing
Copier le fichier sur votre drive pour pouvoir l'éditer comme bon vous semble. Avant de l'exécuter, il faut que vous zippiez votre dossier Dataset et que vous le mettiez sur votre google drive.
