import sys
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
from staging.fchyena import _parse_shows_from_html


SAMPLE_HTML = b'''<html><body>
<div class="show">
  <a href="/show/1">Details</a>
  <time datetime="2025-12-20T20:00:00+01:00">20 Dec 20:00</time>
</div>
<div class="show">
  <a href="/show/2">Details</a>
  <time>21 Dec 20:00</time>
</div>
</body></html>'''


def test_parse_shows_from_html():
    df = _parse_shows_from_html(SAMPLE_HTML)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert 'start_date_time' in df.columns
    assert df['ticket_url'].iloc[0].endswith('/show/1')
