

from fastapi import FastAPI,HTTPException,status,Depends
from azure.storage.blob import ContainerClient
from responses import Response
app = FastAPI()

@app.get("/v1/blob_list")
def List_of_Object():
    try:
        container = ContainerClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=scalaracount;AccountKey=vXdFtfFWdYiypod9vB8I3LfrkrjAFrgZGvgrR2Xt/18Jq9Oi9F0CNKSLLeJ1jpu5+Ek41q3dOZYv+AStsqsACw==;BlobEndpoint=https://scalaracount.blob.core.windows.net/;FileEndpoint=https://scalaracount.file.core.windows.net/;QueueEndpoint=https://scalaracount.queue.core.windows.net/;TableEndpoint=https://scalaracount.table.core.windows.net/", container_name="container1")
        blob_list = container.list_blobs()
        all_blob=[]
        for blob in blob_list:
            all_blob.append(blob.name)
        return(all_blob)
    except Exception as e:
        return Response(e, 'The container does contain ant blob', True)