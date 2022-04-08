import numpy as np
import pandas as pd


def drift(models, validation_set) -> pd.DataFrame:
    # Ingest validation dataset
    # Ingest models
    # For each model, get model's prediction on validation set
    # concat model predictions, and write to AWS or Local

    validation_data = pd.read_parquet('ML Pipeline/META FINAL DATA/validation_gan_1.parquet')
    for model in



