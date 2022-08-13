#! /bin/bash

repo="Fantasy-Premier-League"
git clone git@github.com:vaastav/Fantasy-Premier-League.git
mv $repo/data data
rm -rf ./$repo