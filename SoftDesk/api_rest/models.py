from django.db import models

from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


class Users(AbstractUser):
    pass


class Contributor(models.Model):
    """
    Class intermediate between the tables Users and Projects
    """
    # Valeur sauvegardée
    AUTHOR = "Auteur"
    RESPONSABLE = "Responsable"
    CREATOR = "Créateur"
    # tuple (valeur, label)
    ROLE_CHOICES = [
        (AUTHOR, "Auteur"),
        (RESPONSABLE, "Responsable"),
        (CREATOR, "Créateur")
    ]

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to="Projects", on_delete=models.CASCADE)
    role = models.CharField(max_length=11, choices=ROLE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'project'], name="unique_project_user")
        ]


class Projects(models.Model):
    title = models.CharField(max_length=30)
    contributors = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through=Contributor)
    type = models.CharField(max_length=30)
    description = models.CharField(max_length=128)


class Issues(models.Model):
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
    tag = models.CharField(max_length=12, choices=TAG_CHOICE)
    priority = models.CharField(max_length=7, choices=PRIORITY_CHOICE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICE)
    
    author = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="author")
    assignee = models.ForeignKey(to=Users, on_delete=models.CASCADE, default=author, related_name="assignee")

    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.CharField(max_length=128)
    author = models.ForeignKey(to=Users, on_delete=models.CASCADE,)
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
