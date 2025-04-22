from django import forms
from .models import Person  # Utilise le bon modèle utilisateur

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': '📧 Entrez votre e-mail'
        })
    )
    mot_de_passe = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '🔒 Mot de passe'
        })
    )


class PredictionForm(forms.Form):
    SEX_CHOICES = [
        ("Homme", "Homme"),
        ("Femme", "Femme"),
    ]

    CONTRACT_CHOICES = [
        ("CDI (Contrat à Durée Indéterminée)", "CDI"),
        ("CDD (Contrat à Durée Déterminée)", "CDD"),
        ("Stage", "Stage"),
        ("Indépendant/Freelance", "Freelance"),
    ]

    sexe = forms.ChoiceField(label="Sexe", choices=SEX_CHOICES)
    age = forms.IntegerField(label="Âge", min_value=16, max_value=100)
    education = forms.CharField(label="Niveau d'éducation", help_text="Ex: Licence, Master, BTS, etc.")
    experience = forms.IntegerField(label="Expérience (années)", min_value=0, max_value=50)
    secteur = forms.CharField(label="Secteur souhaité", help_text="Ex: Informatique, Santé, Finance, etc.")
    salaire = forms.IntegerField(label="Salaire espéré", help_text="Montant en euros (ex: 25000)")
    contrat = forms.ChoiceField(label="Type de contrat souhaité", choices=CONTRACT_CHOICES)



from django.contrib.auth.hashers import make_password

class RegisterForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Person
        fields = ['nom', 'prenom', 'email', 'mot_de_passe']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.mot_de_passe = make_password(self.cleaned_data["mot_de_passe"])
        if commit:
            user.save()
        return user
from django import forms
from django.contrib.auth.hashers import make_password
from .models import Person

# Formulaire pour mettre à jour les informations personnelles
from django import forms
from django.contrib.auth.hashers import make_password
from .models import Person

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['nom', 'prenom', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Si un mot de passe est fourni, il sera haché et mis à jour
        if commit:
            user.save()
        return user

class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ancien mot de passe'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nouveau mot de passe'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer nouveau mot de passe'}))
