if [ -z $1 ]; then
  echo "You must pass a gui version to run this script"
  exit
fi

echo "Building gui zip file for version" $1

pyvol_dev_root="/home/rsmith/research/pyvol_development"
cache_dir="${pyvol_dev_root}/pyvol/pyvol/pyvol_gui/cached_source"
project_dir="${pyvol_dev_root}/pyvol/pyvol"

full_zip_name="pyvol-${1}-full-installer.zip"
small_zip_name="pyvol-${1}-installer.zip"

cd ${project_dir}
zip -r ${small_zip_name} pyvol_gui/ -x "pyvol_gui/cached_source/*"
mv ${small_zip_name} ..

# cd $cache_dir
# # pip download bio-pyvol --no-binary :all:
#
# cd ${project_dir}
# zip -r ${full_zip_name} pyvol_gui/
# mv ${full_zip_name} ..

cd ..
git add ${full_zip_name}
git add ${small_zip_name}
git commit -m "[auto] created new installers for version ${1}"
git push origin master
