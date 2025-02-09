import os
import curses


main_menu_items = ["Cracking Passwords", "Network Scanning", "ARP Poisoning", "Exit"]

password_menu_items = ["Back", "Bruteforce Attack", "Dictionary Attack"]

dictionary_menu_items = ["Back", "Enter the hash:", "Enter wordlist location (default: /usr/share/wordlists/rockyou.txt): ", "Crack"]


def draw_menu(stdscr, menu_items, selected_row, extra_content=None):
    """Function for creating a menus"""
    stdscr.clear()
    h, w = stdscr.getmaxyx() 


    stdscr.addstr(1, 2, "Hacking Toolkit", curses.A_BOLD)

    for idx, item in enumerate(menu_items):
        x = 2  
        y = 3 + idx  

        if idx == selected_row:
            stdscr.attron(curses.color_pair(1) | curses.A_BOLD) 
            stdscr.addstr(y, x, f"> {item}")  
            stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
        else:
            stdscr.addstr(y, x, f"  {item}") 

    if extra_content:
        for line in extra_content:
            line_y, line_x, text = line
            if line_y < h and line_x < w:
                stdscr.addstr(line_y, line_x, text, curses.A_BOLD)

    stdscr.refresh()

def get_text_input(stdscr, y, x, initial_text=""):
    """Uses a curses textbox to handle input interactively."""
    win = curses.newwin(1, 100, y, x)  
    box = curses.textpad.Textbox(win)
    win.addstr(0, 0, initial_text)  
    stdscr.refresh()
    
    curses.curs_set(1)  
    text = box.edit().strip()  
    curses.curs_set(0) 

    return text



def draw_progress_bar(stdscr, y, x, percent):
    """Draws a horizontal progress bar."""
    bar_length = 50  
    filled_length = int(bar_length * percent)  
    bar = "█" * filled_length + "-" * (bar_length - filled_length) 
    stdscr.addstr(y, x, f"[{bar}] {percent*100:.2f}%", curses.A_BOLD)
    stdscr.refresh()