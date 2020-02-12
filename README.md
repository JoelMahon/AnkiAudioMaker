# AnkiAudioMaker

This program was something I made for myself to increase my repetitions of my Anki decks when I'm out and about, or just not in the mood to stare at a screen. Especially important for me because the app on my phone's OS doesn't work for media - or at least I couldn't get it to work for media.

What it does in abstract terms is generate an audio file based on a subset of cards' fields.

This script doesn't affect Anki at all, it only reads, never writes. You should still use Anki as you normally would, and only use this as an extra bit of study if you wish.

For example, I can generate a file with all cards from my "Japanese Core 2000 words" deck that are due tomorrow, which will contain each of those cards represented in audio in sequence.

How each card is represented in audio is up to your configuration. I personally have the audio play for the Japanese word, followed by a long pause (to allow time to think), followed by the English answer (using text-to-speech), then a shorter pause.

See [Extra Configuration](https://github.com/JoelMahon/AnkiAudioMaker/blob/master/README.md#L26) to see how to get the fields you want, in the order you want. You can make one .bat that swaps the prompt and the answer for example. Note: this program uses the notes' fields, this means it has no concept of prompt and answer, as in Anki the notes can be used to generate many cards. This can work poorly with my program, sorry! It's on my TODO list to change to work more aligned to how Anki works.

## Set up:
At some point I may add an executable, but for now you gotta use this the hard way I'm afraid!

1. Install the most recent python 3 https://www.python.org/downloads/ (or update if you already have it)
2. Install FFmpeg https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg
3. Clone or download this repo
4. In a console/terminal change directory into your local copy of the repo - Windows console command: cd [YOUR PATH GOES HERE]
4. Create a new python virtual environment called "venv" - Windows console command: python -m virtualenv venv
5. Activate your new virtual enviroment - Windows console command: venv/bin/activate
6. Using the requirements.txt - Windows console command: pip install -r requirements.txt

## Extra Configuration
The .bat as is may be what you want, but odds are low. It's actually quite flexiable in what you can do!

There are three labelled options:

-d <deck_name>: As the name implies, this lets you choose a single deck to process. If left blank it will process all decks for the choosen profile.

-c <collection_path>: If you get tired of choosing the collection.anki2 file each time, you can just put the path in the .bat (remember to surround with "s).

-a <all_cards>: Will be set to False by default, use either true, t, or y, to set this to True (case insensitive). When set to false it will only use the cards that are closest to being due (today's due cards if there are any, tomorrow's if none are due today, etc.). When set to true it will use every card in your choosen deck(s) (this could take a while).

Then after these three labelled options you should provide probably at least 6 more unlabeled ones.

These are the fields. These unlablled options must come as a multiple of three. And they should come in the order you want the audio to be in.

Each field's options should be: <field_name> <audio_or_language> <post_silence_duration_milli>

<field_name> is the name of the field to process, you may have to open Anki to find it.

<audio_or_language> is either "audio" (case insensitive) or a language flag, e.g. "en" or "fr" (supported languages can be found using the gTTS module you installed in set up https://pypi.org/project/gTTS/). If set to "audio" it will parse the field for an .mp3 name and append that .mp3. If set to anything else it will try and append text-to-speech of the field's text using the value as the language.

<post_silence_duration_milli> is the length in milliseconds of the period of silence that will follow the audio for this field.

## Usage:
1. Run the .bat
2. Choose your collection.anki2 in %APPDATA%\Anki\<profile_name>\collection.anki2 using the file selector window

It should output an .mp3 in the same directory as the .py after a while (you can see the progress in the console window, in my experience it was taking about 2-10 seconds per card)
If you left the configuration as given to you, the .mp3 is all the cards due today, Japanese Audio, a pause, then the English meaning using text-to-speech, then another pause, then the next card, etc.

Using the command line options you should be able to make this useful for any deck that doesn't rely on non-mp3 media.
So if you're learning to name every organ in the body using pictures as prompts, you're out of luck, but pretty much everyone else can use it, even without media you can use text-to-speech for both sides of the card for example, or you can use media files (.mp3 only) for both if they exist.

## License

Please see the LICENSE.md for details on the licensing information, regardless, my intention is that anyone can use this code however they want, but I accept no liability and I grant no warranty or expectation of it working (or even being safe).
