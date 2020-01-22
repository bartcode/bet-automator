from setuptools import find_packages
from setuptools import setup

setup(
    name='bet-automator',
    version='0.1.0',
    python_requires='>=3.7',
    install_requires=[
        'requests==2.22.0',
        'pandas==0.25.3',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['autobet=src.__main__:main'],
    },
    description='Automatically determine the right bets of the day.',
    data_files=[('autobet', ['logger.ini', 'config.yml'])]
)
