import setuptools
from os import path


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name="jupyter-tensorboard-proxy",
    version='0.1.1',
    url="https://github.com/kopwei/jupyter-tensorboard-proxy",
    author="kopkop",
    description="kopkop@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
	keywords=['jupyter', 'tensorboard', 'jupyterhub'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[
        'jupyter-server-proxy>=1.5.0',
        'tensorboard>=2.4.1'
    ],
    entry_points={
        'jupyter_serverproxy_servers': [
            'tensorboard = jupyter_tensorboard_proxy:setup_tensorboard',
        ]
    },
    package_data={
        'jupyter_tensorboard_proxy': ['icons/tensorboard.svg'],
    },
)
