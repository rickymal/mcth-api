from django.db import models

from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


class Challenge(models.Model):
    name = models.CharField(max_length=20)
    empresa_desafiadora = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self,):
        return self.name


# Este objeto pode conter Juizes repetidos
class Judge(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

    def __str__(self,):
        return self.user_id.first_name + " " + self.user_id.last_name


class Team(models.Model):
    challenge = models.ForeignKey(
        Challenge, on_delete=models.SET_NULL, null=True, blank=True)
    noteJudger = models.FloatField(default=0.0)
    judger_assign = models.ForeignKey(
        Judge, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    link_project = models.TextField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Team {self.id} for [{self.challenge_id}] challenge "


class Student(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    team_id = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True)
    isLeader = models.BooleanField()

    def __str__(self):
        return self.user_id.first_name + " " + self.user_id.last_name


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Um mentor esta associado a um desafio
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

    def __str__(self):
        if self.user is None:
            return "None"
        return self.user.first_name + " " + self.user.last_name


class Mentoring(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, blank=True)
    time_meeting = models.DateTimeField()

    def __str__(self):

        response = f"[Mentoria] : {self.mentor.user.first_name}"
        if self.team is not None:
            m = f" para equipe {self.team.id}"
        else:
            m = " sem equipe a mentorar"
        response += m
        return response
