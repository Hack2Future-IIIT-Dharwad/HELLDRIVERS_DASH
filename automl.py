import h2o,mlflow,pandas,argparse,json
from h2o.automl import H2OAutoML, get_leaderboard
from mlflow.tracking import MlflowClient
import mlflow.h2o
from mlflow.entities import ViewType
import web 
import sys



def main2(X,y):
    #initialzing h2o and mlflow
    h2o.init()
    global client
    client = MlflowClient()
    

    experiment_name = 'automl-platform'

    try:
        experiment_id = mlflow.create_experiment(experiment_name)
        experiment = client.get_experiment_by_name(experiment_name)
    except:
        experiment = client.get_experiment_by_name(experiment_name)

    # set experiment
    mlflow.set_experiment(experiment_name)


    # print experiment info

    print(f"Name: {experiment_name}")
    print(f"Experiment_id: {experiment.experiment_id}")
    print(f"Artifact Location: {experiment.artifact_location}")
    print(f"Lifecycle_stage: {experiment.lifecycle_stage}")
    print(f"Tracking uri: {mlflow.get_tracking_uri()}")

    
    main_frame = h2o.import_file('hack.csv')    

    target = X
    y = main_frame.columns
    predictors = [n for n in main_frame.columns if n not in X]
    main_frame[target] = main_frame[target].asfactor()
    # ...

    print("Starting AutoML")
    # Wrap autoML training with MLflow
    with mlflow.start_run():
        aml = H2OAutoML(
                        seed=1,  
                        sort_metric='logloss', # Sort models by logloss (metric for multi-classification)
                        verbosity='info', # Turn on verbose info
                        max_runtime_secs = 600,
                        exclude_algos = ['GLM', 'DRF','DeepLearning'],
                    )
    
    print("AutoML training started")
    # Initiate AutoML training
    aml.train(predictors,target, training_frame=main_frame)
    print("AutoML training completed")
    # Set metrics to log
    if aml.leader is not None:
        mlflow.log_metric("log_loss", aml.leader.logloss())
        mlflow.log_metric("AUC", aml.leader.auc())
    else:
        print("No leader model found. Cannot log metrics.")

    # Log and save best model (mlflow.h2o provides API for logging & loading H2O models)
    mlflow.h2o.log_model(aml.leader, artifact_path="model")

    model_uri = mlflow.get_artifact_uri("model")
    print(f'AutoML best model saved in {model_uri}')

    # Get IDs of current experiment run
    exp_id = experiment.experiment_id
    run_id = mlflow.active_run().info.run_id

    # Save leaderboard as CSV
    lb = get_leaderboard(aml, extra_columns='ALL')
    lb_path = f'mlruns/{exp_id}/{run_id}/artifacts/model/leaderboard.csv'
    lb.as_data_frame().to_csv(lb_path, index=False) 

def predict(link):
     # Get best model amongst all runs in all experiments
    all_exps = [exp.experiment_id for exp in client.search_experiments()]
    runs = mlflow.search_runs(experiment_ids=all_exps, run_view_type=ViewType.ALL)
    run_id, exp_id = runs.loc[runs['metrics.log_loss'].idxmin()]['run_id'], runs.loc[runs['metrics.log_loss'].idxmin()]['experiment_id']

    # Load best model (AutoML leader)
    best_model = mlflow.h2o.load_model(f"mlruns/{exp_id}/{run_id}/artifacts/model/")
    file = h2o.import_file(link)
    # Generate predictions with best model (output is H2O frame)
    preds_frame = best_model.predict(file)
    # Convert to pandas series
    y_pred = preds_frame.as_data_frame()['predict']
    return y_pred
def predict2(link):
    h2o.init()
    # Load best model (AutoML leader)
    best_model = mlflow.h2o.load_model(f"mlruns/855536383886581350/5d0c09d6568d409a920e102a7423d51d/artifacts/model")
    file = h2o.import_file(link)
    # Generate predictions with best model (output is H2O frame)
    preds_frame = best_model.predict(file)
    # Convert to pandas series
    y_pred = preds_frame.as_data_frame()['predict']
    print(y_pred)
    return y_pred

