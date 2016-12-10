#!/bin/bash

DL_URL=https://sourceforge.net/projects/tcl/files/Tcl/8.6.1/tk8.6.1-src.tar.gz
DL_DIR=tk8.6.1/

mkdir -p download
mkdir -p download/cache
cd download

rm -f *src..tar.gz
rm -rf tk8.6.1/ 

wget --no-check-certificate $DL_URL
tar x --wildcards -vf tk8.6.1-src.tar.gz tk8.6.1/doc/*

