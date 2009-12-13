wget --no-check-certificate --http-user=tivo --http-password=$2 -O tivoroll.xml "https://$1/TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse=Yes"
