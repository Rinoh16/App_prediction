from django.shortcuts import render, redirect
from .models import Student, Person
from .forms import LoginForm, PredictionForm, RegisterForm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from sklearn.ensemble import RandomForestClassifier
from django.contrib.auth.hashers import check_password, make_password
import pandas as pd
import numpy as np
from .utils import login_required_session


# Login view
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            try:
                user = Person.objects.get(email=email)
                if check_password(mot_de_passe, user.mot_de_passe):
                    request.session['user'] = {
                        'email': user.email,
                        'nom': user.nom,
                        'prenom': user.prenom,
                    }
                    return redirect('/home')
                else:
                    form.add_error(None, "Mot de passe incorrect.")
            except Person.DoesNotExist:
                form.add_error(None, "Utilisateur introuvable.")
        return render(request, 'prediction/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'prediction/login.html', {'form': form})

# Register view
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.mot_de_passe = make_password(form.cleaned_data['mot_de_passe'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'prediction/register.html', {'form': form})

# Home view
@login_required_session
def home(request):
    return render(request, 'prediction/home.html')

# prediction/views.py
def logout(request):
    request.session.flush()
    return redirect('login')  # ou 'login' si tu as une URL nommée

import pickle
import numpy as np
import pandas as pd
from django.shortcuts import render
@login_required_session
def predict_status(request):
    if request.method == "POST":
        # Récupérer les données du formulaire
        sexe = request.POST.get("sexe")
        age = float(request.POST.get("age"))
        education = request.POST.get("education")
        experience = float(request.POST.get("experience"))
        secteur = request.POST.get("secteur")
        salaire = float(request.POST.get("salaire"))
        contrat = request.POST.get("contrat")

        # Charger les objets picklés
        with open("ml_model.sav", "rb") as f:
            model = pickle.load(f)

        with open("scaler.sav", "rb") as f:
            scaler = pickle.load(f)

        with open("label_encoders.sav", "rb") as f:
            label_encoders = pickle.load(f)

        # Encodage des données
        encoded_input = [
            label_encoders["Sexe"].transform([sexe])[0],
            age,
            label_encoders["Niveau d'éducation"].transform([education])[0],
            experience,
            label_encoders["Secteur souhaité"].transform([secteur])[0],
            salaire,
            label_encoders["Type de contrat souhaité"].transform([contrat])[0]
        ]

        # Mise à l'échelle
        scaled_input = scaler.transform([encoded_input])

        # Prédiction
        prediction = model.predict(scaled_input)[0]
        statut = "Employé" if prediction == 1 else "Non Employé"

        return render(request, "prediction/prediction_result.html", {"statut": statut})

    return render(request, "prediction/predict_form.html")



# Visualisation view
@login_required_session
def visualisation(request):
    import matplotlib
    matplotlib.use('Agg')  # Pour éviter l'erreur Tkinter

    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import io
    import base64

    df = pd.read_csv("dataset_statut_emploi_final.csv", encoding="utf-8-sig", sep=';')
    graph_type = request.GET.get('graph', 'age_distribution')

    plt.figure(figsize=(6, 4))
    if graph_type == 'age_distribution':
        sns.histplot(df['Âge'], kde=True, bins=20)
        plt.title("Répartition des âges")
        plt.xlabel("Âge")
        plt.ylabel("Fréquence")

    elif graph_type == 'salary_boxplot':
        sns.boxplot(x=df['Salaire espéré'])
        plt.title("Boxplot des salaires espérés")
        plt.xlabel("Salaire Espéré")

    elif graph_type == 'experience_salary':
        sns.scatterplot(x=df['Expérience (années)'], y=df['Salaire espéré'])
        plt.title("Expérience vs Salaire")
        plt.xlabel("Expérience (années)")
        plt.ylabel("Salaire Espéré")

    elif graph_type == 'status_experience':
        sns.boxplot(x=df["Statut d'emploi"], y=df["Expérience (années)"])
        plt.title("Statut d'emploi vs Expérience")
        plt.xlabel("Statut d'emploi")
        plt.ylabel("Expérience (années)")

    elif graph_type == 'status_education':
        sns.countplot(x=df["Niveau d'éducation"], hue=df["Statut d'emploi"])
        plt.title("Statut d'emploi vs Niveau d'éducation")
        plt.xlabel("Niveau d'éducation")
        plt.ylabel("Nombre")
        plt.xticks(rotation=30)

    else:
        plt.text(0.5, 0.5, "Graphique non reconnu", ha='center')

    # Sauvegarder en mémoire
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')

    return render(request, 'prediction/visualisation.html', {
        'img_data': img_data,
        'graph_type': graph_type
    })
