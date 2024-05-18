# 🐣 Guide d'utilisateur 🐣 
L’équipe 𝑳𝒐𝒔𝒕𝑰𝒏𝑺𝒘𝒂𝒎𝒑 est ravie de vous présenter 𝑺𝒘𝒂𝒎𝑷𝒚, notre application créée avec énormément de passion.
Si vous voulez détecter des pictogrammes dans des images de cartes anciennes grâce à du deep learning, eh bien, Swampy est fait pour vous! Grâce à notre application, vous pouvez non seulement générer des jeux d’entraînement essentiels pour créer votre modèle, mais aussi créer votre propre modèle de deep learning avec les hyperparamètres que vous souhaitez! Amazing! ヽ(^o^)丿

# ⭐ Générez votre dataset ⭐

Pour rappel, le dataset est composé de tuiles d'images modèles de cartes possédant des pictogrammes ou non et les tuiles du masque de ses images modèles.

## 🎭 Créer votre masque dans votre projet QGIS 🎭

1. Lancez le script *model_mask_qgis.py* du dossier *creationImage* dans la console python de QGIS (ctrl+alt+P pour y accéder).
2. Exportez votre projet en format PNG.

## ✂️ Générer les tuiles de vos images ✂️

1. Mettez toutes vos images PNG générées précédemment dans le dossier *modele* si ce sont des images modèles sinon dans le dossier *masque*.
2. Lancez le script *createImagette.py*, attendez un peu et vous trouverez les tuiles dans les dossiers correspondant.
3. Créer un dossier *Dataset* avec deux sous-dossier : *images* pour y mettre vos tuiles du dossier *tuile_modele* et *annotations* pour y mettre vos tuiles du dossier *tuile_masque*

# 🌟 Créer votre propre modèle de deep learning 🌟

Dans le dossier *modeleDeepLearning*, vous avez tous ce qu'il vous faut pour entraîner votre modele et le tester sur les images de cartes anciennes que vous voulez. Enjoy! (◕‿◕✿)

## 🖥️ Avec un environnement local 🖥️

###  🏋️‍♂️ Entraînement du modèle 🏋️‍♂️

#### 📊 Dataset 📊
Le dossier *Dataset* contient le premier dataset de base de l'équipe LostInSwamp et est composé de deux dossiers :
    1. *images* qui contient les images modèles
    2. *annotations* qui contient les masques de ces images modèles.

Si vous voulez utiliser un autre dataset, remplacez ce dossier par votre propre dossier Dataset et respecter l'arborescence du dossier en gardant les mêmes noms de dossier.

#### 🐍 Script python 🐍
C'est avec le script python *model_training.py* que vous allez entraîner votre modèle. Vous pouvez définir les hyperparamètres du modèle en modifiant dans le script les valeurs : ligne 26 pour le **batch size** et ligne 27 pour l'**epoch**. Et vous n'avez plus qu'à exécuter le code.
  
  - Votre modèle entrainé est directement sauvegardé dans le dossier *model* et prend automatiquement le nom 𝐮𝐧𝐞𝐭_<𝐛𝐚𝐭𝐜𝐡_𝐬𝐢𝐳𝐞>𝐛𝐚𝐭𝐜𝐡_<𝐞𝐩𝐨𝐜𝐡>𝐞𝐩𝐨𝐜𝐡.𝐤𝐞𝐫𝐚𝐬
  - Dans le dossier *output_training*, est généré automatiquement le dossier 𝐮𝐧𝐞𝐭_<𝐛𝐚𝐭𝐜𝐡_𝐬𝐢𝐳𝐞>𝐛𝐚𝐭𝐜𝐡_<𝐞𝐩𝐨𝐜𝐡>𝐞𝐩𝐨𝐜𝐡_𝐫𝐞𝐬𝐮𝐥𝐭𝐬 lié à l'entrainement de votre modèle et contient donc :
    
      - le csv et le dataframe contenant les paramètres de performances du modèle
      - le graphique de ses performances
      - une image résultat généré après chaque epoch : pour chaque epoch, le modèle s'entraîne avec toutes les images du jeu d'entrainement et tire au hasard une image dans le jeu de validation et après son entrainement se teste avec, c'est cette image qui est générée.

### 💯 Test du modèle 💯

- C'est avec le script *model_testing* que vous allez tester votre modèle. Tout d'abord, définissez dans le script, ligne 17 le nom du modèle que vous voulez tester et qui se trouve dans le dossier *model* ainsi que le nom du dossier contenant les images à tester, ce dossier doit se trouver dans le dossier *imgCartesAnciennes*.
  
- Les images résultats du test se retrouvent automatiquement dans le dossier *output_testing*

## 🌐 Avec un environnement virtuel 🌐
Voici le lien pour accéder au google colab : https://colab.research.google.com/drive/1nLMtVMuyCFf0LCDyIR7ITDeoW9_fsttq?usp=sharing

1. Copier le fichier sur votre drive pour pouvoir l'éditer comme bon vous semble.
2. Avant de l'exécuter, il faut que vous zippiez votre dossier *Dataset* et que vous le mettiez sur votre google drive.
