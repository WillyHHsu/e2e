import boto3


def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8005", region_name='us-west-2')

    table = dynamodb.create_table(
        TableName='logs',
        KeySchema=[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH'
            }
            ,{
                'AttributeName': 'value',
                'KeyType': 'RANGE'
            }
        ],

        AttributeDefinitions=[
            {
                'AttributeName': 'user_id',
                'AttributeType': 'N'
            }
            ,{
                'AttributeName': 'value',
                'AttributeType': 'S'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


    table_param = dynamodb.create_table(
        TableName='params',
        KeySchema=[
            {
                'AttributeName': 'model',
                'KeyType': 'HASH'
            }
            ,{
                'AttributeName': 'dtime',
                'KeyType': 'RANGE'
            }
        ],

        AttributeDefinitions=[
            {
                'AttributeName': 'model',
                'AttributeType': 'S'
            }
            ,{
                'AttributeName': 'dtime',
                'AttributeType': 'S'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return 'done'


if __name__ == '__main__':
    logs_tables = create_table()
    print('done')