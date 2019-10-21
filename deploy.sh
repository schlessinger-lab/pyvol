if [ -d "bio_pyvol.egg-info"]; then
  rm -r "bio_pyvol.egg-info"
fi

if [ -d "build"]; then
  rm -r "build"
fi

if [ -d "dist"]; then
  rm -r "dist"
fi

python setup.py sdist bdist_wheel --universal
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

if [ -d "bio_pyvol.egg-info"]; then
  rm -r "bio_pyvol.egg-info"
fi

if [ -d "build"]; then
  rm -r "build"
fi

if [ -d "dist"]; then
  rm -r "dist"
fi
