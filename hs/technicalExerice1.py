import requests, json, os

# Config
submission_number = 1
csv_filename = "result.csv"

# Auth 
base_url = "https://sales1.demo.hyperscience.com/api/v5/"
auth_token = "171d33b7d6dc63060e721bff2a41288d6ca28327"
headers = {'Authorization': 'Token ' + auth_token}
params = {'flat': False}

# Functions
def getEndpointURL(endpoint,param):
    endpoint_url = base_url + endpoint + param
    return endpoint_url
    
# Main
print('Starting techExercice1.py script')
endpoint_url = getEndpointURL("submissions","/%s?flat=false" % (submission_number))
print("Checking submission #%s with URL %s" % (submission_number,endpoint_url))
read_submission=requests.get(endpoint_url, headers=headers).json()
check_get_value = read_submission.get("id")
if check_get_value:
    print("Checking extracted field")
    documents = read_submission["documents"]
    print("Number of documents: %s" % len(documents))
    root = os.path.dirname(os.path.realpath(__file__))
    file_result = open(root+"/"+csv_filename,"w+")
    total_number_of_field = 0
    number_extracted_field = 0
    j=0
    while j < len(documents):
        document_fields = read_submission["documents"][j]["document_fields"]
        k=0
        total_number_of_field = total_number_of_field + len(document_fields)
        while k < len(document_fields):
            field_name = read_submission["documents"][j]["document_fields"][k]["name"]
            field_value = read_submission["documents"][j]["document_fields"][k]["transcription"]["normalized"]
            if len(field_value) > 0:
                number_extracted_field += 1
            line = (field_name+","+field_value+"\n")
            file_result.write(line)
            k += 1
        j += 1
    file_result.close()    
else:
    print("Nothing to do, no results")
print("Total of field: %s" % total_number_of_field)
print("Total of extracted field:%s" % number_extracted_field)
performance = (number_extracted_field/total_number_of_field)*100
print("Performance: %s %%" % performance)
