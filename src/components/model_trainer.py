import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training (self, train_array, test_array):

        try:
            logging.info("Start of model trainer, splitting training and testing data")

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array [:, :-1],
                test_array [:, -1],
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            ## create a var of type dic and assign it values from the method
            model_report:dict=evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                              models=models, param=[])

            ## get the index of best model score        
            best_model_score = max (sorted (model_report.values()))

            if best_model_score < 0.6:
                raise CustomException ("All models have score < 0.6. No best model selected.")

            ## get best model (breakdown as follows)
            ## model_report.keys() > list, list(model_report.values() > nested list, .index(best_model_score) > best 
            best_model_name = list (model_report.keys())[list(model_report.values()).index(best_model_score)]
            ## from the 'models' list, pick the best model
            best_model = models[best_model_name]

            ## save this to pkl file
            save_object (
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict (X_test)
            r2_square = r2_score (y_test, predicted)

            return r2_square


        except Exception as e:
            raise CustomException (e, sys)