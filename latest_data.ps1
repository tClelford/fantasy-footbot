$repo="Fantasy-Premier-League"
git clone git@github.com:vaastav/Fantasy-Premier-League.git
Remove-Item -Recurse -Force "./data"

Move-Item -Path ".\$repo\data" -Destination ".\data"
Remove-Item -Recurse -Force ./$repo