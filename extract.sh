#!/bin/bash

echo "Setting up and finding file"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR/builddir/deb_raw/"
DEB="$(ls $DIR/source/*.deb)"

echo "Found a file: $DEB"

echo "Unpacking the .deb file"

ar x "$DEB"
cd "$DIR/builddir/"

tar -xzf ./deb_raw/data.tar.gz -C ./deb/
mkdir -p ./deb/DEBIAN/
tar -xzf ./deb_raw/control.tar.gz -C ./deb/DEBIAN/
cp ./deb_raw/debian-binary ./deb/debian-binary

rm ./deb/DEBIAN/md5sums
sed -r -i "s|^add_repo$|#no|g" ./deb/DEBIAN/postinst
sed -r -i "s|^update_key$|#no|g" ./deb/DEBIAN/postinst

cd $DIR

echo "Preparing to extract files from the the unpacked deb"

mv ./builddir/deb/usr/lib/insync/* ./builddir/sourceLib

echo "Installing packages..."

pip install -r ./decompiler/requirements.txt > /dev/null

echo "Extracting the .pyc files from the unpacked deb..."

python ./decompiler/unpack.py ./builddir/sourceLib/ ./builddir/code/ > /dev/null

echo
echo "Successfully extracted all files, there is a requirements.txt file in ./extract/code, do not forget to install these packages with python version"
cat ./builddir/code/.python-version