#!/usr/bin/env python3
"""
🕷️ Web-Dir Finder Pro v1.1
Outil de brute-force de répertoires web (Multi-threaded).
Optimisé pour la reconnaissance sur cibles type Metasploitable.
"""

import requests
import argparse
import concurrent.futures
from datetime import datetime
import sys

# ──────────────────────────────────────────────────────────────
# Couleurs & Style
# ──────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[38;5;196m"
    GREEN   = "\033[38;5;82m"
    YELLOW  = "\033[38;5;226m"
    BLUE    = "\033[38;5;45m"
    CYAN    = "\033[38;5;51m"
    GRAY    = "\033[38;5;244m"

BANNER = fr"""
{C.BLUE}  __          __  _      {C.CYAN} _____  _         {C.RESET}
{C.BLUE}  \ \        / / | |    {C.CYAN}|  __ \(_)        {C.RESET}
{C.BLUE}   \ \  /\  / /__| |__  {C.CYAN}| |  | |_ _ __    {C.RESET}
{C.BLUE}    \ \/  \/ / _ \ '_ \ {C.CYAN}| |  | | | '__|   {C.RESET}
{C.BLUE}     \  /\  /  __/ |_) |{C.CYAN}| |__| | | |      {C.RESET}
{C.BLUE}      \/  \/ \___|_.__/ {C.CYAN}_____/|_|_|      {C.RESET}
{C.GRAY}          Multi-Threaded Directory Discovery v1.1{C.RESET}
"""

def check_url(directory, base_url):
    """Teste une URL spécifique et affiche le résultat selon le code HTTP."""
    directory = directory.strip()
    if not directory:
        return

    full_url = f"{base_url.rstrip('/')}/{directory}"
    
    try:
        # Affichage discret de la progression (mode verbeux)
        sys.stdout.write(f" {C.GRAY}[*] Scanning: /{directory:<20}{C.RESET}\r")
        sys.stdout.flush()

        # Requête GET sans suivre les redirections pour plus de précision
        response = requests.get(full_url, timeout=3, allow_redirects=False)
        
        if response.status_code == 200:
            print(f"{C.GREEN}[+] 200 OK          : /{directory:<20}{C.RESET}")
        elif response.status_code == 403:
            print(f"{C.YELLOW}[!] 403 Forbidden   : /{directory:<20}{C.RESET}")
        elif response.status_code in [301, 302]:
            location = response.headers.get('Location', 'n/a')
            print(f"{C.BLUE}[>] {response.status_code} Redirect    : /{directory:<20} -> {location}{C.RESET}")
            
    except requests.exceptions.RequestException:
        # On ignore les erreurs individuelles pour ne pas polluer l'affichage
        pass

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Web-Dir Finder Pro")
    parser.add_argument("-u", "--url", required=True, help="URL cible (ex: http://192.168.1.134)")
    parser.add_argument("-w", "--wordlist", required=True, help="Chemin vers la wordlist")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Nombre de threads (défaut: 10)")
    args = parser.parse_args()

    # Nettoyage de l'URL cible
    target_url = args.url
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    print(f" {C.BOLD}[*]{C.RESET} Cible   : {C.YELLOW}{target_url}{C.RESET}")
    print(f" {C.BOLD}[*]{C.RESET} Threads : {C.CYAN}{args.threads}{C.RESET}")
    print(f" {C.BOLD}[*]{C.RESET} Début   : {datetime.now().strftime('%H:%M:%S')}\n")

    try:
        with open(args.wordlist, 'r', encoding='latin-1') as f:
            words = f.readlines()

        print(f" {C.GRAY}[i] Chargement de {len(words)} mots...{C.RESET}\n")

        # Exécution multi-threadée
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
            # On mappe la fonction de test sur chaque mot de la liste
            executor.map(lambda w: check_url(w, target_url), words)

    except FileNotFoundError:
        print(f"{C.RED}[!] Erreur : Le fichier '{args.wordlist}' est introuvable.{C.RESET}")
    except KeyboardInterrupt:
        print(f"\n\n{C.RED}[!] Interruption par l'utilisateur. Sortie...{C.RESET}")
    except Exception as e:
        print(f"\n{C.RED}[!] Erreur imprévue : {e}{C.RESET}")
    
    print(f"\n\n{C.BOLD}[*]{C.RESET} Scan terminé à {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
