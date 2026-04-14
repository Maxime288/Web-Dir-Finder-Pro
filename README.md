# 🕷️ Web-Dir Finder Pro

> **Outil de découverte de répertoires et fichiers cachés**
> Un utilitaire de brute-force Web (Fuzzing) permettant de cartographier la structure d'un serveur et d'identifier des ressources non liées (pages d'admin, backups, fichiers de config).
> Python 3 · Requests · Reconnaissance Web.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-Reconnaissance-red)
![Category](https://img.shields.io/badge/Category-Web%20OSINT-orange)

---

## 📋 Présentation

**Web-Dir Finder Pro** est un scanner de répertoires léger et efficace. Lors d'un audit de sécurité, la découverte de répertoires cachés est une étape critique. Ce script automatise le test de milliers de combinaisons à partir d'une liste de mots (wordlist) pour identifier les points d'entrée potentiels d'une application web.

### Fonctionnalités principales :

* **Détection intelligente** : Analyse les codes de statut HTTP (200, 403, 301/302).
* **Gestion des Timeouts** : Évite de bloquer le script si le serveur est lent.
* **Formatage d'URL** : Nettoyage automatique des slashs pour éviter les erreurs de requête.
* **Code couleur** : Interface visuelle claire pour distinguer rapidement les succès des erreurs.

---

## ⚙️ Installation & Prérequis

### Prérequis

Le script utilise la bibliothèque `requests` pour gérer les interactions HTTP.

```bash
pip install requests
```

### Installation

```bash
git clone https://github.com/Maxime288/Web-Dir-Finder-Pro.git
cd Web-Dir-Finder-Pro
chmod +x web_dir_finder.py
```

---

## 🚀 Utilisation

Vous devez fournir une URL cible et une wordlist (fichier texte contenant un mot par ligne).

### Syntaxe

```bash
python3 web_dir_finder.py -u http://192.168.1.X -w common.txt
```

### Codes de statut gérés :

| Code | Statut | Description |
|------|--------|-------------|
| `200` | OK | La ressource est accessible publiquement. |
| `403` | Forbidden | La ressource existe mais l'accès est restreint (intéressant pour l'escalade de privilèges). |
| `301/302` | Redirect | La ressource redirige vers une autre page. |

---

## 🔬 Détails Techniques

L'outil fonctionne par énumération itérative. Pour chaque entrée de la wordlist, il construit une URL complète et analyse la réponse du serveur.

1. **Requête GET** : Envoi de l'en-tête vers la cible.
2. **Analyse de réponse** : Extraction du `status_code`.
3. **Log** : Affichage uniquement des résultats pertinents (on ignore les `404`).

---

## ⚠️ Avertissement Légal

> L'utilisation de cet outil sur des serveurs dont vous n'avez pas l'autorisation explicite est **illégale** et contraire à l'éthique.
> Cet outil est fourni à des fins éducatives et doit uniquement être utilisé dans le cadre de tests sur vos propres systèmes ou dans des environnements de lab autorisés (CTF, machines virtuelles, etc.).
> **L'auteur décline toute responsabilité en cas d'utilisation abusive.**
