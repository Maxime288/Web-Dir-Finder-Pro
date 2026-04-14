#!/usr/bin/env python3
"""
🕷️ Web-Dir Finder Pro v1.2 (Stealth Edition)
Outil de brute-force de répertoires avec rotation d'User-Agents et délais.
"""

import requests
import argparse
import concurrent.futures
import time
import random
import sys
from datetime import datetime

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
{C.GRAY}          Stealth Multi-Threaded Discovery v1.2{C.RESET}
"""

# Liste d'identités pour tromper le WAF
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
]

def check_url(directory, base_url, delay):
    """Teste une URL avec furtivité."""
    directory = directory.strip()
    if not directory: return

    # Simulation d'un comportement humain : petit délai aléatoire
    if delay > 0:
        time.sleep(random.uniform(0, delay))

    full_url = f"{base_url.rstrip('/')}/{directory}"
    
    # Rotation de l'User-Agent
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    
    try:
        sys.stdout.write(f" {C.GRAY}[*] Scanning: /{directory:<20}{C.RESET}\r")
        sys.stdout.flush()

        # Requête furtive
        response = requests.get(full_url, headers=headers, timeout=5, allow_redirects=False)
        
        if response.status_code == 200:
            print(f"{C.GREEN}[+] 200 OK          : /{directory:<20}{C.RESET}")
        elif response.status_code == 403:
            print(f"{C.YELLOW}[!] 403 Forbidden   : /{directory:<20}{C.RESET}")
        elif response.status_code in [301, 302]:
            print(f"{C.BLUE}[>] {response.status_code} Redirect    : /{directory:<20}{C.RESET}")
            
    except Exception:
        pass

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Web-Dir Finder Pro - Stealth Edition")
    parser.add_argument("-u", "--url", required=True, help="URL cible")
    parser.add_argument("-w", "--wordlist", required=True, help="Wordlist")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Threads (défaut: 5 pour la discrétion)")
    parser.add_argument("-d", "--delay", type=float, default=0, help="Délai max entre requêtes (ex: 0.5)")
    args = parser.parse_args()

    target_url = args.url if args.url.startswith('http') else 'http://' + args.url

    print(f" {C.BOLD}[*]{C.RESET} Cible   : {C.YELLOW}{target_url}{C.RESET}")
    print(f" {C.BOLD}[*]{C.RESET} Mode    : {C.CYAN}Stealth (Random User-Agents){C.RESET}")
    if args.delay > 0:
        print(f" {C.BOLD}[*]{C.RESET} Delay   : {C.CYAN}0-{args.delay}s{C.RESET}")
    print(f" {C.BOLD}[*]{C.RESET} Début   : {datetime.now().strftime('%H:%M:%S')}\n")

    try:
        with open(args.wordlist, 'r', encoding='latin-1') as f:
            words = f.readlines()

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
            executor.map(lambda w: check_url(w, target_url, args.delay), words)

    except FileNotFoundError:
        print(f"{C.RED}[!] Wordlist introuvable.{C.RESET}")
    except KeyboardInterrupt:
        print(f"\n{C.RED}[!] Interruption.{C.RESET}")
    
    print(f"\n\n{C.BOLD}[*]{C.RESET} Scan terminé.")

if __name__ == "__main__":
    main()
