# prediction/ml_models.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

# Charger les données
df = pd.read_csv("dataset_statut_emploi_final.csv", encoding="utf-8-sig", sep=';')

# Encodage des colonnes catégorielles
label_encoders = {}
categorical_columns = ["Sexe", "Niveau d'éducation", "Secteur souhaité", "Type de contrat souhaité"]

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Sauvegarder les encoders
with open("label_encoders.sav", "wb") as f:
    pickle.dump(label_encoders, f)

# Séparation des données
X = df.drop(columns=["Statut d'emploi", "Nom complet"])
y = df["Statut d'emploi"]

# Normalisation
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Sauvegarder le scaler
with open("scaler.sav", "wb") as f:
    pickle.dump(scaler, f)

# Entraînement du modèle
model = RandomForestClassifier(random_state=42)
model.fit(X_scaled, y)

# Sauvegarder le modèle
with open("ml_model.sav", "wb") as f:
    pickle.dump(model, f)
