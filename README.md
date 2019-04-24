# PyVOL

PyVOL is a python library for calculating the volumes of protein binding pockets. While the code can be used to identify binding pockets, the intended use is to describe features of known sites. PyVOL can be imported and run as a python package, run from the command line using the provided argument parser, or run from within PyMOL. Visualization of results is intended to be done through PyMOL.

The API is not guaranteed to be stable.

## Basic Installation

PyVOL minimally requires biopython, msms, numpy, pandas, scipy, scikit-learn, and trimesh in order to run. With the exclusion of MSMS, PyVOL can be installed along with its dependencies simply with:
```bash
pip install bio-pyvol
```
MSMS can be installed manually or (on Linux and OSX) installed from the bioconda channel.

Once PyVOL is installed in the python environment used by PyMOL, the script can be installed by using the plugin manager to install the file "pyvol_plugin.py".

## Quick Start
The simplest binding pocket calculation is simply run with:
```bash
pocket protein_selection
```

## old readme documentation
The PyVOL backend relies on the following dependencies (tested versions in parentheses):
biopython (1.73)
numpy (1.16.1)
pandas (0.24.1)
scipy (1.2.1)
scikit-learn (0.20.2)
trimesh (2.36.29)
msms

PyMOL is sometimes bugged and uses the environment defined by pip rather than conda. In that case run:
pip install pandas scipy scikit-learn trimesh

These can be installed with conda or pip using:
conda install biopython pandas scipy scikit-learn trimesh

biopython and trimesh are available on the conda-forge channel. This can be added with:
conda config --add chanels conda-forge

on Linux or Mac, msms can be installed with:
conda install -c bioconda msms
on Windows, it must be installed manually for now

The PyVOL frontend is currently optimized only for PyMOL 2.0+ and can be installed using the plugin manager after the dependencies have been installed into the same environment that holds PyMOL.
