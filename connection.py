def aws_connection():
    import boto3
    s3 = boto3.client('s3',aws_access_key_id="AKIA3YCVAX2EE3QOZL6V",aws_secret_access_key="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")
    return s3

def azure_connecting_string():
    connection_string="DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=san002;AccountKey=sEoPtESCvyJAaLBPY3JcGHR/3L3mqWrzFYXK6K3s2+UQ0jR3VhINOmTMmw7iyt4IDm4JTxAm6tGl+AStdb3krA==;BlobEndpoint=https://san002.blob.core.windows.net/;FileEndpoint=https://san002.file.core.windows.net/;QueueEndpoint=https://san002.queue.core.windows.net/;TableEndpoint=https://san002.table.core.windows.net/"
    return connection_string