from django.core.validators import RegexValidator

LONG_STR = 254
MEDIUM_STR = 50
SHORT_STR = 10
MIN_WEIGHT = 50
MAX_WEIGHT = 120
MIN_HEIGHT = 150
MAX_HEIGHT = 210


def validate_format(value: str) -> None:
    """Проверка допустимости поля игровой формат."""
    validator = RegexValidator(
        regex=r'^\d+ x \d+$',
        message=('Введите игровой формат в виде 10 x 10')
    )
    validator(value.lower())


def validate_phone_number(value: str) -> None:
    """Проверка формата ввода номера телефона."""
    validator = RegexValidator(
        regex=r'^\+7-\d{3}-\d{3}-\d{2}-\d{2}$',
        message=('Введите номер телефона в формате +7-911-123-45-67')
    )
    validator(value.lower())
