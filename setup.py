import os
from setuptools import setup, find_packages

DIR = os.path.dirname(os.path.abspath(__file__))
readme = open(os.path.join(DIR, 'README.md')).read()
files = ["./assets/*.json"]

setup(
    name='katana',
    version='0.0.1',
    description="""Ethereum Development Framework""",
    long_description=readme,
    author='David Knott',
    author_email='david1k1nott@gmail.com',
    url='https://github.com/DavidKnott/katana',
    package_dir={'katana/':'.'},
    include_package_data=True,
    package_data={'katana':files},
    py_modules=['katana'],
    install_requires=[
        "click>=6.7",
        "viper==0.0.1"
    ],
    dependency_links=[
        'https://github.com/ethereum/viper/tarball/master#egg=viper-0.0.1',
    ],
    license="MIT",
    zip_safe=False,
    entry_points={
        'console_scripts': ["katana=katana.cli:main"],
    },
    keywords='ethereum viper pytest',
    packages=find_packages(exclude=["tests", "tests.*"]),
        classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
)