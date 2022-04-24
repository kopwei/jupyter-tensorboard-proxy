import os
import shutil
import logging


logger = logging.getLogger(__name__)
logger.setLevel('INFO')


def setup_tensorboard():
    """Setup commands and icon paths and return a dictionary compatible
    with jupyter-server-proxy.
    """
    def _get_icon_path():
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'icons', 'tensorboard.svg'
    )

    def _get_tensorboard_command(port):
        if not shutil.which('tensorboard'):
            raise FileNotFoundError('Cannot find tensorboard executable in $PATH')
        logdir = os.getenv('TENSORBOARD_LOGDIR', os.path.expanduser('~/logs'))
        return ['tensorboard', '--logdir', logdir, '--port', '{port}']
    
    return {
        'command': _get_tensorboard_command,
        'port': 6006,
        'timeout': 20,
        'new_browser_tab': True,
        'launcher_entry': {
            'title': 'Tensorboard',
            'icon_path': _get_icon_path()
        },
    }
