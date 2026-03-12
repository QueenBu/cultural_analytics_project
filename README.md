https://docs.google.com/document/d/1oJwCGFiuz1dje9lv5BJXDy1tYoiDs0aiudQnTb944Oo

https://docs.google.com/spreadsheets/d/1mZ07xm--TeFW3pZq4nyv4hZTCjxKz_r8LduQbGg_glo

```
docker build -t face-matcher .
```

for powerShell

```
docker run --rm -v "${PWD}:/app" face-matcher python start.py

docker run --rm -v "${PWD}:/app" face-matcher python main.py

docker run --rm -v "${PWD}:/app" face-matcher python detectFaces.py --movies-folder data/NS_Filme
```

for cmd.exe replace `"${PWD}:/app"` with `"%cd%:/app"`

```
docker run --rm -v "${PWD}:/app" face-matcher python keyframesModern.py --film-folder data/moderneFilme/MoonriseKingdom
ThreeBillboardsOutsideEbbingMissouri
docker run --rm -v "${PWD}:/app" face-matcher python keyframesModern.py --film-folder data/moderneFilme
```