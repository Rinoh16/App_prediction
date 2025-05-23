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
from .forms import LoginForm, PredictionForm, RegisterForm, UserUpdateForm



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
    user = request.session.get('user')  # récupère les infos stockées lors du login
    return render(request, 'prediction/home.html', {'user': user})

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
    matplotlib.use('Agg')  # Évite l'erreur Tkinter
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # Pour 3D
    import seaborn as sns
    import pandas as pd
    import io
    import base64

    # Chargement du dataset
    df = pd.read_csv("dataset_statut_emploi_final.csv", encoding="utf-8-sig", sep=';')

    # Style professionnel
    sns.set(style="whitegrid", palette="Set2", font_scale=1.2)

    graph_type = request.GET.get('graph', 'age_distribution')
    fig = plt.figure(figsize=(8, 5))
    
    # Graphiques améliorés
    if graph_type == 'age_distribution':
        sns.histplot(df['Âge'], kde=True, bins=25, color="skyblue", edgecolor="black")
        plt.title("Répartition des âges", fontsize=14)
        plt.xlabel("Âge", fontsize=12)
        plt.ylabel("Nombre", fontsize=12)
        plt.grid(True)

    elif graph_type == 'salary_boxplot':
        sns.boxplot(x=df['Salaire espéré'], color='lightcoral')
        plt.title("Boxplot des salaires espérés", fontsize=14)
        plt.xlabel("Salaire Espéré", fontsize=12)
        plt.grid(True)

    elif graph_type == 'experience_salary':
        sns.scatterplot(x='Expérience (années)', y='Salaire espéré', data=df, hue='Statut d\'emploi', palette='coolwarm', s=80)
        plt.title("Expérience vs Salaire (par Statut)", fontsize=14)
        plt.xlabel("Expérience (années)", fontsize=12)
        plt.ylabel("Salaire Espéré", fontsize=12)
        plt.grid(True)

    elif graph_type == 'status_experience':
        sns.boxplot(x="Statut d'emploi", y="Expérience (années)", data=df, palette="muted")
        plt.title("Statut d'emploi vs Expérience", fontsize=14)
        plt.xlabel("Statut d'emploi", fontsize=12)
        plt.ylabel("Expérience (années)", fontsize=12)
        plt.grid(True)

    elif graph_type == 'status_education':
        sns.countplot(x="Niveau d'éducation", hue="Statut d'emploi", data=df, palette="Set1")
        plt.title("Statut d'emploi par Niveau d'éducation", fontsize=14)
        plt.xlabel("Niveau d'éducation", fontsize=12)
        plt.ylabel("Nombre", fontsize=12)
        plt.xticks(rotation=30)
        plt.grid(True)

    elif graph_type == '3d_experience_salary':
        ax = fig.add_subplot(111, projection='3d')
        color_map = {"Employé": "green", "Non Employé": "red"}
        colors = df["Statut d'emploi"].map(color_map)

        ax.scatter(df["Expérience (années)"], df["Âge"], df["Salaire espéré"], c=colors, s=50)
        ax.set_xlabel("Expérience (années)")
        ax.set_ylabel("Âge")
        ax.set_zlabel("Salaire espéré")
        ax.set_title("Graphique 3D: Expérience, Âge, Salaire", fontsize=14)

    else:
        plt.text(0.5, 0.5, "Graphique non reconnu", ha='center', fontsize=14)

    # Sauvegarde en mémoire
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=120)
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, 'prediction/visualisation.html', {
        'img_data': img_data,
        'graph_type': graph_type
    })


from django.shortcuts import render, redirect
from .forms import UserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Person
@login_required_session
def update_profile(request):
    user_data = request.session.get('user')
    if not user_data:
        return redirect('login')
    
    try:
        user = Person.objects.get(email=user_data['email'])
    except Person.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Mettre à jour les données de session après modification
            request.session['user'] = {
                'email': user.email,
                'nom': user.nom,
                'prenom': user.prenom,
            }
            messages.success(request, "Votre profil a été mis à jour !")
            return redirect('update_profile')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'prediction/update_profile.html', {'form': form})

@login_required_session
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            email = request.session.get('user', {}).get('email')
            try:
                user = Person.objects.get(email=email)
            except Person.DoesNotExist:
                messages.error(request, "Utilisateur introuvable.")
                return redirect('login')

            if check_password(form.cleaned_data['old_password'], user.mot_de_passe):
                user.mot_de_passe = make_password(form.cleaned_data['new_password1'])
                user.save()
                messages.success(request, "Votre mot de passe a été changé avec succès !")
                return redirect('login')
            else:
                form.add_error('old_password', 'Ancien mot de passe incorrect')
    else:
        form = CustomPasswordChangeForm()

    return render(request, 'prediction/change_password.html', {'form': form})