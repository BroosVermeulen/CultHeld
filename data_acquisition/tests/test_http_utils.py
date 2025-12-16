import sys
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import gzip
import zlib
import json

from utils.http_utils import safe_json


class FakeResp:
    def __init__(self, content: bytes, url='http://example', status_code=200):
        self.content = content
        self.url = url
        self.status_code = status_code

    def json(self):
        raise ValueError('no json')


def test_safe_json_gzip():
    payload = json.dumps({'ok': True}).encode('utf-8')
    gz = gzip.compress(payload)
    resp = FakeResp(gz)
    data = safe_json(resp)
    assert data.get('ok') is True


def test_safe_json_zlib():
    payload = json.dumps({'n': 1}).encode('utf-8')
    z = zlib.compress(payload)
    resp = FakeResp(z)
    data = safe_json(resp)
    assert data.get('n') == 1
