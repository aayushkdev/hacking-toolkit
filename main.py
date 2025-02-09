from utils.utils import *
import curses
import curses.textpad
from passwordcrack.passwordcrack import dictionaryAttack, bruteforceAttack


def main_menu(stdscr):
    """Main menu with all tools listed."""
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    stdscr.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # Red highlight

    current_row = 0

    while 1:
        draw_menu(stdscr, main_menu_items, current_row)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(main_menu_items) - 1:
            current_row += 1
        elif key == 10: 
            if current_row == 0:
                password_menu(stdscr)  
            elif current_row == 1:
                stdscr.clear()
                stdscr.addstr(5, 5, "Network Scanning selected...")  
                stdscr.refresh()
                stdscr.getch()
            elif current_row == 2:
                stdscr.clear()
                stdscr.addstr(5, 5, "ARP Poisoning selected...")  
                stdscr.refresh()
                stdscr.getch()
            elif current_row == 3:
                break  

def password_menu(stdscr):
    """Password cracking submenu."""
    current_row = 0

    while 1:
        draw_menu(stdscr, password_menu_items, current_row)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(password_menu_items) - 1:
            current_row += 1
        elif key == 10: 
            if current_row == 0:
                return
            elif current_row == 1:
                bruteforceAttack(stdscr)
                stdscr.addstr(11, 2, "Press any key to return...", curses.A_DIM)
                stdscr.getch()
            elif current_row == 2:
                dictionaryAttack(stdscr)
                stdscr.addstr(25, 2, "Press any key to return...", curses.A_DIM)
                stdscr.nodelay(False)
                stdscr.getch()


def main():
    """Start the curses-based UI."""
    try:
        curses.wrapper(main_menu)
    except KeyboardInterrupt:
        print("Exiting...")
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()