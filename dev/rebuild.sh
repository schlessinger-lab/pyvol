
# update the version in:
#   setup.py
#   meta.yaml
#   pyvol/__init__.py
#   pyvol/pyvol_gui/__init__.py
# login to anaconda with "anaconda login"
# run this script from the pyvol/dev directory with the version number as the only argument

if [ -z $1 ]; then
  echo "You must pass a version to run this script"
  exit
fi

sh document.sh
sh build.sh
sh package_plugin.sh $1
