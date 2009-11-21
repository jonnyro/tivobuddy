wget --no-check-certificate --http-user=tivo --http-password=YOURMAKHERE -O tivoroll.xml "https://$1/TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse=Yes"
