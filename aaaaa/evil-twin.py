import os
import sys
from colorama import Fore
from rich.console import Console
from rich.table import Table

ATTACK = '1'
DEFENCE = '2'

if __name__ == '__main__':
    os.system('figlet Evil Twin Tool')
    os.system('echo Build by Eyal Levi, Rotem Halbreich, and Moshe Crespin')
    if os.geteuid():
        sys.exit("lease run as root user , use sudo command! Exiting....")

    table = Table(title="Tasks list")

    table.add_column("Opt", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")

    table.add_row("1", "Perform Evil Twin Attack")
    table.add_row("2", "Perform Defence on Evil Twin Attack")

    con = Console()
    con.print(table)
    con.print("Please choose an option:")

    while True:
        user_input = input()
        if user_input == ATTACK:
            os.system('sudo python3 attack/wifi_attack.py')
            break
        elif user_input == DEFENCE:
            os.system('sudo python3 defence/defence.py')
            break

        else:
            print(Fore.RED, 'Not a valid option please , Please try again.')