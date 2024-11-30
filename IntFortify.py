import os
import subprocess
import shutil
import pyfiglet


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    clear_screen()
    terminal_width = shutil.get_terminal_size().columns
    ascii_art = pyfiglet.figlet_format("IntFortify", font="slant").splitlines()
    for line in ascii_art:
        half_index = len(line) // 2
        print("\033[38;5;208m" + line[:half_index] + "\033[38;5;196m" + line[half_index:] + "\033[0m")
    print("\033[38;5;208m" + "By: Abelardieu".center(terminal_width) + "\033[0m")
    description = "A program to map your exposed technology easily and fortify your servers."
    print("\033[38;5;231m" + description.center(terminal_width) + "\033[0m\n")


def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")


def nmap_scan(level, target):
    print(f"\n[+] Running Nmap Level {level} scan on {target}")
    commands = {
        "1": f"nmap -sV -T1 -f -Pn {target}",
        "2": f"nmap -sS -T2 -Pn {target}",
        "3": f"nmap -sV -T3 {target}",
        "4": f"nmap -sC -sV -T4 {target}",
        "5": f"nmap -A -sV -T5 {target}",
    }
    run_command(commands[level])


def sslyze_scan(level, target):
    print(f"\n[+] Running SSLyze Level {level} scan on {target}")
    commands = {
        "1": f"sslyze --regular {target}",
        "2": f"sslyze --certinfo {target}",
        "3": f"sslyze --certinfo --elliptic_curves {target}",
        "4": f"sslyze --certinfo --elliptic_curves --compression {target}",
        "5": f"sslyze --certinfo --elliptic_curves --compression --reneg --heartbleed {target}",
    }
    run_command(commands[level])


def nikto_scan(target):
    print(f"\n[+] Running Nikto scan on {target}")
    ports = [443, 8443]
    for port in ports:
        print(f"\nScanning port {port}...")
        command = f"nikto -h {target} -p {port}"
        run_command(command)


def whois_lookup(target):
    print(f"\n[+] Running WHOIS lookup on {target}")
    try:
        if os.name == 'nt':
            command = f"whois.exe {target}"
        else:
            command = f"whois {target}"
        run_command(command)
    except FileNotFoundError:
        print("\n[!] WHOIS command not found. Please install the 'whois' tool.")
    except Exception as e:
        print(f"\n[!] Error running WHOIS: {e}")


def display_menu():
    print("\n=== Main Menu ===")
    print("1. Ghost (Basic scans with Nmap and SSLyze)")
    print("2. Stealth (Moderate scans with Nmap and SSLyze)")
    print("3. Normal (Balanced scans with Nmap, SSLyze, and Nikto)")
    print("4. Desperate (Aggressive scans with all tools)")
    print("5. Demon (Maximum detail with all tools)")
    print("6. WHOIS Lookup")
    print("7. Exit")
    return input("\nSelect an option: ")


def main():
    print_header()
    target = input("Enter the target (IP or URL): ").strip()
    if not target:
        print("Invalid input. Exiting.")
        return

    while True:
        print_header()
        option = display_menu()
        clear_screen()
        print_header()

        if option in {"1", "2", "3", "4", "5"}:
            nmap_scan(option, target)
            sslyze_scan(option, target)
            if option in {"3", "4", "5"}:
                nikto_scan(target)
        elif option == "6":
            whois_lookup(target)
        elif option == "7":
            print("Exiting IntFortify. Stay safe!")
            break
        else:
            print("Invalid option. Please try again.")
        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main()
