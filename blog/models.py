from django.db import models

class Player(models.Model):
    CATEGORY_CHOICES = [
        ('novice', 'Новичок'),
        ('amateur', 'Любитель'),
        ('pro', 'Профессионал'),
    ]

    username = models.CharField(max_length=100, unique=True)
    age = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    password = models.CharField(max_length=100)

    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)
    stars = models.PositiveIntegerField(default=0)

    def add_win(self):
        self.wins += 1
        # За каждые 3 победы — 1 звезда
        if self.wins % 3 == 0:
            self.stars += 1
        self.save()
        
    def __str__(self):
        return f"{self.username} ({self.get_category_display()})"
