import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from file_manager import FileManager


def main_pipeline():

    # load data
    # iris = load_iris()
    # X = pd.DataFrame(iris.data)
    # y = pd.DataFrame(iris.target)

    WDI = pd.read_csv('data/WorldDevInd.csv')

    fm = FileManager(output_path='output_data')
    for year, wdi in WDI.groupby('Time'):
        X = wdi.drop('GDP (current US$) [NY.GDP.MKTP.CD]', axis=1).iloc[:, 2:]
        y = wdi[['GDP (current US$) [NY.GDP.MKTP.CD]']]

        # split data (for training and testing)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        # train model
        model = XGBClassifier(random_state=42)
        model.fit(X_train.values, y_train.values)

        # get model preds
        preds = pd.DataFrame(model.predict(X_test), columns=['target_pred'])

        # format
        # X_train.columns = ["feature_1", "feature_2", "feature_3", "feature_4"]
        # X_test.columns = ["feature_1", "feature_2", "feature_3", "feature_4"]

        y_train.rename(columns={0: 'target_train'})
        y_train.columns = y_train.columns.astype(str)
        y_test.rename(columns={0: 'target_test'})
        y_test.columns = y_test.columns.astype(str)

        # write

        output_path = fm.get_modified_output_path()

        X_train.to_parquet(f'{output_path}/X_train_{year}.parquet')
        X_test.to_parquet(f'{output_path}/X_test_{year}.parquet')
        y_train.to_parquet(f'{output_path}/y_train_{year}.parquet')
        y_test.to_parquet(f'{output_path}/y_test_{year}.parquet')
        preds.to_parquet(f'{output_path}/pred_{year}.parquet')
        if year == 2002:
            break


main_pipeline()
