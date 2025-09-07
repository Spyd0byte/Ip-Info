import requests as reqs
import socket, time, sys, os, random, threading
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# ==== CONFIG ====
DELAY = 0.02         # Typing speed
DECODE_SPEED = 0.005 # Decode animation speed
SPINNER_SPEED = 0.1

# ==== UTILITY FUNCTIONS ====
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def type_text(text, color=Fore.WHITE, delay=DELAY):
    """Typing effect for terminal text."""
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Style.RESET_ALL, end="")

def decode_text(text, color=Fore.LIGHTGREEN_EX):
    """Matrix-style decode animation for small text."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*"
    decoded = [" "]*len(text)
    for i in range(len(text)):
        for _ in range(random.randint(3, 7)):
            decoded[i] = random.choice(chars)
            sys.stdout.write("\r" + color + "".join(decoded))
            sys.stdout.flush()
            time.sleep(DECODE_SPEED)
        decoded[i] = text[i]
    sys.stdout.write("\r" + color + "".join(decoded) + "\n")

def spinner(message, stop_event):
    """Loading spinner animation."""
    spinner_chars = ["|", "/", "-", "\\"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Fore.YELLOW}{message} {spinner_chars[i % len(spinner_chars)]}")
        sys.stdout.flush()
        i += 1
        time.sleep(SPINNER_SPEED)
    sys.stdout.write("\r" + " " * (len(message)+5) + "\r")

def show_info(data):
    """Show info in Parrot-style tree hierarchy."""
    print(Fore.LIGHTCYAN_EX + "\n└── IP Info")
    print(Fore.LIGHTCYAN_EX + f"    ├── IP Address : {data.get('ip')}")
    print(f"    ├── City       : {data.get('city')}")
    print(f"    ├── Region     : {data.get('region')}")
    print(f"    ├── Country    : {data.get('country')}")
    print(f"    ├── Location   : {data.get('loc')}")
    print(f"    ├── Postal     : {data.get('postal')}")
    print(f"    └── Time Zone  : {data.get('timezone')}")

# ==== ASCII ART ====
ascii_logo = r"""
██╗██████╗░  ██╗███╗░░██╗███████╗░█████╗░
██║██╔══██╗  ██║████╗░██║██╔════╝██╔══██╗
██║██████╔╝  ██║██╔██╗██║█████╗░░██║░░██║
██║██╔═══╝░  ██║██║╚████║██╔══╝░░██║░░██║
██║██║░░░░░  ██║██║░╚███║██║░░░░░╚█████╔╝
╚═╝╚═╝░░░░░  ╚═╝╚═╝░░╚══╝╚═╝░░░░░░╚════╝░
"""

# ==== MAIN PROGRAM ====
clear()
# Static banner now
print(Fore.LIGHTGREEN_EX + ascii_logo)
decode_text("------  [+] SPYD0BYTE -------", Fore.LIGHTBLUE_EX)
print()

# Check Internet
try:
    socket.gethostbyname("www.google.com")
    type_text("# Internet: Active\n", Fore.LIGHTGREEN_EX)
except:
    type_text("!! No Internet !!\nExiting in 5 seconds...\n", Fore.LIGHTRED_EX)
    time.sleep(5)
    exit()

url = "https://ipinfo.io"
type_text("1. Check your IP info\n", Fore.LIGHTCYAN_EX)
type_text("2. Check someone's IP info\n\n", Fore.LIGHTCYAN_EX)

choice = input(Fore.YELLOW + "Choice (1 or 2) > ")

# Spinner setup
stop_event = threading.Event()

if choice == "1":
    type_text("\n**** Your IP Info ****\n", Fore.LIGHTBLUE_EX)
    spinner_thread = threading.Thread(target=spinner, args=("Fetching data", stop_event))
    spinner_thread.start()
    resp = reqs.get(url)
    stop_event.set()
    spinner_thread.join()
    show_info(resp.json())

elif choice == "2":
    type_text("\n**** Someone's IP Info ****\n", Fore.LIGHTBLUE_EX)
    Sip = input(Fore.YELLOW + "Enter IP address: ")
    spinner_thread = threading.Thread(target=spinner, args=("Fetching data", stop_event))
    spinner_thread.start()
    resp = reqs.get(url + "/" + Sip)
    stop_event.set()
    spinner_thread.join()
    show_info(resp.json())

else:
    type_text("\nInvalid choice, input 1 or 2\n", Fore.LIGHTRED_EX)

input(Fore.LIGHTBLACK_EX + "\nPress Enter to Exit > ")
