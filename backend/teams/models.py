from api import validators
from django.contrib.auth.models import AbstractUser
from django.db import models


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


class Level(models.Model):
    """Level model"""
    name = models.CharField(
        verbose_name=("Статус"),
        max_length=validators.MEDIUM_STR,
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
        max_length=validators.MEDIUM_STR,
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
        validators=[validators.validate_format],
    )

    class Meta:
        verbose_name = ("Format")
        verbose_name_plural = ("Formats")

    def __str__(self):
        return self.name


class Messanger(models.Model):
    """Messanger model"""
    name = models.CharField(
        verbose_name="Способ связи",
        help_text="Способ связи",
        max_length=validators.SHORT_STR,
    )
    logo = models.ImageField(
        verbose_name="Логотип",
        help_text="Загрузите логотип",
        upload_to="media/",
        blank=True,
    )

    class Meta:
        verbose_name = ("Messanger")
        verbose_name_plural = ("Messangers")

    def __str__(self):
        return self.name


class ContactDetails(models.Model):
    """ContactDetail model"""
    messanger = models.ForeignKey(
        Messanger,
        on_delete=models.CASCADE,
        related_name="contact_details",
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


class EntityBaseModel(AbstractUser):
    """Base model to create teams and players"""
    # Define the USERNAME_FIELD attribute
    USERNAME_FIELD = "registration_phone_number"
    email = None
    registration_phone_number = models.CharField(
        max_length=validators.MEDIUM_STR,
        unique=True,
        blank=False,
        verbose_name="Телефон",
        help_text="+7-911-123-45-67",
        validators=[validators.validate_phone_number],
    )
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
        blank=True,
    )
    sport = models.ForeignKey(
        Sport,
        on_delete=models.SET_NULL,
        related_name="%(class)ss",
        blank=False,
        null=True,
    )
    format = models.ForeignKey(
        Format,
        on_delete=models.SET_NULL,
        related_name="%(class)ss",
        blank=False,
        null=True,
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
    photo = models.ImageField(
        verbose_name="Фото",
        help_text="Загрузите фото",
        upload_to="media/",
        blank=True,
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
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
        verbose_name=("Название команды или академии"),
        max_length=validators.MEDIUM_STR,
        help_text=("Введите название команды или академии"),
        blank=True,
    )

    class Meta:
        verbose_name = ("%(class)s")
        verbose_name_plural = ("%(class)ss")


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
    manager = models.ForeignKey(
        ManagerPosition,
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
