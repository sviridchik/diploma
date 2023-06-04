from django.utils.translation import gettext_lazy as _

COLORS_CHOICES = [
    ('white', _('white')),
    ('black', _('black')),
]

LANGUAGE_CHOICES = [
    ('RUSSIAN', 'RUSSIAN'),
    ('ENGLISH', 'ENGLISH'),
]

TYPE_CHOICES = [
    ('injection', _('injection')),
    ('ampule', _('ampule')),
    ('pill', _('pill')),
    ('suspension', _('suspension')),
    ('bag', _('bag')),
    ('aerosols', _('aerosols')),
    ('capsules', _('capsules')),
]

SPEC_CHOICES = [
    ('endocrinologist', _('endocrinologist')),
    ('neurologist', _('neurologist')),
    ('therapist', _('therapist')),
    ('cardiologist', _('cardiologist')),
    ('ophthalmologist', _('ophthalmologist')),
    ('nutritionist', _('nutritionist')),
    ('surgeon', _('surgeon')),
]
FOOD_CHOICES = [
    ('Before meals', _('Before meals')),
    ('While eating', _('While eating')),
    ('After meal', _('After meal')),
    ('No matter', _('No matter')),
]
DOSE_CHOICES = [
    ('pcs', _('pcs')),
    ('ml', _('ml')),
]
DEVISE_CHOICES = [
    ('tablet', _('tablet')),
    ('phone', _('phone')),
    ('notebook', _('notebook')),
    ('desktop', _('desktop')),
]
