
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="bio-pyvol",
    version="1.0.0",
    description="Protein binding pocket partitioning and volume calculations",
    long_description=README,
    long_dscription_content_type="text/markdown",
    url="https://github.com/rhs2132/pyvol",
    author="Ryan Smith",
    author_email="rhydesmith@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        ],
    packages=["pyvol"],
    install_requires=[
        "bio>=1.73",
        "numpy>=1.16.1",
        "pandas>=0.24.1",
        "scipy>=1.2.1",
        "scikit-learn>=0.20.2",
        "trimesh>=2.36.29",
        ],
    entry_points={
        "console_scripts": [
            "pyvol=pyvol.__main__:main",
            ]
        },
    )
