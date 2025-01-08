import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.dynamodb = None
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION")
        self.dynamodb_endpoint = os.getenv("DYNAMODB_ENDPOINT")

    def connect(self):
        try:
            self.dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url=self.dynamodb_endpoint,
                region_name=self.aws_region,
                aws_access_key_id= self.aws_access_key,
                aws_secret_access_key= self.aws_secret_key
            )
            print("Connected to DynamoDB Local successfully!")
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Failed to connect to DynamoDB: {str(e)}")
        return self.dynamodb

    def get_table(self, table_name):
        if not self.dynamodb:
            raise Exception("Database connection is not established. Call 'connect()' first.")
        return self.dynamodb.Table(table_name)