from .cyton import OpenBCICyton
from .plugins import *
from .utils import *
#from .wifi import OpenBCIWiFi
import sys
if sys.platform.startswith("linux"):
    from .ganglion import OpenBCIGanglion
