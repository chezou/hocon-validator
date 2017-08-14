import setuptools

setuptools.setup(
    name='hocon-validator',
    version='0.0.1',
    packages=setuptools.find_packages(),
    install_requires=[
        'pyyaml',
        'pyhocon',
    ],
    entry_points={
        'console_scripts': [
            'hocon-validator=hocon_validator.hocon_validator:main'
        ]
    }
)