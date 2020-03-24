pyvol_dev_root="/home/rsmith/research/pyvol_development"
docs_dir="${pyvol_dev_root}/pyvol/docs"

if [ -d "${pyvol_dev_root}/_build" ]; then
  rm -r "${pyvol_dev_root}/_buil"
fi

cd "${pyvol_dev_root}/pyvol"
# pandoc -s -o README.md README.rst

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

cd ${docs_dir}
make latexpdf
if [ -f "manual.pdf" ]; then
  mv manual.pdf pyvol_manual.pdf
  git add .; git commit -m "[auto] rebuilt pdf"; git push origin master
fi

# sphinx-apidoc run with: sphinx-apidoc -o docs/source/ pyvol/
# PyMOL 3k5v view 1: (-0.8930549025535583, 0.4392430782318115, 0.09748003631830215, -0.4189101457595825, -0.8907894492149353, 0.17604589462280273, 0.16416054964065552, 0.11639083176851273, 0.9795329570770264, 0.0001701563596725464, 0.00048378854990005493, -182.1396942138672, 17.222610473632812, 22.656993865966797, 59.59479522705078, 166.03463745117188, 198.02749633789062, -20.0)
# view 2: (-0.7477022409439087, 0.4609299898147583, -0.47798359394073486, -0.43831321597099304, -0.8833208084106445, -0.16615529358386993, -0.49880295991897583, 0.08527922630310059, 0.8624975681304932, 0.0009277071803808212, 0.0003758147358894348, -110.71723937988281, 18.246036529541016, 12.564921379089355, 58.72468185424805, 89.2468032836914, 131.82928466796875, -20.0)
