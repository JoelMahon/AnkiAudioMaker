from gtts import gTTS
from pydub import AudioSegment
from datetime import datetime
from ankisync2.anki import db
from tqdm import tqdm
from tkinter import filedialog
import tkinter as tk
import os
import getopt

FIELD_ARG_FORMAT_SIZE = 3

DATE_STR = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
EXTENSION = "mp3"
OUT_PATH = f"AnkiAudioMaker_{DATE_STR}.{EXTENSION}"

ONE_SEC_SIL = AudioSegment.silent(1000)

AUDIO_PRE_SLICE = len("[sound:")
AUDIO_POST_SLICE = -len("]")

TTS_PATH = f"TTS_tmp.{EXTENSION}"


def main(argv):
    deck_name, collection_path, all_cards = parse_args(argv)
    format_tuples = list_of_tuples_from_iterable(argv, FIELD_ARG_FORMAT_SIZE)
    make_all_audio(deck_name, collection_path, all_cards, format_tuples).export(OUT_PATH, format=EXTENSION)


def list_of_tuples_from_iterable(iterable, size=2):
    it = iter(iterable)
    return list(zip(*[it] * size))


def parse_args(argv):
    deck_name = ""  # default to no deck (will use all decks)
    collection_path = ""  # default to no path (will ask for path with UI)
    all_cards = False  # default to False (just use today's cards)

    opts = None

    usage = "test.py -d <deck_name> -c <collection_path> -a <all_cards>"
    try:
        opts, _ = getopt.getopt(argv, "hd:c:a:", ["deck_name=", "collection_path=", "all_cards="])
    except getopt.GetoptError:
        print(usage)
        input("Press enter to continue...")
        exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(usage)
            input("Press enter to continue...")
            exit()
        elif opt in ("-d", "--deck_name"):
            deck_name = arg
        elif opt in ("-c", "--collection_path"):
            collection_path = arg
        elif opt in ("-a", "--all_cards"):
            all_cards = arg.lower() in ['true', 't', 'y']

    # remove all the non-option based arguments to leave the field triples (field_key audio/text post_silence_dur_milli)
    [(argv.remove(key), argv.remove(value)) for key, value in opts]
    if len(argv) % FIELD_ARG_FORMAT_SIZE != 0:
        print(f"Non-option arguments must come as a multiple of {FIELD_ARG_FORMAT_SIZE}")
        input("Press enter to continue...")
        exit()
    return deck_name, collection_path, all_cards


def make_all_audio(deck_name, collection_path, all_cards, format_tuples):
    tk.Tk().withdraw()
    collection_path = os.path.expandvars(collection_path)
    collection_path = collection_path or filedialog.askopenfilename(title="Choose collection.anki2")
    if not collection_path:
        print("You must choose a collection_path or specify one in the arguments")
        input("Press enter to continue...")
        exit()

    init_db(collection_path)

    cards = get_cards(deck_name, all_cards)

    media_path = os.path.dirname(collection_path) + "/collection.media/"

    # add a bit of silence to the start of the audio
    output_audio = ONE_SEC_SIL

    for card in tqdm(cards):
        output_audio = output_audio + make_card_audio(card, media_path, format_tuples)

    os.remove(TTS_PATH)

    # add a bit of silence to the end of the audio
    output_audio = output_audio + ONE_SEC_SIL * 4
    return output_audio


def init_db(collection_path):
    def fix():
        c = db.Col.get()

        for d in c.decks.values():
            db.Decks.create(id=d["id"], name=d["name"])

        for m in c.models.values():
            db.Models.create(id=m["id"], name=m["name"], flds=[f["name"] for f in m["flds"]], css=m["css"])

            for t in m["tmpls"]:
                db.Templates.create(mid=m["id"], name=t["name"], qfmt=t["qfmt"], afmt=t["afmt"])

    db.database.init(collection_path)

    if 'col' not in db.database.get_tables():
        db.database.create_tables([
            db.Col, db.Notes, db.Cards, db.Graves, db.Revlog
        ])
        db.Col.create()

    if 'decks' not in db.database.get_tables():
        db.database.create_tables([
            db.Decks, db.Models, db.Templates
        ])
        fix()


def make_card_audio(card, media_path, format_tuples):
    card_audio = AudioSegment.empty()

    for key, audio_or_lang, post_silence_dur_milli in format_tuples:
        if audio_or_lang.lower().startswith("a"):  # a for audio!
            tuple_audio = AudioSegment.from_mp3(media_path + card[key][AUDIO_PRE_SLICE:AUDIO_POST_SLICE])
        else:  # text
            # generate TTS and save it to a temporary file for PyDub to load
            gTTS(text=card[key], lang=audio_or_lang, slow=False).save(TTS_PATH)
            tuple_audio = AudioSegment.from_mp3(TTS_PATH)

        card_audio = card_audio + tuple_audio + AudioSegment.silent(int(post_silence_dur_milli))

    return card_audio


def get_cards(deck_name, all_cards):
    cards = []
    min_due = None
    for c in db.Cards.select(db.Cards, db.Decks, db.Notes.flds, db.Models) \
            .join(db.Decks, on=(db.Decks.id == db.Cards.did)) \
            .where(db.Decks.name.startswith(deck_name)) \
            .join(db.Notes, on=(db.Notes.id == db.Cards.nid)) \
            .join(db.Models, on=(db.Models.id == db.Notes.mid)) \
            .order_by(db.Cards.due):
        if not all_cards:
            if not min_due:
                min_due = c.due
            elif c.due > min_due:
                break
        cards.append(dict(zip(c.note.model.flds, c.note.flds)))

    return cards


if __name__ == "__main__":
    main(os.sys.argv[1:])
