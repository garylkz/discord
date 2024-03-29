from importlib import import_module
import json
import logging
import os
from pathlib import Path
import random
import subprocess
import tempfile
import textwrap
import time
from typing import List, Tuple
from urllib.request import urlopen

import requests


def rand_int_str() -> str:
    return str(random.random())[2:]


def basename(path: str) -> str:
    return path.split('/')[-1].split('.')[0]


def list_attrs(obj: object, attrs: List[str]) -> str:
    return '\n'.join([f'{a}: {getattr(obj, a)}' for a in attrs])


def clamp(i: int, *, min_i: int = 1, max_i: int = 100) -> int:
    return min(max(i, min_i), max_i)


def load_env(path: str = 'creds.json') -> None:
    envs = json.load(open(path))
    os.environ.update(envs)


def wrap(text: str, *, width: int = 4000, lang: str = None) -> List[str]:
    ls = textwrap.wrap(text, width, replace_whitespace=False)
    return [f'```{lang}\n{s}```' for s in ls] or ['None']


# TODO: Better alternative
def subprocess_log(args: List[str], inp: str = None) -> Tuple[str, float]:
    with tempfile.TemporaryFile('r+t') as fp:
        t = time.time()
        subprocess.run(
            args=args, input=inp, stdout=fp, stderr=subprocess.STDOUT
        )
        dt = time.time() - t
        fp.seek(0)
        return fp.read(), dt


def send_embeds(chn_id: int, chunks: List[str], **fields) -> requests.Response:
    return requests.post(
        f'https://discord.com/api/v9/channels/{chn_id}/messages',
        headers={'Authorization': f'Bot {os.environ["TOKEN"]}'},
        json={'embeds': [{**{'description': c}, **fields} for c in chunks]}
        # json={'embeds': [{'description': c} | fields for c in chunks]} #3.9
    )


def error_log(e: Exception, chn_id: int) -> requests.Response:
    logging.exception(e)
    return chn_id and send_embeds(
        chn_id, wrap(str(e), lang='bash'),
        title=type(e).__name__, color=0xe74c3c
    )


def load_data(**init) -> dict:
    try:
        data = json.load(open('data.json'))
    except FileNotFoundError:
        data = {}
    init.update(data)
    save_data(init)
    return init


def save_data(data: dict, **update) -> None:
    update.update(data)
    json.dump(update, open('data.json', 'w'))


def import_url(url: str, *, path: str = 'modules', name: str = None):
    script = str(urlopen(url).read().decode())
    _path = Path(path)
    _path.mkdir(parents=True, exist_ok=True)
    name = name or basename(url)
    _file = _path / (f'{name}.py')
    _file.write_text(script)
    package = path.replace('/', '.')
    return import_module(f'.{name}', package)
