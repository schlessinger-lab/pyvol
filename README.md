# PyVOL

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
