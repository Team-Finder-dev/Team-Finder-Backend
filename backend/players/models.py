from api import validators
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from teams import models as teams_models


class Position(models.Model):
    """Position model"""
    name = models.CharField(
        verbose_name=("Позиция"),
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
        related_name="players",
        on_delete=models.CASCADE,
    )
    palyer = models.ForeignKey(
        "Player",
        related_name="sport_positions",
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
        return self.characteristic


class PlayerPositionCharacteristic(models.Model):
    """Model connect player and Sport positon"""
    position_characteristic = models.ForeignKey(
        PositionCharacteristic,
        related_name="players",
        on_delete=models.CASCADE,
    )
    palyer = models.ForeignKey(
        "Player",
        related_name="position_characteristics",
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


class DominantSide(models.Model):
    """DominantSide"""
    name = models.CharField(
        verbose_name=("Доминирующая рука/нога"),
        max_length=validators.SHORT_STR,
    )

    class Meta:
        verbose_name = ("DominantSide")
        verbose_name_plural = ("DominantSides")

    def __str__(self):
        return self.name


class SportDominantSide(models.Model):
    """SportDominantSide model"""
    dominant_side = models.ForeignKey(
        DominantSide,
        verbose_name=("Доминирующая рука/нога"),
        on_delete=models.CASCADE,
        related_name="sports",
    )
    sport = models.ForeignKey(
        teams_models.Sport,
        verbose_name=("Спорт"),
        on_delete=models.CASCADE,
        related_name="dominant_sides",
    )

    class Meta:
        verbose_name = ("SportDominantSide")
        verbose_name_plural = ("SportDominantSides")

    def __str__(self):
        return f"{self.sport} {self.dominant_side}"


class Player(teams_models.EntityBaseModel):
    """Player model"""
    birthday = models.DateField(
        verbose_name=("Дата рождения"),
        auto_now=False,
        auto_now_add=False,
        help_text=("Дата рождения"),
        blank=False,
    )
    dominant_side = models.ForeignKey(
        DominantSide,
        verbose_name=("Доминирующая рука/нога"),
        on_delete=models.SET_NULL,
        related_name="players",
        blank=False,
        null=True,
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
    about = models.TextField(
        verbose_name=("О себе"),
        help_text="Расскажите о себе",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Class introduced because teams and player are inhereted from the same class
# the connection between teams and player is one_to_many
class TeamPlayer(models.Model):
    """TeamPlayer model"""
    player = models.ForeignKey(
        Player,
        verbose_name=("Игрок"),
        on_delete=models.CASCADE,
        related_name="teams",
    )
    team = models.ForeignKey(
        teams_models.Team,
        verbose_name=("Команда"),
        on_delete=models.CASCADE,
        related_name="players",
    )

    class Meta:
        verbose_name = ("TeamPlayer")
        verbose_name_plural = ("TeamPlayers")

    def __str__(self):
        return self.player
