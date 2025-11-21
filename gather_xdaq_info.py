from pyxdaq.xdaq import get_XDAQ
from pathlib import Path
import json
import shutil
result_dir = Path("results")
if result_dir.exists():
    shutil.rmtree(result_dir)
result_dir.mkdir()
xdaq = get_XDAQ(rhs=False, skip_headstage=True)
print(xdaq.dev.status, xdaq.dev.info)
(result_dir / "status.json").write_text(json.dumps(xdaq.dev.status))
(result_dir / "info.json").write_text(json.dumps(xdaq.dev.info))
xdaq.enableDataStream('all', True, True)
for delay in range(8):
    xdaq.setCableDelay('all', delay)
    (result_dir / f'raw_{delay}.bin').write_bytes(xdaq.runAndReadBuffer(128))
shutil.make_archive('results', 'zip', result_dir)
