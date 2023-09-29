from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

def feature_importance(df, list_X, col_y, reg=True, mdi=True, mda=True, sfi=True):
    """Compute and plot feature importances using various methods.
    
    Parameters:
    df (DataFrame): The dataframe containing the features and target.
    list_X (list): The list of feature column names.
    col_y (str): The name of the target column.
    """
    
    # Make a copy of the dataframe and drop rows with NA values
    df_copy = df[list_X + [col_y]].dropna()
    df_copy = df_copy[~np.isinf(df_copy).any(axis=1)]
    
    # Create feature matrix X and target vector y
    X = df_copy[list_X].iloc[:-1,:].values
    y = df_copy[col_y].iloc[1:].values
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train a RandomForest model
    if reg:
        model = RandomForestRegressor(max_depth=3, random_state=42)
    else:
        model = RandomForestClassifier(max_depth=3, random_state=42)
    
    model.fit(X_train, y_train)
    
    # --- MDI (Mean Decrease Impurity) ---
    if mdi:
        importances = model.feature_importances_
        feature_names = list_X
        forest_importances = pd.Series(importances, index=feature_names)

        # Sort feature importances in ascending order for horizontal bar plot
        sorted_importances = forest_importances.sort_values(ascending=True)

        fig, ax = plt.subplots(figsize=(15, len(list_X) // 3))
        sorted_importances.plot.barh(ax=ax, color="#88A5E7", edgecolor="black")
        ax.set_title("Feature importances using MDI")
        ax.set_xlabel("Mean Decrease in Impurity")
        fig.tight_layout()
        plt.show()
    
    # --- MDA (Mean Decrease Accuracy) ---
    if mda:
        # Compute initial accuracy (MSE) of the model
        y_pred = model.predict(X_test)
        initial_accuracy = mean_squared_error(y_test, y_pred)

        feature_importance_mda = {}

        for i, column in enumerate(list_X):
            X_test_new = np.delete(X_test, i, axis=1)
            X_train_new = np.delete(X_train, i, axis=1)

            model_new = RandomForestRegressor(random_state=42)
            model_new.fit(X_train_new, y_train)

            y_pred_new = model_new.predict(X_test_new)
            new_accuracy = mean_squared_error(y_test, y_pred_new)

            feature_importance_mda[column] = initial_accuracy - new_accuracy

        feature_importance_mda_series = pd.Series(feature_importance_mda)
        sorted_importances_mda = feature_importance_mda_series.sort_values(ascending=True)

        fig, ax = plt.subplots(figsize=(15, len(list_X) // 3))
        sorted_importances_mda.plot.barh(ax=ax, color="#88A5E7", edgecolor="black")
        ax.set_title("Feature importances using MDA")
        ax.set_xlabel("Mean Decrease in MSE")
        fig.tight_layout()
        plt.show()

    # --- SFI (Single Feature Importance) ---
    if sfi:
        feature_importance_sfi = {}

        for i, column in enumerate(list_X):
            X_train_single = X_train[:, i].reshape(-1, 1)
            X_test_single = X_test[:, i].reshape(-1, 1)

            model_single = RandomForestRegressor(random_state=42)
            model_single.fit(X_train_single, y_train)

            y_pred_single = model_single.predict(X_test_single)
            single_accuracy = mean_squared_error(y_test, y_pred_single)

            feature_importance_sfi[column] = single_accuracy

        feature_importance_sfi_series = pd.Series(feature_importance_sfi)
        sorted_importances_sfi = feature_importance_sfi_series.sort_values(ascending=True)

        fig, ax = plt.subplots(figsize=(15, len(list_X) // 3))
        sorted_importances_sfi.plot.barh(ax=ax, color="#88A5E7", edgecolor="black")
        ax.set_title("Feature importances using SFI")
        ax.set_xlabel("Mean Decrease in MSE")
        fig.tight_layout()
        plt.show()

def linear_models_importance(df, list_X, col_y, reg=True):
    df_copy = df[list_X + [col_y]].dropna()
    df_copy = df_copy[~np.isinf(df_copy).any(axis=1)]

    # Create feature matrix X and target vector y
    X = df_copy[list_X].iloc[:-1,:].values
    y = df_copy[col_y].iloc[1:].values

    sc = StandardScaler()
    X_sc = sc.fit_transform(X)

    # Diviser les données en ensembles d'apprentissage et de test
    X_train, X_test, y_train, y_test = train_test_split(X_sc, y, test_size=0.2, random_state=42)

    # Créer le modèle Lasso
    if reg:
        model = Ridge()
    else:
        model = LogisticRegression()

    # Entraîner le modèle
    model.fit(X_train, y_train)

    feature_weights = pd.Series(model.coef_.flatten(), index=list_X)
    sorted_feature_weights = feature_weights.sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(15, len(list_X) // 3))
    sorted_feature_weights.plot.barh(ax=ax, color="orange", edgecolor="black")
    ax.set_title("Feature Weights")
    ax.set_xlabel("Weight")
    fig.tight_layout()
    plt.show()