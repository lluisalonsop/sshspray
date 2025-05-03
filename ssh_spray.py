import argparse
import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException
import socket
from termcolor import colored  # Import termcolor for colored output

def try_password_auth(ip, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=username, password=password, timeout=5)
        print(colored(f"[✓] Success (password) on {ip}", "green"))
        client.close()
    except (AuthenticationException, SSHException, socket.error) as e:
        print(colored(f"[✗] Failed (password) on {ip}: {e}", "red"))

def try_key_auth(ip, port, username, key_path, passphrase):
    try:
        key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
    except paramiko.PasswordRequiredException:
        print(colored(f"[!] Key requires a passphrase but none was provided: {key_path}", "yellow"))
        return
    except paramiko.SSHException:
        try:
            key = paramiko.ECDSAKey.from_private_key_file(key_path, password=passphrase)
        except Exception as e:
            print(colored(f"[!] Failed to load key: {e}", "yellow"))
            return

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=username, pkey=key, timeout=5)
        print(colored(f"[✓] Success (key) on {ip}", "green"))
        client.close()
    except (AuthenticationException, SSHException, socket.error) as e:
        print(colored(f"[✗] Failed (key) on {ip}: {e}", "red"))

def main():
    parser = argparse.ArgumentParser(description="SSH multi-host checker with password or private key authentication")
    parser.add_argument('--hosts', required=True, help='File containing list of IPs/hosts')
    parser.add_argument('-p', '--port', type=int, default=22, help='SSH port (default: 22)')
    parser.add_argument('-u', '--username', required=True, help='SSH username')
    parser.add_argument('-P', '--password', help='Password for password-based authentication')
    parser.add_argument('-i', '--identity', help='Private key file (like ssh -i)')
    parser.add_argument('--passphrase', help='Passphrase for the private key (if encrypted)')

    args = parser.parse_args()

    with open(args.hosts) as f:
        hosts = [line.strip() for line in f if line.strip()]

    for ip in hosts:
        if args.password:
            try_password_auth(ip, args.port, args.username, args.password)
        elif args.identity:
            try_key_auth(ip, args.port, args.username, args.identity, args.passphrase)
        else:
            print(colored("[-] You must provide either a --password or a private key with -i", "yellow"))

if __name__ == "__main__":
    main()
