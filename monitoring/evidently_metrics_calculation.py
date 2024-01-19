import datetime
import time
import random
import logging 
import pandas as pd
import psycopg
import joblib

from prefect import task, flow

from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10
rand = random.Random()

def convert_to_category(df,cat_features):
    for c in cat_features:
        df[c] = df[c].astype('category')	

    return df
	
def generate_report_mapping():
    raw_data = pd.read_csv('../data/YouTubeDataset_withChannelElapsed.csv')
    features =['index','channelId','videoCategoryId', 'channelViewCount',
                        'videoCount', 'subscriberCount', 'videoId','channelelapsedtime',
                        'channelCommentCount', 'videoViewCount','elapsedtime', 
                        'videoDislikeCount','videoPublished', 'VideoCommentCount','videoLikeCount']
    cat_features = ['channelId', 'videoId','videoPublished']
        
    raw_data = raw_data[features]
    trained_data = raw_data

    # i will filter the training set for a week as well cause if I compare the whole training set
    # to one week of new data then the report takes a really long time to run
    trained_data = trained_data[(trained_data['videoPublished']>='2015-09-21T17:54:24.000Z') & (trained_data['videoPublished']<='2015-09-28T17:54:24.000Z')]

    trained_data = convert_to_category(trained_data,cat_features)

    with open('lightgbm_reg.bin', 'rb') as f_in:
        model = joblib.load(f_in)

    #since I have no new data, I will just assume that the last week of the training data is new data

    raw_data['videoPublished'] = raw_data['videoPublished'].astype(object)
    new_data = raw_data[(raw_data['videoPublished']>='2015-09-29T17:54:24.000Z') & (raw_data['videoPublished']<='2015-10-05T17:54:24.000Z')]
    new_data.drop(['videoLikeCount'],axis=1,inplace=True)

    new_data = convert_to_category(new_data,cat_features)
	
    new_data['videoLikeCount'] = model.predict(new_data)
	
    num_features = list(set(features)-set(cat_features))
    column_mapping = ColumnMapping(
        prediction='videoLikeCount',
        numerical_features=num_features,
        categorical_features=cat_features,
        target=None
    )
	
    report = Report(metrics = [
        ColumnDriftMetric(column_name='videoLikeCount'),
        DatasetDriftMetric(),
        DatasetMissingValuesMetric()
    ])

	
    return model,new_data,trained_data,report,column_mapping,features

@task
def prep_db():
	create_table_statement = """
    drop table if exists evidently_metrics;
    create table evidently_metrics(
        prediction_drift float,
        num_drifted_columns integer,
        share_missing_values float
    )
    """

	with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='metrics'")
		if len(res.fetchall()) == 0:
			conn.execute("create database metrics;")
		with psycopg.connect("host=localhost port=5432 dbname=metrics user=postgres password=example") as conn:
			conn.execute(create_table_statement)

@task
def calculate_metrics_postgresql(curr,model,new_data,trained_data,report,column_mapping,features):

	report.run(reference_data = trained_data, current_data = new_data,
		column_mapping=column_mapping)

	result = report.as_dict()
	print(result)

	prediction_drift = result['metrics'][0]['result']['drift_score']
	num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
	share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']

	curr.execute(
		"insert into evidently_metrics(prediction_drift, num_drifted_columns, share_missing_values) values (%s, %s, %s)",
		(prediction_drift, num_drifted_columns, share_missing_values)
	)
	time.sleep(5)

@flow
def batch_monitoring_backfill():
	model,new_data,trained_data,report,column_mapping,features = generate_report_mapping()
	prep_db()
	with psycopg.connect("host=localhost port=5432 dbname=metrics user=postgres password=example", autocommit=True) as conn:
		with conn.cursor() as curr:
			calculate_metrics_postgresql(curr,model,new_data,trained_data,report,column_mapping,features)
		logging.info("data sent")

if __name__ == '__main__':
	batch_monitoring_backfill()