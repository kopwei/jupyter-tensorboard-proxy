import os
import shutil
import logging
from dotenv import load_dotenv


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

        # NOTES: With the edits below, it will expect to find the TF_LOG_DIR variable
        #   either already exported in the current shell session, or located in a ~/.tensorboard file
        # In addition, if using s3 for the location, it will also expect to find these env vars in the same location, either as env vars or in ~/.tensorboard
        #   AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, S3_ENDPOINT_URL (if not official AWS)
        #   If these vars are not found, errors will result from boto3 within tensorflow-io, so no error handling is needed here.

        # first look for --logdir override in the form of an s3 bucket or alternate path, then fall back to home_dir if not found
        if os.environ.get('TF_LOG_DIR'):
            TF_LOG_DIR = os.environ.get('TF_LOG_DIR')
        # providing a second option to store this in a dot file, as env vars are context/session specific
        elif os.path.isfile("%s/.tensorboard" % os.environ.get('HOME')):
            load_dotenv("%s/.tensorboard" % os.environ.get('HOME'))
            if not os.environ.get('TF_LOG_DIR'):
                logger.error("If you wish to change the tensorflow/tensorboard TF_LOG_DIR via config file instead of env var, you must put 'TF_LOG_DIR=path' in the $HOME/.tensorboard file")
            else:
                TF_LOG_DIR = os.environ.get('TF_LOG_DIR')
        else:
            # Create working directory
            home_dir = os.environ.get('HOME') or "/home/%s" % os.environ.get('NB_USER') or '/home/jovyan'
            working_dir = f'{home_dir}'
            if not os.path.exists(working_dir):
                os.makedirs(working_dir)
                logger.info("Created directory %s" % working_dir)
            else:
                logger.info("Directory %s already exists" % working_dir)
            TF_LOG_DIR = '%s/logs' % home_dir
        return ['tensorboard', '--logdir', TF_LOG_DIR, '--port', '{port}']
    
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
