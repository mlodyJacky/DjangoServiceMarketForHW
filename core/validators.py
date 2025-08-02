# core/validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import requests
from nudenet import NudeDetector
import os
import tempfile
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import numpy as np
import tensorflow as tf
import tempfile


POLISH_BAD_ROOTS = [
    'kurw', 
    'pizd', 
    'chuj', 
    'jeba', 
    'pierdol',
    'skurw', 
    'sucz', 
    'cip', 
    'pojeb',
    'deb'
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

    for root in POLISH_BAD_ROOTS:
        if root in low:
            raise ValidationError(
                _('Pole zawiera niedozwolone słowo podobne do '),
                params={'root': root},
            )

    words = set(low.split())
    bad_en = words & english_bad
    if bad_en:
        word = bad_en.pop()
        raise ValidationError(
            _('Pole zawiera niedozwolone słowo: “%(word)s”'),
            params={'word': word},
        )
    


detector = NudeDetector()

def validate_image_is_safe(image_file):
    ext = os.path.splitext(image_file.name)[1]
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(image_file.read())
        tmp.flush()
        tmp_path = tmp.name

    try:
        detections = detector.detect(tmp_path)
    finally:
        os.unlink(tmp_path)

    for det in detections:
        score = det.get('score', 0)
        label = det.get('class', 'UNKNOWN')
        if score > 0.5:
            raise ValidationError(
                _('Zdjęcie prawdopodobnie zawiera niedozwolone treści'),
                params={'label': label, 'score': score},
            )
        

import joblib, os
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
from skimage.color import rgb2gray
HOTWHEELS_MODEL = joblib.load('hw_classifier_rf.joblib')




def validate_image_is_hotwheels(file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            for chunk in file.chunks():
                temp.write(chunk)
            temp_path = temp.name

        img = Image.open(temp_path).convert("RGB")
        img_np = np.array(img)
        gray = rgb2gray(img_np)
        resized = resize(gray, (128, 128))
        features = hog(resized, pixels_per_cell=(16,16), cells_per_block=(2,2), feature_vector=True)

        p = HOTWHEELS_MODEL.predict_proba([features])[0][1]

        if p < 0.43:
            raise ValidationError(
                _(f"Zbyt mało HW na zdjeciu by je dodać")
            )
    except Exception as e:
        raise ValidationError(f"Błąd analizy obrazu: {e}")

