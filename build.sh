#!/bin/bash

echo "Make sure you have dpkg installed on your system"
dpkg -V

echo "Make sure your are running python version 3.7.4, your python version is:"
python -V

cd ./builddir/

echo "Ensuring clean build directory"

rm -r ./distLib/*
rm -r ./distLib_build/*
rm -r ./distDeb_build/*
rm -r ./distArch_build/*

echo "Building lib..."

#pyinstaller --clean --onedir --distpath ./distLib/ --workpath ./distLib_build/ --add-data "./code/ideskui/build:./ideskui/build" -p ./code/ ./code/insync.py > /dev/null
pyinstaller --distpath ./distLib/ -p ./code/ ./code/insync.py

mv ./*.spec ./distLib/

echo "Done building lib..."

echo "Preparing to build deb package"

cp -r ./deb/usr ./distDeb_build
cp -r ./deb/DEBIAN ./distDeb_build
cp ./deb/debian-binary ./distDeb_build
cp -r ./distLib/insync ./distDeb_build/usr/lib/

echo "Building deb package..."
dpkg-deb -Z gzip -b ./distDeb_build/ ./distArch_build/insync.deb > /dev/null
echo "Done building deb package"

echo "Preparing to build arch package"

git clone https://aur.archlinux.org/insync.git ./distArch_build/.temp
mv ./distArch_build/.temp/* ./distArch_build/
rm -rf ./distArch_build/.temp

sed -r -i "s|'[a-z0-9]{64}'|'SKIP'|g" ./distArch_build/PKGBUILD
sed -i 's|"http://s.insynchq.com/builds/${pkgname}_${pkgver}-${_dist}_amd64.deb"|"insync.deb"|g' ./distArch_build/PKGBUILD

cd ./distArch_build/

echo "Building arch package..."

makepkg --noconfirm > /dev/null

echo "Done building arch package..."

cd ..

echo "Moving all files to out"

cp ./distArch_build/insync.deb ../out/
cp ./distArch_build/*.pkg.tar.xz ../out/

echo "Done!"
