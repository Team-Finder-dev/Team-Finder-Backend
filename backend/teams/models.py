from api import validators
from django.contrib.auth.models import AbstractUser
from django.db import models


class Level(models.Model):
    """Level model"""
    name = models.CharField(
        verbose_name=("Статус"),
    )

    class Meta:
        verbose_name = ("Level")
        verbose_name_plural = ("Levels")

    def __str__(self):
        return self.name


class Sex(models.Model):
    """Sex model"""
    name = models.CharField(
        verbose_name=("Пол"),
    )

    class Meta:
        verbose_name = ("Sex")
        verbose_name_plural = ("Sexes")

    def __str__(self):
        return self.name


class Format(models.Model):
    """Format model"""
    name = models.CharField(
        verbose_name=("Игровой формат"),
        max_length=validators.SHORT_STR,
        validators=[validators.validate_format]
    )

    class Meta:
        verbose_name = ("Format")
        verbose_name_plural = ("Formats")

    def __str__(self):
        return self.name


class ContactDetails(models.Model):
    """ContactDetail model"""
    messanger = models.CharField(
        verbose_name="Способ связи",
        help_text="Способ связи",
    )
    main_contact = models.BooleanField(
        verbose_name="Передочтительный способ связи",
        help_text="Передочтительный способ связи",
        default=False,
    )
    contact = models.CharField(
        max_length=validators.MEDIUM_STR,
        blank=False,
        verbose_name="Контактные данные",
        help_text="Введите ваши контактные данные",
    )

    class Meta:
        verbose_name = ("ContactDetail")
        verbose_name_plural = ("ContactDetails")

    def __str__(self):
        return f"{self.messanger}: {self.contact}"


class TeamContactDetails(ContactDetails):
    """TeamContactDetails model"""
    team = models.ForeignKey(
        "Team",
        verbose_name=("Контактные данные"),
        related_name="contact_details",
        on_delete=models.CASCADE,
    )


class City(models.Model):
    """City model"""
    name = models.CharField(
        verbose_name=("Город"),
        max_length=validators.MEDIUM_STR
    )

    class Meta:
        verbose_name = ("City")
        verbose_name_plural = ("Cities")

    def __str__(self):
        return self.name


class EntityBaseModel(models.Model):
    """Base model to create teams and players"""
    format = models.ForeignKey(
        Format,
        on_delete=models.DO_NOTHING,
        related_name="teams",
        blank=False,
        null=False,
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.SET_NULL,
        related_name="%(class)ss",
        blank=False,
        null=True,
    )
    sex = models.ForeignKey(
        Sex,
        on_delete=models.SET_NULL,
        related_name="%(class)ss",
        blank=False,
        null=True,
    )
    password = models.CharField(
        max_length=validators.SHORT_STR,
        verbose_name="Пароль",
        help_text="Введите пароль",
        blank=False,
        null=False,
    )
    photo = models.ImageField(
        verbose_name="Фото",
        help_text="Загрузите фото",
        upload_to="media/",
        blank=True,
    )
    city = models.ForeignKey(
        City,
        on_delete=models.DO_NOTHING,
        related_name="%(class)ss",
        blank=False,
        null=True,
    )
    statistics = models.URLField(
        verbose_name=("Статистика"),
        max_length=validators.LONG_STR,
        help_text="Введите ссылку на статистику",
        blank=True,
    )
    academy = models.CharField(
        verbose_name=("Название комнады или академии"),
        max_length=validators.MEDIUM_STR,
        help_text=("Введите название комнады или академии"),
        balnk=True,
    )

    class Meta:
        verbose_name = ("%(class)s")
        verbose_name_plural = ("%(class)ss")


class Sport(models.Model):
    """Sport model"""
    name = models.CharField(
        unique=True,
        max_length=validators.MEDIUM_STR,
        verbose_name="Вид спорта",
    )

    class Meta:
        verbose_name = ("Sport")
        verbose_name_plural = ("Sports")

    def __str__(self):
        return self.name


class UserDetails(AbstractUser):
    """UserDetails model"""
    first_name = models.CharField(
        max_length=validators.MEDIUM_STR,
        blank=False,
        verbose_name="Имя",
        help_text="Введите имя",
    )
    last_name = models.CharField(
        max_length=validators.MEDIUM_STR,
        blank=False,
        verbose_name="Фамилия",
        help_text="Введите фамилию",
    )
    father_name = models.CharField(
        max_length=validators.MEDIUM_STR,
        verbose_name="Отчество",
        help_text="Введите отчество",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class ManagerPosition(models.Model):
    """ManagerPosition model"""
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


class TeamManager(UserDetails):
    """Team_manager model"""
    postion = models.ForeignKey(
        ManagerPosition,
        blank=False,
        on_delete=models.DO_NOTHING,
    )


class Tournament(models.Model):
    """Tournament model"""
    name = models.CharField(
        max_length=validators.LONG_STR,
        verbose_name="Название команды",
    )

    class Meta:
        verbose_name = ("Tournament")
        verbose_name_plural = ("Tournaments")

    def __str__(self):
        return self.name


class Team(EntityBaseModel):
    """Team model"""
    name = models.CharField(
        max_length=validators.MEDIUM_STR,
        verbose_name="Название команды",
    )
    sport = models.ForeignKey(
        Sport,
        on_delete=models.DO_NOTHING,
        related_name="teams",
        blank=False,
        null=False,
    )
    manager = models.ForeignKey(
        TeamManager,
        on_delete=models.SET_NULL,
        related_name="teams",
        blank=False,
        null=True,
    )
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.SET_NULL,
        related_name="teams",
        blank=False,
        null=True,
    )

    def __str__(self):
        return self.name
