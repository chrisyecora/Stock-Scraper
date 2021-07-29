# Purpose

    This program is a python script that uses the RESTful API provided by
polygon.io to get the close price of the top 20 largest market cap stocks. 
    
    The script uses an HTTP request in order to get the JSON object. The JSON object is then
    pasred and placed into a pandas DataFrame object. Once this is done, the data is exported into
    a csv file that can be used for further analysis.

# Data Collected

Daily closing price for 2 years
Daily trading volume
Date

# Side Notes

    This script was made using a free API, which only permits 5 API calls per minute. For this
reason, the API calls in the program are delayed by 12 seconds in order to not overflow the 
API calls.

    Only 2 years of historical data is included in the free version of polygon.io, which is why
only 2 years of data was collected for each stock