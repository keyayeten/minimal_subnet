from setuptools import setup, find_packages

setup(
    name='ip_manipulations',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'minimal_subnet=ip_manipulations.controller:main',
        ],
    },
)
