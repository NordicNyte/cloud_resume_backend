import json
import boto3
from decimal import Decimal

def convert_decimal_to_int_or_float(value):
    """
    Recursively convert Decimal objects to int or float
    to make them JSON serializable.
    """
    if isinstance(value, list):
        return [convert_decimal_to_int_or_float(v) for v in value]
    elif isinstance(value, dict):
        return {k: convert_decimal_to_int_or_float(v) for k, v in value.items()}
    elif isinstance(value, Decimal):
        # Convert Decimal to int if it's a whole number, else to float
        return int(value) if value % 1 == 0 else float(value)
    else:
        return value

def lambda_handler(event, context):
    print("Lambda function started.")
    
    # Log incoming event data
    print("Event data received:", json.dumps(event))
    
    # Connect to DynamoDB resource
    print("Connecting to DynamoDB...")
    client = boto3.resource('dynamodb')
    print("DynamoDB connection established.")

    # Create DynamoDB table object
    print("Fetching DynamoDB table 'visitor_count'...")
    table = client.Table('visitor_count')
    print("DynamoDB table fetched successfully.")

    # Increment visitor_count on DynamoDB and return the updated value
    print("Updating visitor count...")
    update_response = table.update_item(
        Key={'path': 'index.html'},
        UpdateExpression="ADD visitor_count :inc",
        ExpressionAttributeValues={':inc': 1},
        ReturnValues="UPDATED_NEW"
    )
    print("Visitor count updated successfully. Update response:", update_response)

    # Extract the updated visitor count from the update response and convert it to int
    visitor_count = int(update_response['Attributes']['visitor_count'])
    print(f"Extracted updated visitor count: {visitor_count}")

    # Prepare response
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'visitor_count': visitor_count})
    }
    print("Response prepared:", response)

    print("Lambda function execution completed.")
    return response
