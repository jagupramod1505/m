from fastapi import FastAPI,HTTPException,status,Depends,APIRouter
# import uvicorn
from lib import bucket_permission_match
from lib import Response
from connection import aws_connection,azure_connecting_string
from azure.storage.fileshare import ShareServiceClient
from azure.storage.blob import BlobServiceClient
# from pydantic import BaseModel
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union
# import boto3

# global connection_string
# connection_string="DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=san002;AccountKey=sEoPtESCvyJAaLBPY3JcGHR/3L3mqWrzFYXK6K3s2+UQ0jR3VhINOmTMmw7iyt4IDm4JTxAm6tGl+AStdb3krA==;BlobEndpoint=https://san002.blob.core.windows.net/;FileEndpoint=https://san002.file.core.windows.net/;QueueEndpoint=https://san002.queue.core.windows.net/;TableEndpoint=https://san002.table.core.windows.net/"

router = APIRouter(

    prefix="/Aws-Azure",

    tags=["/Aws-Azure"],

    responses={404: {"description": "Not found"}}

)
#==========================function for list of buckets==================================================================

@router.get("/v1/bucket_list")
def list_buckets(cloud_key :str):
    if cloud_key =="aws":
        try:
            s3=aws_connection()
            bucket=s3.list_buckets()
            bucket_list=[]
            for item in bucket ["Buckets"]:
                bucket_list.append(item["Name"])
            data=bucket_list
            
            return Response(data, 'Bucket retrieved successfully', False)
        except Exception as e:
            return Response(e, 'The specified bucket does not exist', True)
    if cloud_key =="azure":
        try:
            connection_string=azure_connecting_string()
            blob_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
            containers = blob_client.list_containers()
            container_names = []
            for container in containers:
                container_names.append(container.name)
            data1=(container_names)

            service_client = ShareServiceClient.from_connection_string(conn_str=connection_string)
            data2=[]
            my_list = list(service_client.list_shares())
            for item in (my_list):
                data2.append(item["name"])

            return Response(f'container = {data1} and file share = {data2}', 'file share and container retrieved successfully', False)
        except Exception as e:
            return Response(e, 'Opration Failed', True)
    else:
        return Response("Invalid input", 'Opration Failed', True)

#==========================function for list of Object==================================================================
@router.get("/v1/object_List")

def List_of_Object(Bucketname: str):
    try:
        s3=aws_connection()
        object = s3.list_objects(Bucket=Bucketname)
        objectname = []
        for item in object['Contents']:
            objectname.append(item['Key'])
        data = (objectname)
        if data is not None:
            return Response(data, 'Object retrieved successfully', False)
    except Exception as e:
        return Response(e, 'The specified does not exist', True)
#==========================function for list permission of bucket=======================================================

@router.get("/v1/bucket_permission")
def list_bucket_permission(cloud_key :str,bucketname : str):
    if cloud_key =="aws":
        try:
            s3=aws_connection()
            bucket = s3.get_bucket_acl(Bucket=bucketname)
            
            bucket_permission=[]
            for item in bucket ["Grants"]:
                existing_permission=(item["Permission"])
                bucket_permission.append(existing_permission)
            bucket_permission=set(bucket_permission)
            data=list(bucket_permission)
            return Response(data, 'Permission retrieved successfully', False)
        except Exception as e:
            return Response(e, 'The specified bucket does not exist', True)

    if cloud_key =="azure":
        connection_string=azure_connecting_string()
        service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = service_client.get_container_client(bucketname)
        access_policy = container_client.get_container_access_policy()
        permission_list=[]
        for identifier in access_policy['signed_identifiers']:
            permission_list.append(identifier.access_policy.permission)
        identifireid_list=[]
        for identifier in access_policy['signed_identifiers']:
            identifireid_list.append(identifier.id)
        data = dict(zip(identifireid_list, permission_list))
        return Response(data, 'container permission retrieved successfully', False)
    

@router.get("/v1/container_permission")
def container_permission(container_name:str):
    try:
        #storagecontainerone
        #container2
        #container = ContainerClient.from_connection_string(conn_str=connection_string,container_name=container_name)
        #container_access_policy = container.get_container_access_policy()
        connection_string=azure_connecting_string()
        service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = service_client.get_container_client(container_name)
        access_policy = container_client.get_container_access_policy()
        permission_list=[]
        for identifier in access_policy['signed_identifiers']:
            permission_list.append(identifier.access_policy.permission)
        identifireid_list=[]
        for identifier in access_policy['signed_identifiers']:
            identifireid_list.append(identifier.id)
        data = dict(zip(identifireid_list, permission_list))
        return Response(data, 'container permission retrieved successfully', False)
    except Exception as e:
        return Response(e, 'Opration Failed', True)
        
    
     
#======================function for comparing permissions of bucket====================================================

@router.get("/v1/compare_bucket_permission")
def compare_bucket_permission(bucketname : str, bucket_permission : str,input_choise:int =0):
    try:
        s3=aws_connection()
        bucket = s3.get_bucket_acl(Bucket=bucketname)
        
        bucketpermission=[]
        for item in bucket ["Grants"]:
            existing_permission=(item["Permission"])
            bucketpermission.append(existing_permission)
        bucketpermission=set(bucketpermission)
        eplist=list(bucketpermission)

        bucket_permission = bucket_permission.split(",")
        iplen=(len(bucket_permission))
    
        match_list=[]
        
        if input_choise:
            eplist = [x.upper() for x in eplist]
            bucket_permission= [x.upper() for x in bucket_permission]
            flag=bucket_permission_match(eplist,bucket_permission,match_list)
        else:
            flag=bucket_permission_match(eplist,bucket_permission,match_list)

        unmatch_list = []
        for element in bucket_permission:
            if element not in match_list:
                unmatch_list.append(element)

        if flag ==iplen:
            return Response("all Permission match successfully",'Permission matched', False)
        if flag ==0:
            return Response(f'Permission match:{match_list} ,Permission not match:{unmatch_list}',"Permission not matched" , True)
        return Response(f'Permission match:{match_list} ,Permission not match:{unmatch_list}', "Permission matched partially", True)
    except Exception as e:
        return Response(e, 'Opration Failed', True)
