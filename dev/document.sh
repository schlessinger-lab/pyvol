pyvol_dev_root="/home/rsmith/research/pyvol_development"
docs_dir="${pyvol_dev_root}/pyvol/docs"

if [ -d "${pyvol_dev_root}/_build" ]; then
  rm -r "${pyvol_dev_root}/_buil"
fi


cd ${docs_dir}
make html

if [ -f "${pyvol_dev_root}/pyvol-docs/_build/html/index.html" ]; then
  cd "${pyvol_dev_root}/pyvol-docs/gh-pages"

  rm *.html
  rm -r _sources/
  rm -r _static/

  cp -r ../_build/html/* .
  touch .nojekyll
  git add .
  git commit -m "[auto] rebuilt docs"; git push origin gh-pages
  git push origin gh-pages
fi

# make latexpdf
# if [ -f "manual.pdf"]; then
#   mv manual.pdf pyvol_manual.pdf
#   git add .; git commit -m "[auto] rebuilt pdf"; git push origin master
# fi
