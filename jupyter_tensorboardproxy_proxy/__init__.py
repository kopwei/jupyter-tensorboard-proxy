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

    # Make sure executable is in $PATH
    def _get_tensorboard_command(port):
        executable = shutil.which('tensorboard')
        if not executable:
            raise FileNotFoundError('Can not find tensorboard executable in $PATH')
        # Create theia working directory
        home_dir = os.environ.get('HOME') or '/home/jovyan'
        working_dir = f'{home_dir}'
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
            logger.info("Created directory %s" % working_dir)
        else:    
            logger.info("Directory %s already exists" % working_dir)
        return ['tensorboard']
    
    return {
        'command': '_get_tensorboard_command',
        'timeout': 20,
        'new_browser_tab': True,
        'launcher_entry': {
            'title': 'tensorboard',
            'icon_path': _get_icon_path()
        },
    }
