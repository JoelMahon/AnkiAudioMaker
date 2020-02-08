pushd %~dp0
call .\venv\Scripts\activate
python .\AnkiAudioMaker.py -d "Core 2000" -c "%APPDATA%\Anki2\Joel\collection.anki2" Vocabulary-Audio Audio 4000 Vocabulary-English en 500