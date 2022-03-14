import sys
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def compile_response(msg, statusCode=200):
    data_key = 'data' if statusCode == 200 else 'error'
    response = {
        'headers': {
            'Content-Type':'application/json'
        },
        'body': {
            data_key: msg
        },
        'statusCode': str(statusCode)
    }
    return response

def error_500():
    return compile_response('Something went wrong on the server', 500)

def main(dict):
    method = dict['__ow_method']
    
    authenticator = IAMAuthenticator(dict['IAM_API_KEY'])
    service = CloudantV1(authenticator=authenticator)
    
    service.set_service_url(dict['COUCH_URL'])
    
    if method == 'post':
        if 'review' in dict:
            review = Document(**dict['review'])
            response = service.post_document(
                db='reviews',
                document=review
            ).get_result()
        else:
            return compile_response("Bad request. No data provided.", 400)
    else:
        try:
            response = service.post_find(
                db='reviews',
                selector = {
                    'dealership': {
                        '$eq': int(dict['dealerId'])
                    }
                },
                fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
            ).get_result()
        except:
            return error_500()
        if response['bookmark'] == 'nil':
            return compile_response('dealerId does not exist', 404) 
    
    return compile_response(response)
