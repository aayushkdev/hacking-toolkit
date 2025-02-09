import hashlib
import re
from utils.utils import *
import curses
import time


def detectHash(hash_value):
    """Detects the type of hash based on its pattern and length."""
    hash_types = {
        "md5": r"^[a-f0-9]{32}$",
        "sha1": r"^[a-f0-9]{40}$",
        "sha256": r"^[a-f0-9]{64}$",
        "sha512": r"^[a-f0-9]{128}$",
        "ntlm": r"^[a-f0-9]{32}$",
        "bcrypt": r"^\$2[ayb]\$.{56}$",
        "Argon2": r"^\$argon2[id]\$.{30,}$",
        "sha3-256": r"^[a-f0-9]{64}$",
        "sha3-512": r"^[a-f0-9]{128}$",
    }

    for algo, pattern in hash_types.items():
        if re.match(pattern, hash_value, re.IGNORECASE):
            return algo
    return False

def dictionaryCrackHash(stdscr, hash_value, hash_type, wordlist_file):

    stdscr.nodelay(True) 

    try:
        with open(wordlist_file, "r", encoding="utf-8", errors="ignore", buffering=65536) as file:
            wordlist = file.readlines()
            total_words = len(wordlist)

            stdscr.addstr(10, 2, "Dictionary Attack in Progress", curses.A_BOLD)
            stdscr.addstr(11, 2, "Press 'q' to exit...", curses.A_DIM)


            for index, word in enumerate(wordlist):
                word = word.strip()

                stdscr.move(14, 2)  
                stdscr.clrtoeol() 
                stdscr.addstr(14, 2, f"Trying: {word}...", curses.A_BOLD)

                percent = (index + 1) / total_words
                draw_progress_bar(stdscr, 16, 2, percent)  

                stdscr.refresh()


                hashed_word = hashlib.new(hash_type, word.encode()).hexdigest()
                if hashed_word == hash_value:
                    stdscr.addstr(23, 2, f"[✔] Password found: {word}", curses.A_BOLD)
                    stdscr.refresh()
                    return True
                
                key = stdscr.getch()
                if key == ord('q'):  
                    stdscr.nodelay(False)  
                    return False

            stdscr.addstr(31, 2, "[✘] Password not found in wordlist.", curses.A_BOLD)
            stdscr.refresh()
            return False
    
    except FileNotFoundError:
        stdscr.addstr(10, 2, "[!] Wordlist file not found!", curses.A_BOLD)
        stdscr.refresh()
        return False
    

def dictionaryAttack(stdscr):
    stdscr.clear()

    current_row = 0
    hash_input = ""
    wordlist = ""

    while 1:
        extra_content = [
            (4, 20, hash_input), 
            (5, 73, wordlist) 
        ]

        draw_menu(stdscr, dictionary_menu_items, current_row, extra_content)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1

        elif key == curses.KEY_DOWN and current_row < len(dictionary_menu_items) - 1:
            current_row += 1

        elif key == 10: 
            if current_row == 0:
                return
            
            elif current_row == 1: 
                hash_input = get_text_input(stdscr, 4, 20, hash_input)

            elif current_row == 2:  
                wordlist = get_text_input(stdscr, 5, 73, wordlist)

            elif current_row == 3:
                break

    if not wordlist:
        wordlist = "/usr/share/wordlists/rockYou.txt" 

    detected_type = detectHash(hash_input)

    if not detected_type:
        stdscr.addstr(8, 2, "[✘] Unknown hash type detected", curses.A_BOLD)
        return False
    stdscr.addstr(8, 2, f"[✔] Detected Hash Type: {detected_type}", curses.A_BOLD)

    if detected_type in hashlib.algorithms_available:
        dictionaryCrackHash(stdscr, hash_input, detected_type, wordlist)
    else:
        stdscr.addstr(9, 2, f"[✘] Cracking not supported for the detected hash type: {detected_type}", curses.A_BOLD)
        return False



def bruteforceAttack(stdscr):
    pass

    