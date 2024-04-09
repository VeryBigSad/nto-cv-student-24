import logging
import os
import sys
from dotenv import load_dotenv
from pydantic import ValidationError
from configs.env_configs_models import EnvConfigsModel
from core.wlui.formatter import formatter as wlui_formatter
from core.wlui.l_filter import WLUIFilter


root_logger = logging.getLogger()

if root_logger.handlers:
    root_logger.removeHandler(*root_logger.handlers)

# This flag available only in production enviroment
is_prod = os.environ.get("PROD_MODE") in [1, True, "true", "True"]


if is_prod:
    root_logger.setLevel(logging.INFO)
else:
    root_logger.setLevel(logging.INFO)
    load_dotenv(dotenv_path=os.path.join("configs", ".env"))


if root_logger.handlers:
    root_logger.removeHandler(*root_logger.handlers)

consoleHandler = logging.StreamHandler()
consoleHandler.addFilter(WLUIFilter())
consoleHandler.setFormatter(wlui_formatter)

root_logger.addHandler(consoleHandler)
root_logger.setLevel(logging.INFO)
_logger = logging.getLogger(__name__)

try:
    env_parameters = EnvConfigsModel(**os.environ)
except ValidationError as e:
    _logger.critical(exc_info=e, msg="Env parameters validation")
    sys.exit(-1)
env_parameters.PROD_MODE = is_prod

if env_parameters.PROD_MODE:
    _logger.info("Start in production mode")
else:
    _logger.info("Start in develop mode")
