echo "This must be run from the dev directory"
pyvol_root=".."

cd $pyvol_root
if [ -d "bio_pyvol.egg-info" ]; then
  rm -r "bio_pyvol.egg-info"
fi

if [ -d "build" ]; then
  rm -r "build"
fi

if [ -d "dist" ]; then
  rm -r "dist"
fi

python setup.py sdist bdist_wheel

if [ -d "dist" ]; then
  rm pyvol/pyvol_gui/cached_source/bio-pyvol-*.tar.gz
  cp dist/bio-pyvol-*.tar.gz pyvol/pyvol_gui/cached_source/

  # twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
fi

if [ -d "bio_pyvol.egg-info" ]; then
  rm -r "bio_pyvol.egg-info"
fi

if [ -d "build" ]; then
  rm -r "build"
fi

if [ -d "dist" ]; then
  rm -r "dist"
fi
