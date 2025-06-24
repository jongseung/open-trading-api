from pathlib import Path


def load_env(path: str = ".env") -> dict:
    """Load key=value pairs from a .env file."""
    env = {}
    p = Path(path)
    if not p.exists():
        return env
    with p.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env


def apply_to_kis_api(env: dict):
    """Apply environment values to rest.kis_api module."""
    import rest.kis_api as kis_api

    if env:
        kis_api._cfg = env
        if 'my_agent' in env:
            kis_api._base_headers['User-Agent'] = env['my_agent']

