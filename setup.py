import setuptools

setuptools.setup(
    name='hocon-validator',
    description='A HOCON validator',
    author='Aki Ariga chezou',
    author_email='chezou@gmail.com',
    license='Apache License 2.0',
    keywords='HOCON validator',
    version='0.0.3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*']),
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