from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Charger le modèle
model = joblib.load('model/PredictionPrixMaison.pkl')

# Codes postaux disponibles (extraits du fichier CSV)
CODES_POSTAUX = [36372, 60002, 60016, 60046, 62025, 62034, 62088, 62214, 62234, 62249,
                 81418, 81521, 81524, 85255, 85262, 85266, 85331, 85377, 90038, 90211,
                 90265, 90803, 91752, 91901, 91915, 92021, 92040, 92253, 92276, 92543,
                 92677, 92692, 92802, 92880, 93105, 93111, 93314, 93446, 93510, 93720,
                 93924, 94501, 94531, 94565, 94568, 95008, 95220, 96019, 98021]

@app.route('/', methods=['GET', 'POST'])
def index():
    prix = None
    erreur = None

    if request.method == 'POST':
        chambres = int(request.form['chambres'])
        salles_bain = float(request.form['salles_bain'])
        surface = float(request.form['surface'])
        code_postal = int(request.form['code_postal'])

        # Vérifier les valeurs minimales
        if chambres < 1 or salles_bain < 1 or surface < 100:
            erreur = "Valeurs invalides! Veuillez respecter: Chambres: minimum 1 | Salles de bain: minimum 1 | Surface: minimum 100m²"
        else:
            # Préparer les données
            nouvelle_maison = np.array([[chambres, salles_bain, surface, code_postal]])

            # Prédiction
            prix = model.predict(nouvelle_maison)[0]
            
            # Vérification supplémentaire si le modèle retourne un prix négatif
            if prix < 0:
                erreur = "Le modèle a donné un prix invalide. Veuillez vérifier vos données sont minimum."
                prix = None

    return render_template('index.html', prix=prix, erreur=erreur, codes_postaux=CODES_POSTAUX)

if __name__ == '__main__':
    app.run(debug=True)
