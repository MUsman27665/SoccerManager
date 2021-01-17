from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'admin'),
      (2, 'organizer'),
      (3, 'captain'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    name = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=100, default="")
    phone_number = models.CharField(max_length=15, default='1')
    email = models.EmailField(default="example@gmail.com")


class Gallery(models.Model):
    description = models.CharField(max_length=500, default="")
    image = models.ImageField(upload_to='gallery', null=True, blank=True)


class Team(models.Model):
    Captain_name = models.ForeignKey(User, on_delete=models.CASCADE, max_length=100, default="")
    team_player_1 = models.CharField(max_length=100, default="")
    team_player_2 = models.CharField(max_length=100, default="")
    team_player_3 = models.CharField(max_length=100, default="")
    team_player_4 = models.CharField(max_length=100, default="")
    team_player_5 = models.CharField(max_length=100, default="")
    team_player_6 = models.CharField(max_length=100, default="")
    team_player_7 = models.CharField(max_length=100, default="")
    team_player_8 = models.CharField(max_length=100, default="")
    team_player_9 = models.CharField(max_length=100, default="")
    team_player_10 = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.Captain_name.name


class Tournament(models.Model):
    T_name = models.CharField(max_length=100, default="")
    T_owner = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    Start_date = models.DateField(max_length=100, default='2020-12-12')
    End_date = models.DateField(max_length=100, default='2020-12-12')
    no_of_matches = models.DecimalField(max_length=100, default="1", max_digits=5, decimal_places=3)
    no_of_teams = models.DecimalField(max_length=15, default='1', max_digits=5, decimal_places=3)
    teams = models.ManyToManyField(Team, related_name='teams', blank=True)

    def __str__(self):
        return self.T_name


class Match(models.Model):
    Match_team1 = models.ForeignKey(Team, on_delete=models.CASCADE, default=0, related_name="TeamOne")
    Match_team2 = models.ForeignKey(Team, on_delete=models.CASCADE, default=0, related_name="TeamTwo")
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, default=1, related_name='tournament')
    Date = models.DateField(max_length=100, default='2020-12-12')
    Result = models.CharField(max_length=15, default='1')

    def __str__(self):
        return self.Result


class TournamentRequest(models.Model):
    tournament_request_status_choice = [
        ('Initiated', 'Initiated'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    to_organizer = models.ForeignKey(User, on_delete=models.CASCADE, default=0, related_name="organizer")
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, default=0, related_name="TeamTwo")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=1, related_name='tournament')
    status = models.CharField(choices=tournament_request_status_choice, default='Initiated', max_length=20)

    def __str__(self):
        return self.team.Captain_name.username
