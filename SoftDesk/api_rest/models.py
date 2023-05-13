from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


class Users(AbstractUser):
    email = models.EmailField(unique=True, blank=True, max_length=254, verbose_name='email address')

    def __str__(self):
        return f"{self.username}"


class Contributors(models.Model):
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
    project = models.ForeignKey(to="Projects", on_delete=models.CASCADE, related_name="project")
    role = models.CharField(max_length=11, choices=ROLE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'project'], name="unique_project_user")
        ]
        verbose_name = "Contributor"
        verbose_name_plural = "Contributors"

    def __str__(self):
        return f"{self.user}"


class Projects(models.Model):
    SITE = "Site web"
    ANDROID = "Applications Android"
    IOS = "iOS"

    PLATFORM_CHOICE = [
        (SITE, "Site web"),
        (ANDROID, "Applications Android"),
        (IOS, "iOS")
    ]

    title = models.CharField(max_length=30)
    contributors = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through=Contributors)
    type = models.CharField(max_length=30, choices=PLATFORM_CHOICE)
    description = models.CharField(max_length=128)

    def __str__(self):
        return f"Projet: {self.title}"

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


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
    assignee = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="assignee")

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Problème: {self.title}"

    class Meta:
        verbose_name = "Issue"
        verbose_name_plural = "Issues"


class Comments(models.Model):
    description = models.CharField(max_length=128)
    author = models.ForeignKey(to=Users, on_delete=models.CASCADE, )
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire pour le problème: {self.issue.title}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
