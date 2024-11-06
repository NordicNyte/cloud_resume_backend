import boto3
import json
from moto import mock_aws
import pytest
from lambda_function import lambda_handler

# The @mock_aws decorator is used to mock AWS services, like DynamoDB, for testing purposes.
# It ensures that actual AWS resources are not accessed, allowing for safe and isolated testing.
@mock_aws
def test_lambda_handler():
    """
    Unit test for the Lambda function using a mock DynamoDB environment.

    This test simulates the Lambda function's interaction with AWS DynamoDB by:
    
    1. Mocking a DynamoDB table named 'visitor_count'.
    2. Adding an initial item to simulate the visitor count starting at 0 for the path 'index.html'.
    3. Invoking the Lambda function (using a mock event and context) to simulate incrementing the visitor count.
    4. Retrieving the updated visitor count from the mock DynamoDB table.
    
    Assertions:
    - The Lambda function returns a status code of 200.
    - The visitor count is incremented to 1 in the mock DynamoDB table.
    - The Lambda function response body contains the updated visitor count.

    This test is safe to run as it uses the @mock_aws decorator, which mocks AWS services for isolated and controlled testing.
    
    To run this test, use pytest:
    - pytest -vs
    - pytest -vs test_lambda_unit.py
    """

    # Set up the mock DynamoDB environment
    # Create a DynamoDB client
    client = boto3.resource('dynamodb', region_name='us-east-1')
    
    # Create the mock table to simulate DynamoDB
    table = client.create_table(
        TableName='visitor_count',
        KeySchema=[{'AttributeName': 'path', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'path', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(TableName='visitor_count')
    
    # Add initial item to simulate existing data in DynamoDB
    table.update_item(
        Key={
            'path': 'index.html'  # Specifies the primary key (path) for the item to update
        },
        AttributeUpdates={
            'visitor_count': {
                'Value': 0,        # Increment visitor_count by 1
                'Action': 'ADD'    # 'ADD' will increase the current value of visitor_count
            }
        }
    )

    # Call the Lambda handler function
    event = {}  # Mock event (you can expand this for specific API Gateway simulation)
    context = {}  # Mock context (optional)
    response = lambda_handler(event, context)

    # Retrieve the updated visitor count from the mock DynamoDB table
    result = table.get_item(Key={'path': 'index.html'})
    updated_count = result['Item']['visitor_count']

    # Assertions
    assert response['statusCode'] == 200, "Expected status code to be 200"
    assert updated_count == 1, f"Expected visitor count to be 1, but got {updated_count}"
    response_body = json.loads(response['body'])
    assert response_body['visitor_count'] == updated_count, f"Expected visitor count in response body to be {updated_count}, but got {response_body['visitor_count']}"