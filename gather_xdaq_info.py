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
for run in range(5):
    for delay in range(8):
        xdaq.setCableDelay('all', delay)
        (result_dir / f'rhd_raw_{delay}_{run}.bin').write_bytes(xdaq.runAndReadBuffer(128))

del xdaq

xdaq = get_XDAQ(rhs=True, skip_headstage=True)
xdaq.enableDataStream('all', True, True)
for run in range(5):
    for delay in range(8):
        xdaq.setCableDelay('all', delay)
        (result_dir / f'rhs_raw_{delay}_{run}.bin').write_bytes(xdaq.runAndReadBuffer(128))

shutil.make_archive('results', 'zip', result_dir)
print("Results saved to results.zip")

try:
    print()
    del xdaq
    xdaq = get_XDAQ(rhs=False)
    for p, stream_on_port in enumerate(xdaq.ports.group_by_port()):
        if any([i.available for i in stream_on_port]):
            print(f'Port {p+1} X3R/X6R detected')
        else:
            print(f'Port {p+1} N/A')

except Exception as e:
    pass

try:
    print()
    del xdaq
    xdaq = get_XDAQ(rhs=True)
    for p, stream_on_port in enumerate(xdaq.ports.group_by_port()):
        if any([i.available for i in stream_on_port]):
            print(f'Port {p+1} X3SR detected')
        else:
            print(f'Port {p+1} N/A')

except Exception as e:
    pass
