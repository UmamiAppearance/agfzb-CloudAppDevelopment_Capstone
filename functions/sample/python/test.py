import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(dict):
    method = dict["__ow_method"]
    
    if method == "post":
        return { "message": "hello poster" }
    
    authenticator = IAMAuthenticator(dict['IAM_API_KEY'])
    service = CloudantV1(authenticator=authenticator)
    
    service.set_service_url(dict['COUCH_URL'])
    response = service.post_find(
        db='reviews',
        selector = {
            'dealership': {
                '$eq': int(dict["dealerId"])
            }
        },
        fields = ["id", "name", "dealership", "review", "purchase", "purchase_date", "car_make", "car_model", "car_year"]
    ).get_result()
    
    try:
        # result_by_filter=my_database.get_query_result(selector,raw_result=True)
        result= {
            'headers': {'Content-Type':'application/json'},
            'body': {'data':response}
        }
    except:
        result = {}
    
    return result
