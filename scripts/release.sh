cd ..
rm -rf build
rm -rf dist
rm -rf release
rm -rf venv

python3 -m venv venv
./venv/bin/python3 -m pip install --upgrade pip
./venv/bin/python3 -m pip install -r requirements.txt
./venv/bin/python3 -m pip uninstall kivy
./venv/bin/python3 -m pip install --no-binary kivy kivy
./venv/bin/python3 -m pip install pyinstaller
./venv/bin/python3 -m PyInstaller main.spec

mv dist release
rm -rf build
rm -rf dist
rm -rf venv