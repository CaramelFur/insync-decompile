#!/bin/bash

echo Cleaning unpacked raw debian package
rm -r ./builddir/deb_raw/*

echo Cleaning unpacked debian package files
rm -r ./builddir/deb/*

echo Cleaning packed and compiled insync files
rm -r ./builddir/sourceLib/*

echo Cleaning unpacked but compiled insync files
rm -r ./builddir/code/*
rm ./builddir/code/.python-version

echo Cleaning temp build lib files for pyinstaller
rm -r ./builddir/distLib_build/*

echo Cleaning builded lib files
rm -r ./builddir/distLib/*

echo Cleaning temp deb build files
rm -r ./builddir/distDeb_build/*

echo Cleaning temp arch build files
rm -r ./builddir/distArch_build/*