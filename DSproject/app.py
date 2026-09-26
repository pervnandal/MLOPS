import os
import warnings
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
import mlflow
from mlflow.models.signature import infer_signature
import mlflow.sklearn
import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actaul, pred):
    rmse = np.sqrt(mean_squared_error(actaul, pred))
    mae = mean_absolute_error(actaul, pred)
    r2 = r2_score(actaul, pred)
    return rmse, mae, r2


if __name__ == "__main__":

    # Data ingestion - reading the dataset(wine quality)
    csv_url = "https://raw.githubusercontent.com/mlflow/mlflow/master/tests/datasets/winequality-red.csv"

    try:
        data = pd.read_csv(csv_url, sep=";")
    except Exception as e:
        logger.exception("Unable to download the data")

    # train_test_split
    train, test = train_test_split(data)  # default test = 0.25

    train_x = train.drop(columns=["quality"], axis=1)
    test_x = test.drop(columns=["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    # argv is for arguments given from terminal
    # argv[1]-> first argument of terminal
    # argv[2]-> second argument of terminal

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    with mlflow.start_run():
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)

        predicted_qualites = lr.predict(test_x)
        rmse, mae, r2 = eval_metrics(test_y, predicted_qualites)

        print("Elasticnet model (alpha={:f}, l1_ratio={:f}):".format(alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("Alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2_score", r2)

        # For the remote server(AWS) - we need to do the setup
        remote_server_uri = ""
        mlflow.set_tracking_uri(remote_server_uri)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(
                sk_model=lr, 
                name="model", 
                registered_model_name="ElasticnetWineModel"
            )
        else:
            mlflow.sklearn.log_model(sk_model=lr, name="model")
