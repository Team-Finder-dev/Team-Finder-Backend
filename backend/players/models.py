from api import validators
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from teams import models as teams_models


class Position(models.Model):
    """Position model"""
    name = models.CharField(
        verbouse_name=("Позиция"),
        help_text="Выберите позицию",
        max_length=validators.MEDIUM_STR,
    )

    class Meta:
        verbose_name = ("Position")
        verbose_name_plural = ("Positions")

    def __str__(self):
        return self.name


class SportPosition(models.Model):
    """SportPosition model"""
    sport = models.ForeignKey(
        teams_models.Sport,
        verbose_name="Sport",
        on_delete=models.CASCADE,
        related_name="sport_positions"
    )
    position = models.ForeignKey(
        Position,
        verbose_name="Position",
        on_delete=models.CASCADE,
        related_name="sport_positions"
    )

    class Meta:
        verbose_name = ("SporPosition")
        verbose_name_plural = ("SporPositions")

    def __str__(self):
        return f'{self.sport.name}: {self.position.name}'


class PlayerSportPosition(models.Model):
    """Model connect player and Sport positon"""
    sport_postion = models.ForeignKey(
        SportPosition,
        realted_name="players",
        on_delete=models.CASCADE,
    )
    palyer = models.ForeignKey(
        "Player",
        realted_name="sport_positions",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = ("PlayerSportPosition")
        verbose_name_plural = ("PlayerSportPositions")


class CharacteristicCategory(models.Model):
    """CharacteristicCategory model"""
    name = models.CharField(
        verbose_name=("Категория"),
        max_length=validators.MEDIUM_STR,
    )

    class Meta:
        verbose_name = ("CharacteristicCategory")
        verbose_name_plural = ("CharacteristicCategories")

    def __str__(self):
        return self.name


class Characteristic(models.Model):
    """Characteristic model"""
    name = models.CharField(
        verbose_name=("Характеристика"),
        max_length=validators.MEDIUM_STR,
    )
    category = models.ForeignKey(
        CharacteristicCategory,
        related_name="characteristics",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = ("Characteristic")
        verbose_name_plural = ("Characteristics")

    def __str__(self):
        return self.name


class PositionCharacteristic(models.Model):
    """PositionCharacteristic model"""
    characteristic = models.ForeignKey(
        teams_models.Sport,
        verbose_name="Спортивня характеристика",
        on_delete=models.CASCADE,
        related_name="position_characteristics"
    )
    position = models.ForeignKey(
        Position,
        verbose_name="Position",
        on_delete=models.CASCADE,
        related_name="position_characteristics"
    )

    class Meta:
        verbose_name = ("PositionCharacteristic")
        verbose_name_plural = ("PositionCharacteristics")

    def __str__(self):
        return f"{self.position.name}: {self.characteristic.name}"


class PlayerPositionCharacteristic(models.Model):
    """Model connect player and Sport positon"""
    position_characteristic = models.ForeignKey(
        PositionCharacteristic,
        realted_name="players",
        on_delete=models.CASCADE,
    )
    palyer = models.ForeignKey(
        "Player",
        realted_name="position_characteristics",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = ("PlayerPositionCharacteristic")
        verbose_name_plural = ("PlayerPositionCharacteristics")


class PlayerContactDetails(teams_models.ContactDetails):
    """PlayerContactDetails model"""
    player = models.ForeignKey(
        "Player",
        verbose_name=("Контактные данные"),
        related_name="contact_details",
        on_delete=models.CASCADE,
    )


class Player(teams_models.EntityBaseModel, teams_models.UserDetails):
    """Player model"""
    team = models.ForeignKey(
        teams_models.Team,
        verbose_name=("Команда"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    is_lefty = models.BooleanField(
        verbose_name="Доминирующая рука/нога",
        default=False,
    )
    weight = models.PositiveSmallIntegerField(
        verbose_name=("Вес"),
        validators=[MinValueValidator(validators.MIN_WEIGHT),
                    MaxValueValidator(validators.MAX_WEIGHT)],
        blank=False,
        null=False,
    )
    height = models.PositiveSmallIntegerField(
        verbose_name=("Рост"),
        validators=[MinValueValidator(validators.MIN_HEIGHT),
                    MaxValueValidator(validators.MAX_HEIGHT)],
        blank=False,
        null=False,
    )
    about = models.CharField(
        verbouse_name=("О себе"),
        help_text="Расскажите о себе",
        max_length=validators.LONG_STR,
    )

    def __str__(self):
        return self.name
