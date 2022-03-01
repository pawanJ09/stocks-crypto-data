from botocore.exceptions import ClientError
from pprint import pprint
import boto3
import random


client = boto3.client('dynamodb')
resource = boto3.resource('dynamodb')
table = resource.Table('stocks-code-dd')


class StocksCodeModel:

    table_name = 'stocks-code-dd'

    def __init__(self, stock_id, name, code):
        self.stock_id = stock_id
        self.name = name
        self.code = code

    def json(self):
        return {"id": self.stock_id, "name": self.name, "code": self.code}

    def __repr__(self):
        return f"StocksCodeModel(id={self.stock_id!r}, name={self.name!r}, code={self.code!r})"

    @classmethod
    def find_by_name(cls, name):
        try:
            stocks_code = table.get_item(
                Key={
                    'stock_name': name
                },
                AttributesToGet=[
                    'id', 'stock_name', 'stock_code'
                ]
            )
            return stocks_code
        except ClientError as e:
            print(e.response['Error']['Message'])

    def save_to_db(self):
        try:
            response = table.put_item(
                Item={
                    'id': self.stock_id,
                    'stock_name': self.name,
                    'stock_code': self.code
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])

    @classmethod
    def update_in_db(cls, name, code):
        try:
            response = table.update_item(
                Key={
                    'stock_name': name
                },
                UpdateExpression="set stock_code = :sc",
                ExpressionAttributeValues={
                    ':sc': code
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            print(e.response['Error']['Message'])

    @classmethod
    def delete_from_db(cls, name):
        try:
            response = table.delete_item(
                Key={
                    'stock_name': name
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])

    @classmethod
    def fetch_all(cls):
        # This can be expensive if huge dynamo db table data exists
        try:
            response = table.scan()
            return response
        except ClientError as e:
            print(e.response['Error']['Message'])
