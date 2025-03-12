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
from sklearn.preprocessing import OneHotEncoder  # For encoding categorical features using one-hot encoding

# Scikit-learn: Machine learning model
from sklearn.ensemble import RandomForestClassifier  # For building random forest models

# Scikit-learn: Tree visualization
from sklearn.tree import export_graphviz  # For exporting decision trees in DOT format
from sklearn.tree import plot_tree  # For plotting decision trees

# Load the dataset
csv_path = "thyroid_data (1).csv"  # Update with your file path
df = pd.read_csv(csv_path)

# Label encoding yes/no values
mapping = {'No': 0, 'Yes': 1}
boolean_columns = ['Smoking', 'Hx Smoking', 'Hx Radiotherapy', 'Recurred']
df[boolean_columns] = df[boolean_columns].applymap(lambda x: mapping.get(x, x))

# Encode features with only 2 values
le = LabelEncoder()
columns_to_encode = ['Gender', 'Focality', 'M']
for column in columns_to_encode:
    df[column] = le.fit_transform(df[column])

# Encoding with an order
mappings = {
    'Physical Examination': {'Normal': 0, 'Diffuse goiter': 1, 'Single nodular goiter-left': 2, 
                             'Single nodular goiter-right': 3, 'Multinodular goiter': 4},
    'Adenopathy': {'No': 0, 'Right': 1, 'Left': 1, 'Posterior': 2, 'Bilateral': 3, 'Extensive': 4},
    'Pathology': {'Micropapillary': 0, 'Papillary': 1, 'Follicular': 2, 'Hurthle cell': 3},
    'T': {'T1a': 0, 'T1b': 1, 'T2': 2, 'T3a': 3, 'T3b': 4, 'T4a': 5, 'T4b': 6},
    'N': {'N0': 0, 'N1a': 1, 'N1b': 2},
    'Stage': {'I': 0, 'II': 1, 'III': 2, 'IVA': 3, 'IVB': 4},
    'Response': {'Excellent': 0, 'Indeterminate': 1, 'Biochemical Incomplete': 2, 'Structural Incomplete': 3}
}

for col, mapping in mappings.items():
    df[col] = df[col].map(mapping)

# One-hot encoding for 'Thyroid Function'
ohe = OneHotEncoder()
feature_array = ohe.fit_transform(df[['Thyroid Function']]).toarray()
feature_labels = np.array(ohe.categories_).ravel()
features = pd.DataFrame(feature_array, columns=feature_labels)

df = pd.concat([df, features], axis=1)
df = df.drop(['Thyroid Function'], axis='columns')

df = df[['Response', 'Adenopathy', 'N', 'T', 'Recurred']]
df.head()

# Split into training and testing
inputs = df.drop('Recurred', axis='columns')
target = df['Recurred']
X_train, X_test, y_train, y_test = train_test_split(inputs, target, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate the model
print("Model Accuracy:", model.score(X_test, y_test))

# Predictions
y_pred = model.predict(X_test)

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
y_prob = model.predict_proba(X_test)[:, 1]
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
max_depth = 2
feature_names = list(inputs.columns)

plt.figure(figsize=(20, 10))
plot_tree(model.estimators_[tree_number], feature_names=feature_names, max_depth=max_depth, filled=True)
plt.show()

import joblib
joblib.dump(model, "thyroid_cancer_model.pkl")