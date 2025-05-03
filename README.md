# SSH Multi-Host Checker

This Python script allows you to perform SSH authentication checks on multiple hosts using either password-based or private key-based authentication. It supports custom SSH ports and allows you to provide a passphrase if your private key is encrypted. The output is colored for easy interpretation: **green** for success and **red** for failure.

## Usage

### 1. Install dependencies

You need to install the required Python package for colored output.

```bash
pip install termcolor
```
### 2. Run the script
```bash
ssh_spray.py [-h] --hosts HOSTS [-p PORT] -u USERNAME [-P PASSWORD] [-i IDENTITY] [--passphrase PASSPHRASE]

SSH multi-host checker with password or private key authentication

optional arguments:
  -h, --help            show this help message and exit
  --hosts HOSTS         File containing list of IPs/hosts
  -p PORT, --port PORT  SSH port (default: 22)
  -u USERNAME, --username USERNAME
                        SSH username
  -P PASSWORD, --password PASSWORD
                        Password for password-based authentication
  -i IDENTITY, --identity IDENTITY
                        Private key file (like ssh -i)
  --passphrase PASSPHRASE
                        Passphrase for the private key (if encrypted)
```
### 3. Examples
1. Private key authentication (with passphrase):
```bash
python3 ssh_spray.py --hosts hosts.txt -u user -i ./id_rsa --passphrase test -p 2222
```
2. Password authentication:
```bash
python3 ssh_spray.py --hosts hosts.txt -u user -P test -p 22
```