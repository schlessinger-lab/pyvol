if [ -z $1 ]; then
  echo "You must pass a version to run this script"
  exit
fi

echo "Building gui zip file for version" $1

pyvol_dev_root="/home/rsmith/research/pyvol_development"
project_dir="${pyvol_dev_root}/pyvol/pyvol"

zip_name="pyvol-${1}-installer.zip"

cd ${project_dir}
zip -r ${zip_name} pyvol_gui/
mv ${small_zip_name} ../installers/
cp ../installers/${small_zip_name} ../installers/pyvol-installer.zip

cd ..
git add installers/*.zip
git commit -m "[auto] created new installer for version ${1}"
git push origin master
