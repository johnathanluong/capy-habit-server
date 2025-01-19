from django.db import models
from django.contrib.auth.models import AbstractUser

gacha_cost = 50

class CustomUser(AbstractUser):
    # Extention of the default user model
    email = models.EmailField(unique=True)
    display_name = models.CharField(
        max_length=100,
        default=''
        )
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        help_text="The timezone the user resides in")
    completed_habits = models.IntegerField(
        default=0,
        help_text="The number of completed habits a user has")
    last_login = models.DateTimeField(
        auto_now=True,
        help_text="Gets the last login for the user")
    points = models.PositiveIntegerField(
        default=0,
        help_text="The number of points a user has, obtained from completing habits and keeping up streaks")
    level = models.PositiveIntegerField(default=1)
    experience_points = models.PositiveIntegerField(default=0)
    xp_for_level = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return f"Username: {self.username}, Display Name: {self.display_name}"
    
    def levelUp(self):
        self.level += 1
        self.experience_points -= self.xp_for_level
        self.xp_for_level += 10
        
    def checkLevelUp(self):
        if self.experience_points >= self.xp_for_level:
            self.levelUp()
            return True
        return False
    
    def completeHabit(self):
        awarded_xp = 5 + (self.level - 1)
        awarded_points = 10 + (self.level - 1)
        self.experience_points += awarded_xp
        self.points += awarded_points
        self.checkLevelUp()       
    
    def get_accessories(self):
        return self.user_accessories.all()
    
    def pull(self):
        if self.points >= gacha_cost:
            self.points -= gacha_cost
