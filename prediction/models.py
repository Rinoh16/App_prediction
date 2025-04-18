from django.db import models
from django.db import models

class Person(models.Model):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    mot_de_passe = models.CharField(max_length=128, default='test123')


    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Student(models.Model):
    GENDER_CHOICES = [
        ("M", "Masculin"),
        ("F", "Feminin"),
    ]

    CONTRACT_CHOICES = [
        ("CDI", "CDI"),
        ("CDD", "CDD"),
        ("Stage", "Stage"),
        ("Freelance", "Freelance"),
    ]

    EMPLOYMENT_STATUS_CHOICES = [
        (1, "Employé"),
        (0, "Non Employé"),
    ]

    name = models.CharField(max_length=255, default="Nom inconnu")  # Nom complet
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")  # Sexe
    age = models.IntegerField(default=18)  # Âge
    education_level = models.CharField(max_length=100, default="Baccalauréat")  # Niveau d'éducation
    years_experience = models.IntegerField(default=0)  # Expérience (années)
    desired_sector = models.CharField(max_length=100, default="Informatique")  # Secteur souhaité
    expected_salary = models.FloatField(default=0.0)  # Salaire espéré
    desired_contract = models.CharField(max_length=50, choices=CONTRACT_CHOICES, default="CDI")  # Type de contrat souhaité
    employment_status = models.IntegerField(choices=EMPLOYMENT_STATUS_CHOICES, null=True, blank=True)  # Statut d'emploi (1 = Employé, 0 = Non Employé)

    def __str__(self):
        return self.name

