# Cahier des charges

## Objectif :

Créer un chatbot IA accessible via une interface web qui permettra aux utilisateurs :

- De poser des questions en langage naturel
- D’obtenir des réponses instantanées et contextuelles
- De consulter et gérer l’historique de leurs échanges

## Besoins :

Le prestataire devra :

- Développer une application web intégrant le chatbot IA (backend en Python avec Flask ou FastAPI, frontend en HTML/CSS et Jinja)
- Mettre en place un système de stockage des conversations (base de données ou fichiers JSON)
- Intégrer ou préparer l’intégration d’un modèle NLP avancé
- Offrir une interface ergonomique et responsive (adaptée aux mobiles et ordinateurs)

## Public :

Utilisateurs recherchant une assistance automatisée et accessible 24/7, incluant :

- Particuliers souhaitant obtenir rapidement des informations
- Entreprises désireuses d’améliorer leur support client
- Utilisateurs ne maîtrisant pas toujours l’utilisation d’outils complexes

## Concurrents :

Les solutions existantes sur le marché incluent divers chatbots et assistants virtuels (ex. ChatGPT, IBM Watson).

### Comparaison avec les concurrents, différences au niveau des fonctionnalités

#### IBM Watson Assistant

- Points forts :

  - Interface web intuitive avec tableau de bord analytique pour le suivi des interactions
  - Compréhension avancée du langage naturel grâce à des modèles NLP sophistiqués
  - Support de nombreuses langues pour une utilisation internationale
  - Réponses contextuelles et conservation de l'historique des conversations
  - Modèles de conversation prédéfinis pour un déploiement rapide

- Limitations :
  - Nécessite un abonnement mensuel après 30 jours d'essai gratuit
  - Restrictions d'utilisation à 10 000 documents et 10 000 requêtes mensuelles
  - Efficacité variable selon les langues, surtout pour les moins courantes
  - Intégration complexe avec des systèmes externes non-IBM
  - Interface moins adaptable que notre solution prévue avec HTML/CSS et Jinja
#### ChatGPT :
- Points forts :
  - Le ChatGPT pourrait générer automatiquement les titres de chaque conversation. Pourtant, notre chatbot donne un datetime pour chaque conversation.
  - Dans le ChatGPT, chaque conversation est représenté dans une page individuelle, alors qu'ici toutes les historiques sont dans la même page.
  - Le ChatGPT propose une IA plus puissante avec environ 500 milliards et 1 trilions de paramètres. Alors que le nôtre, qui est llama3.2-3b n'a que 3 milliards de paramètres.
  - Le ChatGPT peut prendre et analyser des fichiers locaux joints tels que l'image, le fichier texte, le pdf, etc, ce qui n'est pas possible dans notre chatbot.
- Limitations : 
-   inon, l'utilisateur ne peut que utiliser un modèle moins performant.

#### ChatGPT :
##### Ses points forts :
- Le ChatGPT pourrait générer automatiquement les titres de chaque conversation. Pourtant, notre chatbot donne un datetime pour chaque conversation.
- Dans le ChatGPT, chaque conversation est représenté dans une page individuelle, alors qu'ici toutes les historiques sont dans la même page.
- Le ChatGPT propose une IA plus puissante avec environ 500 milliards et 1 trilions de paramètres. Alors que le nôtre, qui est llama3.2-3b n'a que 3 milliards de paramètres.
- Le ChatGPT peut prendre et analyser des fichiers locaux joints tels que l'image, le fichier texte, le pdf, etc, ce qui n'est pas possible dans notre chatbot.
##### Ses limitations : 
- Le meilleur modèle du ChatGPT a une limite de tokens entrés et sortis, ce qui nécessite un abonnement quand la limite est atteinte. Sinon, l'utilisateur ne peut que utiliser un modèle moins performant.

## Identité graphique :

- Typographie moderne et lisible :
  L’application utilisera la police Poppins via Google Fonts pour offrir un rendu contemporain et une excellente lisibilité, garantissant ainsi une expérience utilisateur agréable.
- Design épuré et minimaliste :
  L’interface adopte un design simple et sans surcharge visuelle, permettant aux utilisateurs de se concentrer sur l’échange avec le chatbot. L’utilisation d’un layout structuré et de blocs de contenu clairement définis assure une navigation fluide.
- Logo et identité visuelle forte :
  Le logo, intégré dans l’en-tête, renforce l’identité du chatbot et assure une reconnaissance immédiate de l’application.
- Interface responsive :
  Le design s’adapte aux différents supports (mobiles, tablettes, ordinateurs), garantissant une expérience cohérente et optimisée, quel que soit l’appareil utilisé.
