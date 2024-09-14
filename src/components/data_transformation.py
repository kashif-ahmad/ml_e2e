import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    ## will help to store model in pkl file
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")


class DataTransformation:
    
    def __init__(self):
        ## create a variable and init with class above
        self.data_transformation_config = DataTransformationConfig()

    ## this function will transform the data 
    def get_data_transformer_object(self):

        try:

            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course",
            ]
        
            ## define a numerical pipeline here
            numerical_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scalar", StandardScaler())
                ]
            )

            ## define a categorical pipeline here
            categorical_pipeline = Pipeline(
                steps=(
                    ("Imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scalar", StandardScaler(with_mean=False))
                )
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            ## create a transformer object with two pipelines defined above
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", numerical_pipeline, numerical_columns),
                    ("cat_pipeline", categorical_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            return CustomException(e, sys)


    def initiate_data_transformation(self, train_path, test_path):

        try:
            ## read the train and test data
            train_data = pd.read_csv(train_path)
            test_data  = pd.read_csv(test_path)

            logging.info(f"Test and train data completed")
            logging.info(f"Obtaining preprocessing object")

            ## get an instance of pipeline object which has both numerical and categorical data
            preprocessing_obj = self.get_data_transformer_object()

            ## identify the target column
            target_column = "math_score"
            ## identify the numerical columns
            numerical_columns = ["writing_score", "reading_score"]

            ## set the train dataframe with/without target columns
            input_feature_train_df = train_data.drop(columns=[target_column], axis=1)
            target_feature_train_df = train_data[target_column]
                                                 
            ## set the test dataframe with/without target columns
            input_feature_test_df = test_data.drop(columns=[target_column], axis=1)
            target_feature_test_df = test_data[target_column]

            logging.info(f"Created preprocessing objects on training/test dataframes")

            ## here we fit the data using transformer object
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.fit_transform(input_feature_test_df)

            ## the np.c_ function 'translates slice objects to concatenation along the second axis.'
            ## arrays will be stacked along their last axis after being upgraded to at least 2-D 
            ## with 1’s post-pended to the shape
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            ## here we want to save our model to a pkl file
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path)
        
        except Exception as e:
            raise CustomException(e,sys)

        except:
            pass
    

