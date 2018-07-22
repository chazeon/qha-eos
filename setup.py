from setuptools import setup, find_packages

setup(
    name='qha-eos',
    version='0.0.1',
    packages=find_packages('src'),
    package_dir={
        '': 'src'
    },
    install_requires=[
        'numpy',
        'qha'
    ],
    entry_points={
        'qha.plugins': [
            'eos = qha_eos.app:QHAEOSCommandHandler'
        ],
        'console_scripts': [
            'qha-eos = qha_eos.__main__:main'
        ]
    }
)
