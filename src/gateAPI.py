import re
import gate_api
from gate_api.exceptions import ApiException, GateApiException

# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4"
)

api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
api_instance = gate_api.SpotApi(api_client)

def get_gateio_listed_coins():
    try:
        # List all currencies' details
        api_response = api_instance.list_currencies()
        coins = []
        for curr in api_response:
            if '_' not in curr.currency and '3' not in curr.currency and '5' not in curr.currency:
                coin = re.sub("[^A-Za-z]","", curr.currency)
                coins.append(coin)
        return coins
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling SpotApi->list_currencies: %s\n" % e)