from io import StringIO
import boto3

def df_to_s3_as_csv(df, bucket, filename):
	csv_buffer = StringIO()
	df.to_csv(csv_buffer)
	s3_resource = boto3.resource('s3')
	s3_resource.Object(bucket, filename).put(Body=csv_buffer.getvalue())