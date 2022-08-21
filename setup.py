from setuptools import setup

setup(
    name = "ehh",
    version = "1.1.0",
    author = "Lennard Voogdt",
    author_email = "lennard@spring.nl",
    description = ("A tool for easy aliasing and listing of (complex) linux/bash commands. Support for custom vars."),
    license = "MIT",
    keywords = "remember linux commands alias listing",
    url = "https://github.com/lennardv2/ehh",
    packages=['ehh'],
    install_requires=['colorama', 'click', 'pyyaml'],
    entry_points={
        'console_scripts': [
            'ehh = ehh:main',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
    ],
)