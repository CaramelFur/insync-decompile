#!/bin/bash

echo "Installing necessary packages..."

pip install uncompyle6 > /dev/null

cd ./builddir/code/

echo "Decompiling the needed files..."

uncompyle6 -o ./idesksync/licensing.py ./idesksync/licensing.pyc > /dev/null
rm ./idesksync/licensing.pyc

echo "Modifying the decompiled files..."

sed -i 's|  _verify_signature(data.encode(), signature)|  #replaced|g' ./idesksync/licensing.py
sed -i 's|if expiry is None:|if False:|g' ./idesksync/licensing.py
sed -i 's|day = 86400|day = 86400\n    expiry = _approx_time() + day * 5|g' ./idesksync/licensing.py

echo "Done!"
