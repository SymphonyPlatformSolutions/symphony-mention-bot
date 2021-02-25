from appbase.botloader.config import _config
import logging.config
import sys, os
from datetime import datetime

level_str = _config['LOG_LEVEL']
my_level = str(level_str)

### To log to STDERR
logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w', level=my_level
)
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)
stderr_handler.setFormatter(formatter)

logger.addHandler(stderr_handler)
logging.getLogger("urllib3").setLevel(logging.WARNING)

### To logs to file
#
# now = datetime.now()
# dt = now.strftime("%d-%m-%Y-%H-%M-%S")
#
# log_dir = os.path.join(os.path.dirname(__file__), "../logs")
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir, exist_ok=True)
#
# logging.basicConfig(
#         filename=os.path.join(log_dir, 'MirrorBot-' + dt +'.log'),
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#         filemode='w', level=my_level
# )
# logging.getLogger("urllib3").setLevel(logging.WARNING)