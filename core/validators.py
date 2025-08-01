# core/validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import requests

POLISH_BAD_ROOTS = [
    'kurw',   # pokryje: kurwa, kurwie, kurwami…
    'pizd',   # pizda, pizdą, pizdom…
    'chuj',   # chuj, chuja, chujem…
    'jeba',   # jebac, jebie, jebane…
    'pierdol',# pierdol, pierdole, pierdolony…
    'skurw',  # skurwysyn, skurwiel…
    'sucz',   # suka, suczka…
    'cip',    # cipa, cipki…
    'pojeb',  # pojebany, pojeb…
    'deb',    # debil, debilny…
    'cwel',
    'huj',
    'kutas',
    'pizda',
    'kretyn',
    'zjeb',
    'rucha',
    'spierd',
    'niedorucha',
    'pierdo',
    'sperma'
]

en_resp = requests.get(
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en'
)
english_bad = set(en_resp.text.splitlines())

def validate_no_bad_words(value: str):
    low = value.lower()

    # 1) Sprawdź korzenie polskie:
    for root in POLISH_BAD_ROOTS:
        if root in low:
            raise ValidationError(
                _('Pole zawiera niedozwolone słowo podobne do „%(root)s”'),
                params={'root': root},
            )

    # 2) Sprawdź słowa angielskie w całości:
    words = set(low.split())
    bad_en = words & english_bad
    if bad_en:
        word = bad_en.pop()
        raise ValidationError(
            _('Pole zawiera niedozwolone słowo: “%(word)s”'),
            params={'word': word},
        )