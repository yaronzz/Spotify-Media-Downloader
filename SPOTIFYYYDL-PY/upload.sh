cd SPOTIFYYYDL-PY
rm -rf dist
rm -rf build 
rm -rf exe 
rm -rf spotifyyy_dl.egg-info
mkdir exe

# pack
python setup.py sdist bdist_wheel
# creat exe file
pyinstaller -F spotifyyy_dl/__init__.py
# rename exe name
mv dist/__init__.exe exe/spotifyyy_dl-dl.exe

pip uninstall -y spotifyyy_dl-dl

# creat requirements.txt
pipreqs ./ --force --encoding=utf8

# python setup.py install

# upload
twine upload dist/*







# powershell·
cd QOBUZZZDL-PY
Remove-Item dist -recurse -Force
Remove-Item build -recurse -Force
Remove-Item exe -recurse -Force
Remove-Item spotifyyy_dl.egg-info -recurse -Force
md exe

# pack
python setup.py sdist bdist_wheel
# creat exe file
pyinstaller -F spotifyyy_dl/__init__.py
#pyinstaller -F -i ../logo.ico spotifyyy_dl/__init__.py
# rename exe name
cp dist/__init__.exe exe/qobuzzz-dl.exe
rm dist/__init__.exe

pip uninstall -y qobuzzz-dl

# creat requirements.txt
# pipreqs ./ --force

# python setup.py install

# upload
twine upload dist/*
