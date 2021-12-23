#Import the Libraries needed
import requests
import sys


#Create the functions used in the script
def returnHeaders (server, port):
    import sys
    import requests
    if port == '80':
        url = 'http://' + server + ':' + port
    else:
        url = 'https://' + server + ':' + port
    try:
        response = requests.get(url, verify=False)
        return response.headers
    except:
        return 'Null'

def combineDictionaries (childDictionary, parentDictionary):
    for key in childDictionary.keys():
        if key in parentDictionary.keys():
            #add the value of the childDictionary key into the value of the parentDictionary key (which is the same key)
            allValues = []
            parentValues = parentDictionary[key]
            childValue = childDictionary[key]
            if isinstance(parentValues, list) and childValue not in parentValues:
                #add childDictionary values for this key to the parentDictionary values for this key and updated the parentDictionary
                allValues.append(childValue)
                allValues.append(parentValues)
                parentDictionary[key] = allValues
            else:
                pass #nothing to do here as the key/value pair from the childDictionary is already in the parentDictionary
        else:
            #add the key/value pair to the parent dictionary
            parentDictionary[key] = childDictionary[key]

#set a dictionary of servers to check
servers = {"google.com": ["80", "443"]}


#initiate the dictionary that will hold the server: headers values
headers = {}



#Go through all the servers and pull the headers from the service hosted on the ports
for server in servers.keys():
    port = servers[server]
    if isinstance(port, list):
        serverHeaders = []
        for p in port:
            serverHeaders.append(returnHeaders(server, p))
        headers[server] = serverHeaders
    else:
        serverHeaders = returnHeaders(server, port)
        headers[server] = serverHeaders




#create a unique dictionary of headers across all the servers
combinedHeaders = {}
for server in headers.keys():
    serverHeaders = headers[server]
    if isinstance(serverHeaders, list):
        #iterate through the list of header dictionaries for each port
        for portHeaders in serverHeaders:
            combineDictionaries(portHeaders, combinedHeaders)
    else:
        #add the headers for the server into the combinedHeaders dictionary
        combineDictionaries(serverHeaders, combinedHeaders)

print("There are {0} unique headers across {1} servers. The headers are as follows:".format(len(combinedHeaders.keys()), len(servers.keys())))
for header in combinedHeaders.keys():
    print("Header: {0} -------------- Value: {1}".format(header, combinedHeaders[header]))
    

