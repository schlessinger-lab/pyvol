
if [ -z $1 ]; then
  echo "You must pass a gui version to run this script"
  exit
fi

sh document.sh
sh build.sh
sh package_plugin.sh $1
