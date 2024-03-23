from django.core.validators import RegexValidator

LONG_STR = 254
MEDIUM_STR = 50
SHORT_STR = 10
MESSANGERS = [
    ('1', 'Telegram'),
    ('2', 'WhatsApp'),
    ('3', 'Телефон')
]
DOMINANT_SIDES = [
    ('1', 'Правша'),
    ('2', 'Левша'),
]
MIN_WEIGHT = 50
MAX_WEIGHT = 120
MIN_HEIGHT = 150
MAX_HEIGHT = 210


def validate_format(value):
    """Проверка допустимости поля игровой формат."""
    validator = RegexValidator(
        regex=r'^\d+ x \d+$',
        message=('Введите игровой формат в виде 10 x 10')
    )
    validator(value.lower())
