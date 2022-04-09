import numpy as np
import pandas as pd
import json
from xgboost import XGBClassifier


def drift(models=None, validation_set=None) -> pd.DataFrame:
    """
    Ingest validation dataset
    Ingest models
    For each model, get model's prediction on validation set
    concat model predictions, and write to AWS or Local
    """


    validation_data = pd.read_parquet('../ML Pipeline/META FINAL DATA/validation_gan_1.parquet')
    output_dirs = ['1', '2', '3', '4', '5']
    output_paths = 'ML Pipeline/output_data'

    models = []
    accuracies = []

    for subdir in output_dirs:
        path = f'{output_paths}/{subdir}/'
        model = XGBClassifier(random_state=42)
        model.load_model(f'{path}/model.json')
        accuracy_dict = json.load(f'{path}/accuracy.json')
        models.append(model)
        accuracies.append(accuracy_dict)

    df = pd.DataFrame({'Model':[], 'Accuracy':[]})


drift()




