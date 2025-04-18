import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Charger ton dataset
df = pd.read_csv("dataset_statut_emploi_final.csv", encoding="utf-8-sig", sep=';')  # chemin vers tes données

# Séparer X et y
X = df.drop(columns=["Statut d'emploi"])
y = df["Statut d'emploi"]

# Encoder les colonnes catégorielles
label_encoders = {}
for column in X.columns:
    if X[column].dtype == "object":
        le = LabelEncoder()
        X[column] = le.fit_transform(X[column])
        label_encoders[column] = le

# Encoder la target aussi (optionnel selon ton modèle)
target_encoder = LabelEncoder()
y = target_encoder.fit_transform(y)
label_encoders["target"] = target_encoder

# Entraîner le modèle
model = RandomForestClassifier()
model.fit(X, y)

# Sauvegarder le modèle
joblib.dump(model, "model.joblib")

# Sauvegarder les encoders
joblib.dump(label_encoders, "label_encoders.joblib")
