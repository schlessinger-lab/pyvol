
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
        "bio",
        "numpy",
        "pandas",
        "scipy",
        "scikit-learn",
        "trimesh",
        ],
    entry_points={
        "console_scripts": [
            "pyvol=pyvol.__main__:main",
            ]
        },
    )
