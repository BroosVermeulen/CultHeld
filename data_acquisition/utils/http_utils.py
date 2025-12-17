import json
import time
import logging
from typing import Optional, Dict, Any
import requests

logger = logging.getLogger(__name__)


def safe_request(method: str, url: str, *, headers: Optional[Dict[str, str]] = None,
                 params: Optional[Dict[str, Any]] = None, data: Optional[Any] = None,
                 json_body: Optional[Any] = None, retries: int = 3, backoff: float = 1.0,
                 timeout: float = 10.0) -> requests.Response:
    """Perform an HTTP request with retries and exponential backoff.

    Returns the final requests.Response (may be non-200). Raises the last exception
    only if all retries fail due to network errors.
    """
    last_exc = None
    # Ensure a friendly default User-Agent to reduce blocks by some servers
    hdrs = dict(headers or {})
    if not any(k.lower() == "user-agent" for k in hdrs.keys()):
        hdrs["User-Agent"] = "CultHeldDataAcquisition/1.0 (+https://github.com/ambrosiusvermeulen)"
    for attempt in range(1, retries + 1):
        try:
            resp = requests.request(method, url, headers=hdrs, params=params, data=data, json=json_body, timeout=timeout)
            return resp
        except requests.RequestException as e:
            last_exc = e
            wait = backoff * (2 ** (attempt - 1))
            logger.warning("HTTP %s to %s failed on attempt %d/%d: %s — retrying in %.1fs", method, url, attempt, retries, e, wait)
            time.sleep(wait)
    # If we get here, all retries failed
    logger.error("All retries failed for %s %s: %s", method, url, last_exc)
    raise last_exc


def safe_get(url: str, **kwargs) -> requests.Response:
    return safe_request("GET", url, **kwargs)


def safe_post(url: str, **kwargs) -> requests.Response:
    return safe_request("POST", url, **kwargs)


def safe_json(resp: requests.Response) -> Any:
    """Parse response as JSON with defensive fallbacks and logging.

    - Tries resp.json() first.
    - Falls back to decoding resp.content as UTF-8 (with ignore) and json.loads.
    - If parsing still fails, logs a snippet of the raw content and raises ValueError.
    """
    try:
        return resp.json()
    except Exception as e:
        # Try tolerant fallbacks including common compression encodings
        raw = None
        try:
            raw = resp.content
        except Exception:
            raw = None

        # 1) try to decode as utf-8
        if isinstance(raw, (bytes, bytearray)):
            try:
                text = raw.decode('utf-8')
                return json.loads(text)
            except Exception:
                pass

            # 2) try gzip
            try:
                import gzip
                text = gzip.decompress(raw).decode('utf-8')
                logger.debug('Decoded response via gzip.decompress for %s', getattr(resp, 'url', '<unknown>'))
                return json.loads(text)
            except Exception:
                pass

            # 3) try brotli (br)
            try:
                import brotli
                text = brotli.decompress(raw).decode('utf-8')
                logger.debug('Decoded response via brotli.decompress for %s', getattr(resp, 'url', '<unknown>'))
                return json.loads(text)
            except Exception:
                pass

            # 4) try zlib
            try:
                import zlib
                text = zlib.decompress(raw).decode('utf-8')
                logger.debug('Decoded response via zlib.decompress for %s', getattr(resp, 'url', '<unknown>'))
                return json.loads(text)
            except Exception:
                pass

        # last attempt: coerce to str and parse
        try:
            text = str(raw)
            return json.loads(text)
        except Exception as e2:
            snippet = None
            try:
                snippet = (resp.content[:1024] if hasattr(resp, 'content') else str(resp))
            except Exception:
                snippet = str(resp)[:1024]
            logger.error("Failed to parse JSON response from %s; resp.status=%s; snippet=%s; errors: %s | %s",
                         getattr(resp, 'url', '<unknown>'), getattr(resp, 'status_code', '<no-status>'), snippet, e, e2)
            raise ValueError("Invalid JSON response") from e2
