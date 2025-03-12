# Data manipulation and numerical operations
import pandas as pd   # For data manipulation and analysis
import numpy as np    # For numerical operations

# Data visualization libraries
import matplotlib.pyplot as plt   # For plotting and visualizations
import seaborn as sns   # For statistical data visualization

# Scikit-learn: Model selection and evaluation
from sklearn.model_selection import train_test_split   # For splitting the data into training and testing sets
from sklearn.metrics import accuracy_score, classification_report  # For evaluating model performance
from sklearn.metrics import roc_curve, roc_auc_score  # For calculating ROC curve and AUC

# Scikit-learn: Preprocessing
from sklearn.preprocessing import LabelEncoder   # For encoding categorical labels into numeric values

# Scikit-learn: Machine learning model
from sklearn.ensemble import RandomForestClassifier  # For building random forest models

# Scikit-learn: Tree visualization
from sklearn.tree import plot_tree  # For plotting decision trees

# Load the dataset
csv_path = "survey lung cancer.csv"  # Update with your actual file path
df = pd.read_csv(csv_path)

# Encode the target variable ('LUNG_CANCER')
df['LUNG_CANCER'] = df['LUNG_CANCER'].map({'YES': 1, 'NO': 0})

mapping = {'Male': 1, 'Female': 2}
boolean_columns = ['GENDER']
df[boolean_columns] = df[boolean_columns].applymap(lambda x: mapping.get(x, x))

df = df[['AGE', 'ALCOHOL CONSUMING', 'ALLERGY ', 'PEER_PRESSURE', 'LUNG_CANCER']]
df.head()

# Split features and target variable
inputs = df.drop('LUNG_CANCER', axis=1)
target = df['LUNG_CANCER']

# Identify categorical columns
categorical_columns = inputs.select_dtypes(include=['object']).columns

#Encode categorical columns using LabelEncoder
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    inputs[col] = le.fit_transform(inputs[col])  # Convert to numeric values
    label_encoders[col] = le  # Store encoder for future use

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(inputs, target, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.2f}")
print(df.columns)

# Predictions
y_pred = model.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Feature importance plot
importances = model.feature_importances_
indices = np.argsort(importances)

plt.figure(figsize=(10, 6))
plt.title('Feature Importances')
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [inputs.columns[i] for i in indices])
plt.xlabel('Relative Importance')
plt.show()

# ROC Curve
y_prob = model.predict_proba(X_test)[:, 1]  # Probability of class 1
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
auc_score = roc_auc_score(y_test, y_prob)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', label=f'ROC Curve (AUC = {auc_score:.2f})')
plt.plot([0, 1], [0, 1], color='red', linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

# Decision tree visualization
tree_number = 0
max_depth = 3
feature_names = list(inputs.columns)

plt.figure(figsize=(20, 10))
plot_tree(model.estimators_[tree_number], feature_names=feature_names, max_depth=max_depth, filled=True)
plt.show()

import joblib
joblib.dump(model, "lung_cancer_model.pkl")
