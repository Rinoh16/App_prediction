import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
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

# Séparation train / test (80% / 20%)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Entraînement du modèle sur le training set
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Sauvegarder le modèle entraîné
with open("ml_model.sav", "wb") as f:
    pickle.dump(model, f)
