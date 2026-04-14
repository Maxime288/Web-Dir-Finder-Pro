#!/usr/bin/env python3
"""
🕷️ Web-Dir Finder Pro
Outil de brute-force de répertoires web pour la reconnaissance.
"""

import requests
import sys
import argparse

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
    GRAY    = "\033[38;5;244m"

BANNER = fr"""
{C.BLUE}  __          __  _      {C.GRAY} _____  _         {C.RESET}
{C.BLUE}  \ \        / / | |    {C.GRAY}|  __ \(_)        {C.RESET}
{C.BLUE}   \ \  /\  / /__| |__  {C.GRAY}| |  | |_ _ __    {C.RESET}
{C.BLUE}    \ \/  \/ / _ \ '_ \ {C.GRAY}| |  | | | '__|   {C.RESET}
{C.BLUE}     \  /\  /  __/ |_) |{C.GRAY}| |__| | | |      {C.RESET}
{C.BLUE}      \/  \/ \___|_.__/ {C.GRAY}|_____/|_|_|      {C.RESET}
{C.GRAY}          Professional Directory Discovery v1.0{C.RESET}
"""

def brute_force(url, wordlist):
    print(f" {C.BOLD}[*]{C.RESET} Cible : {C.YELLOW}{url}{C.RESET}")
    print(f" {C.BOLD}[*]{C.RESET} Analyse en cours...\n")
    
    try:
        with open(wordlist, 'r') as file:
            for line in file:
                directory = line.strip()
                full_url = f"{url.rstrip('/')}/{directory}"
                
                try:
                    response = requests.get(full_url, timeout=2)
                    
                    # Interprétation des codes de statut
                    if response.status_code == 200:
                        print(f" {C.GREEN}[+] TROUVÉ (200) : /{directory}{C.RESET}")
                    elif response.status_code == 403:
                        print(f" {C.YELLOW}[!] INTERDIT (403) : /{directory}{C.RESET}")
                    elif response.status_code == 301 or response.status_code == 302:
                        print(f" {C.BLUE}[>] REDIRECTION ({response.status_code}) : /{directory}{C.RESET}")
                        
                except requests.exceptions.RequestException:
                    continue # On ignore les erreurs de connexion individuelles

    except FileNotFoundError:
        print(f"{C.RED}[!] Erreur : Wordlist '{wordlist}' introuvable.{C.RESET}")

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Bruteforceur de répertoires web")
    parser.add_argument("-u", "--url", required=True, help="URL cible (ex: http://192.168.1.1)")
    parser.add_argument("-w", "--wordlist", required=True, help="Chemin vers la wordlist (ex: common.txt)")
    args = parser.parse_args()

    brute_force(args.url, args.wordlist)

if __name__ == "__main__":
    main()
