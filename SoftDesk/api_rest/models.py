from django.db import models

from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


class Users(AbstractUser):
    pass


class Contributor(models):
    """
    Class intermediate between the tables Users and Projects
    """
    AUTHOR = "Auteur"
    RESPONSABLE = "Responsable"
    CREATOR = "Créateur"

    ROLE_CHOICES = [
        (AUTHOR, "Auteur"),
        (RESPONSABLE, "Responsable"),
        (CREATOR, "Créateur")
    ]

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    projects = models.ManyToManyField(to="Projects")
    role = models.CharField(choices=ROLE_CHOICES)


class Projects(models):
    title = models.CharField(max_length=30)
    contributors = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through=Contributor)
    type = models.CharField(max_length=30)
    description = models.CharField(max_length=128)


class Issues(models):
    BUG = "Bug"
    TASK = "Tâche"
    AMELIORATION = "Amélioration"

    LOW = "Faible"
    MEDIUM = "Moyenne"
    STRONG = "Haute"

    TO_DO = "A faire"
    IN_PROGRESS = "En cours"
    FINISHED = "Terminé"

    TAG_CHOICE = [
        (BUG, "Bug"),
        (TASK, "Tâche"),
        (AMELIORATION, "Amélioration")
    ]

    PRIORITY_CHOICE = [
        (LOW, "Faible"),
        (MEDIUM, "Moyenne"),
        (STRONG, "Haute")
    ]

    STATUS_CHOICE = [
        (TO_DO, "A faire"),
        (IN_PROGRESS, "En cours"),
        (FINISHED, "Terminé")
    ]

    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=128)
    # A voir si défaut pour les choix
    tag = models.CharField(choices=TAG_CHOICE)
    status = models.CharField(choices=STATUS_CHOICE)
    priority = models.CharField(choices=PRIORITY_CHOICE)

    author = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    assignee = models.ForeignKey(to=Users, on_delete=models.CASCADE, default=author)

    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models):
    description = models.CharField(max_length=128)
    author = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
