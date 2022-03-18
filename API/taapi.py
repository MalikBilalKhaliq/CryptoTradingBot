import requests 


class TaapiIndicator:
    #Result Will be place in that global variable
    result= {}
    # Define endpoint 
    endpoint = "https://api.taapi.io/bulk"
    def __init__(self,exchangeName,sybmolData,interval,indicator):
        # Define a JSON body with parameters to be sent to the API 
        #print("Printing Class Indicator")
        #print(indicator)
        self.parameters = {
            "secret": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJpbGFsb25lN0BnbWFpbC5jb20iLCJpYXQiOjE2NDUwMDEzMTQsImV4cCI6Nzk1MjIwMTMxNH0.6zy2zZ9Bgl2KJVK-BVoHtVgxnUipOAmk4tgZl7npq2M",
            "construct": {
                "exchange": exchangeName,
                "symbol": sybmolData,
                "interval": interval
            }     
        }
        self.parameters["construct"]["indicators"]=indicator
        #print("Printing Self parameter")
        #print(self.parameters)

    def SetIndicatorsValue(self):
        #Below url is for making connection activate
        url = "http://www.kite.com"
        #Also set the timeout for 5
        timeout = 5
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
        # Send POST request and save the response as response object 
        response = requests.post(url = self.endpoint, json = self.parameters)
        # Extract data in json format 
        self.result = response.json() 


