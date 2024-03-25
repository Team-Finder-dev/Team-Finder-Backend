from django.db import models



class Player(models.Model): # Здесь наследование от модел просто для примера.
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    photo = models.ImageField(upload_to='players/', null=True, blank=True)
    sex = models.CharField(max_length=100, choices=[('male', 'Мужская'), ('female', 'Женская'),])
    weight = models.PositiveSmallIntegerField(blank=False)
    height = models.PositiveSmallIntegerField(blank=False)
    city = models.CharField(max_length=100)
    statistics = models.URLField(null=True, blank=True)
    academy = models.CharField(max_length=100)
    about = models.TextField(null=True, blank=True)
    level = models.CharField(max_length=100, choices=[('любитель', 'Любитель'), ('профессионал', 'Профессионал')])

    class Meta:
        abstract = True

class Team(models.Model): # Здесь наследование от модел просто для примера.
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teams/', null=True, blank=True)
    sex = models.CharField(max_length=100, choices=[('male', 'Мужская'), ('female', 'Женская'), ('unisex', 'Смешанная'), ])
    contact_person = models.CharField(max_length=100)
    position = models.CharField(max_length=100, choices = [('captain', 'Капитан'), ('administrator', 'Администратор'), ('coach', 'Тренер'), ])
    level = models.CharField(max_length=100, choices=[('любитель', 'Любитель'), ('профессионал', 'Профессионал')])

    class Meta:
        abstract = True

class FootballPlayer(Player):
    ROLE_CHOICES = [
        ('goalkeeper', 'Вратарь'),
        ('right_defender', 'Правый защитник'),
        ('left_defender', 'Левый защитник'),
        ('center_defender', 'Центральный защитник'),
        ('defensive_midfielder', 'Опорный полузащитник'),
        ('central_midfielder', 'Центральный полузащитник'),
        ('right_midfielder', 'Правый полузащитник'),
        ('left_midfielder', 'Левый полузащитник'),
        ('attacking_midfielder', 'Атакующий полузащитник'),
        ('forward', 'Нападающий'),
    ]
    name = models.CharField(max_length=100)
    skils = models.ManyToManyField("FootballCharacteristic", on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(choices = ROLE_CHOICES, on_delete=models.SET_NULL, null=True)
    working_leg = models.CharField(max_length=100, choices=[('right', 'Правая'), ('left', 'Левая'), ('both', 'Обе'),])
    playing_format = models.CharField(choices = [('11 x 11', '11 x 11'), ('8 x 8', '8 x 8'), ('5 x 5', '5 x 5'), ], max_length=100)
    

class FootballFieldPlayer(FootballPlayer):
    best_skills = models.ManyToManyField("FootballFieldCharacteristic", on_delete=models.SET_NULL, null=True)
    worst_skills = models.ManyToManyField("FootballFieldCharacteristic", on_delete=models.SET_NULL, null=True)


class FootballKeeperPlayer(FootballPlayer):
    best_skills = models.ManyToManyField("FootballKeeperCharacteristic", on_delete=models.SET_NULL, null=True)
    worst_skills = models.ManyToManyField("FootballKeeperCharacteristic", on_delete=models.SET_NULL, null=True)


class FootballTeam(Team):
    tournament = models.ManyToManyField("Tournament", on_delete=models.SET_NULL, null=True)
    format = models.CharField(choices = [('11 x 11', '11 x 11'), ('8 x 8', '8 x 8'), ('5 x 5', '5 x 5'), ], max_length=100)


class BasketballPlayer(Player):
    pass

class HockeyPlayer(Player):
    pass

class HockeyFieldPlayer(HockeyPlayer):
    pass

class HockeyKeeperPlayer(HockeyPlayer):
    pass

class Characteristic(models.Model):
    CATEGORY_CHOICES = [
        ('технические', 'Технические'),
        ('физические', 'Физические'),
        ('психологические', 'Психологические'),
    ]
    category = models.CharField(max_length=100, сhoices=CATEGORY_CHOICES)

class FootballFieldCharacteristic(Characteristic):
    # здесь характеристики для полевого игрока
    pass

class FootballKeeperCharacteristic(Characteristic):
    # а тут для вратаря
    pass

class HockeyFieldCharacteristic(Characteristic):
    pass

class HockeyKeeperCharacteristic(Characteristic):
    pass

class BasketballCharacteristic(Characteristic):
    pass

