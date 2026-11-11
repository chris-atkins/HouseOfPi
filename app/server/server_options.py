import re
from dataclasses import dataclass
from typing import Mapping, Optional, Tuple

# Relative to the working directory: the deploy job copies the cert and key into the app directory.
SSL_CONTEXT = ('cert.crt', 'key.key')

DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 5000


@dataclass(frozen=True)
class ServerOptions:
    host: str
    port: int
    ssl_context: Optional[Tuple[str, str]]
    debug: bool


def server_options_from_env(environ: Mapping[str, str]) -> ServerOptions:
    return ServerOptions(
        host=(environ.get('PYTHON_HOST') or '').strip() or DEFAULT_HOST,
        port=_parse_port(environ.get('PYTHON_PORT')),
        ssl_context=SSL_CONTEXT if _is_on(environ.get('PYTHON_SSL_ON')) else None,
        debug=_is_on(environ.get('PYTHON_DEBUG_ON')),
    )


def _is_on(value: Optional[str]) -> bool:
    return value is not None and value.strip().lower() in ('true', 'yes')


def _parse_port(value: Optional[str]) -> int:
    if value is None or value.strip() == '':
        return DEFAULT_PORT
    # Plain ASCII digits only: int() would also accept '+5001', '5_001' and non-ASCII digits.
    if not re.fullmatch(r'[0-9]+', value.strip()):
        raise ValueError(f'PYTHON_PORT must be an integer, got {value!r}')
    port = int(value)
    if not 1 <= port <= 65535:
        raise ValueError(f'PYTHON_PORT must be between 1 and 65535, got {port}')
    return port
