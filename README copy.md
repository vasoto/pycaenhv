# pycaenhv - Pure Python Bindings for CAENHVWrapper

This package provides access to all the CAENHVWrapper functionality in pure Python, no compilation needed.

## Install
1. Download latest version of CAENHVWrapper
2. Install pycaenhv: `pip install -U .`

## Usage

There are two ways to use the module - direct functions or high level classes

### Functions Approach

```python
import pycaenhv as hv

hv.init_system()
hv.ramp_up(channel=1, )
hv.deinit_system()
```

### Classes Approach

```python
from pycanehv import HVBoard, HVChannel

board = HVBoard() # initialize
channel = HVChannel(board, 1)
channel.ramp_up()

print(channel)
print(channel.name)
channel.stop()

```


