# DolibabyPhp

An authenticated RCE exploit for Dolibarr ERP/CRM CVE-2023-30253.

## Installation

???

## Usage

```txt
Usage: python -m dolibabyphp [OPTIONS] TARGET_URL USERNAME PASSWORD COMMAND
                             [ARGS]...

  This exploit will log into the Dolibarr web server at the specified target URL
  with the provided username and password. After that it will attempt to create
  a web page with a unique name. Once created, it will modify the web page to
  include the custom PHP code bypassing the sanitation check by not using only
  lowercase letters (e.g. PHP or pHp instead of php). There are multiple
  payloads to choose from After the payload has finished running, the web page
  will be deleted.

Options:
  --help  Show this message and exit.

Commands:
  bash-reverse-shell     Spawns a bash shell on the victim machine and...
  custom-php-payload     Specify your own PHP payload to be run on the victim...
  custom-system-payload  Specify your own payload to be run via PHP system()...
  sftp                   SFTPs to the attacker machine, downloads the...
  wget                   Downloads the file at the specified URL to to the...
```

## Running from source

In order to run the project from the source code, make sure you add the `src/` directory to the `PYTHONPATH` and then import the module `dolibabyphp` with the `-m` flag.

```shell
PYTHONPATH="$(pwd)/src/" python -m dolibabyphp
```
