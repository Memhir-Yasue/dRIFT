import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from file_manager import FileManager

def main_pipeline():

    # load data
    iris = load_iris()
    X = pd.DataFrame(iris.data)
    y = pd.DataFrame(iris.target)

    # split data (for training and testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    # train model
    model = XGBClassifier(random_state=42)
    model.fit(X_train, y_train)

    # get model preds
    preds = pd.DataFrame(model.predict(X_test), columns=['target_pred'])

    # format
    X_train.columns = ["feature_1", "feature_2", "feature_3", "feature_4"]
    X_test.columns = ["feature_1", "feature_2", "feature_3", "feature_4"]

    y_train.rename(columns={0: 'target_train'})
    y_train.columns = y_train.columns.astype(str)
    y_test.rename(columns={0: 'target_test'})
    y_test.columns = y_test.columns.astype(str)

    # write
    fm = FileManager(output_path='output_data')
    output_path = fm.get_modified_output_path()

    X_train.to_parquet(f'{output_path}/X_train.parquet')
    X_test.to_parquet(f'{output_path}/X_test.parquet')
    y_train.to_parquet(f'{output_path}/y_train.parquet')
    y_test.to_parquet(f'{output_path}/y_test.parquet')
    preds.to_parquet(f'{output_path}/pred.parquet')


main_pipeline()
