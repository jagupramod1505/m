def bucket_permission_match(eplist,bucket_permission,match_list):
    try:
        flag=0
        for item in eplist:
            for index in bucket_permission:
                if item == index:
                    match_list.append(index)
                    flag=flag+1
        return flag
    except Exception as e:
        return Response(e, 'Opration Failed', True)




def Response(json_data, message, error):
    return {
        "data": json_data,
        "message": message,
        "error": error
    }

