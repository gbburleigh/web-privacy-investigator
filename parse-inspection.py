import json, pandas, os, sys
from numpy.core.numeric import NaN

"""
Main parsing function for inspection-log.ndjson
Crawls full report returned by blacklight-collector and aggregates results for analysis

Arguments:
site(str): website directory to pull data from
device(str): chosen device directory to pull site data from
"""
def parse_inspection(site, device):
    #Load our data
    filename="inspection-log.ndjson"
    dir_ = os.getcwd() + f"/data/{site}/{device}"
    dir_ = r'{}'.format(dir_)

    #Instantiate accumulators
    opData = []
    filterData = []
    cookieData = []
    
    #Open inspection-log.ndjson for given device/site
    with open(f'{dir_}/{filename}', 'r') as fp:
        done = []

        #.ndjson files have to be read and parsed into individual json objects line by line
        for line in fp.readlines():
            if line in done:
                pass
            j = json.loads(line)

            #Throw away blank entries
            if j['message'] == {}:
                continue

            #If no data available, ignore row
            try:
                data = j['message']['data']
            except:
                continue
            
            #If the data entry is a dictionary, it can be an operation log, or a filter log

            if type(data) == dict:
                
                #Logs an operation completed by the browser when accessing site
                if 'operation' in data.keys():
                    args = safe_fetch(data, 'arguments')
                    symbol = safe_fetch(data, 'symbol')
                    value = safe_fetch(data, 'value')
                    if value == {}:
                        value = None
                    operation = safe_fetch(data, 'operation')
                    opStack = safe_fetch(j['message'], 'stack')
                    if opStack is None:
                        continue;
                    for entry in opStack:
                        col = safe_fetch(entry, 'columnNumber')
                        lineNum = safe_fetch(entry, 'lineNumber')
                        func = safe_fetch(entry, 'funcName')
                        source = safe_fetch(entry, 'source')
                        obj = [operation, symbol, value, opStack, args, col, lineNum, func, source]
                        if obj != [None, None, None, None, None, None, None, None, None]:
                            opData.append(obj)

                #Logs matches to hard-coded domains and scripts from list 'listName'
                elif 'filter' in data.keys():
                    filter = safe_fetch(data, 'filter')
                    listName = safe_fetch(data, 'listName')
                    filterStack = safe_fetch(data, 'stack')
                    typ = safe_fetch(data, 'type')
                    url = safe_fetch(data, 'url')
                    obj = [filter, listName, filterStack, typ, url]
                    if obj != [None, None, None, None, None]:
                        filterData.append(obj)

            #If the data entry is a list, we're looking at cookie data
            elif type(data) == list:
                if data == []:
                    continue
                data = data[0]
                key = safe_fetch(data, 'key')
                cookieValue = safe_fetch(data, 'value')
                path = safe_fetch(data, 'path')
                httpOnly = safe_fetch(data, 'httpOnly')
                domain = safe_fetch(data, 'domain')
                maxAge = safe_fetch(data, 'maxAge')
                extensions = safe_fetch(data, 'extensions')
                secure = safe_fetch(data, 'secure')
                expires = safe_fetch(data, 'expires')
                obj = [key, cookieValue, domain, maxAge, extensions, path, secure, httpOnly, expires]
                if obj != [None, None, None, None, None, None, None, None, None]:
                    cookieData.append(obj)
            
            done.append(line)

    #Put our accumulators in DataFrames for ease of analysis and return

    opColumns = ['operation', 'symbol', 'value', 'stack', 'args', 'lineCol', 'lineNum', 'funcName', 'funcSource']
    opDf = pandas.DataFrame(opData, columns=opColumns, index=list(range(len(opData))))

    filterColumns = ['filter', 'listName', 'stack', 'type', 'url']
    filterDf = pandas.DataFrame(filterData, columns=filterColumns, index=list(range(len(filterData))))

    cookieColumns = ['cookie', 'value', 'domain', 'maxAge', 'extensions', 'path', 'secure', 'httpOnly', 'expires']
    cookieDf = pandas.DataFrame(cookieData, columns=cookieColumns, index=list(range(len(cookieData))))

    return opDf, filterDf, cookieDf

#Wrapper for bypassing KeyErrors if given key is not present in dict
def safe_fetch(dict, key):
    try:
        return dict[key]
    except:
        return None

#Test
if __name__=="__main__":
    args = sys.argv
    opDf, filterDf, cookieDf = parse_inspection('phoenix.edu', 'iPhone4')
    geolocationDf = opDf[opDf['funcSource'].str.contains('geolocation', na=False, case=False)]
    print(geolocationDf.head()['funcSource'].values)    
