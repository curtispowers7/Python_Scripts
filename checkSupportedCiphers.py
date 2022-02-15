#import the libraries needed
import ssl, socket, re, time, multiprocessing, json

#function to check if a specific cipher will work to establish a connection with a specific host/port combination
def testSocketConnection(cipher, hostname, port):
    context = ssl.create_default_context()
    try:
        context.set_ciphers(cipher)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sslSock = context.wrap_socket(sock, server_hostname = hostname)
        try: 
            sslSock.connect((hostname, port))
            print("Success at connection to {0} with {1}".format(hostname, cipher))
            sslSock.close()
            sock.close()
            return True
        except:
            print("Failure to connect to {0} with {1}".format(hostname, cipher))
            return False
    except:
        print("Not able to set cipher of {0}".format(cipher))
        pass

#function to check all ciphers offered by openSSL for connectivity
def testServerConnection(hostname, port):
    ciphers = ["TLS_AES_256_GCM_SHA384", 
    "TLS_CHACHA20_POLY1305_SHA256", 
    "TLS_AES_128_GCM_SHA256", 
    "TLS_AES_128_CCM_SHA256", 
    "ECDHE-ECDSA-AES256-GCM-SHA384", 
    "ECDHE-RSA-AES256-GCM-SHA384", 
    "ECDHE-ECDSA-CHACHA20-POLY1305", 
    "ECDHE-RSA-CHACHA20-POLY1305", 
    "ECDHE-ECDSA-AES256-CCM", 
    "ECDHE-ECDSA-AES128-GCM-SHA256", 
    "ECDHE-RSA-AES128-GCM-SHA256", 
    "ECDHE-ECDSA-AES128-CCM", 
    "ECDHE-ECDSA-AES128-SHA256", 
    "ECDHE-RSA-AES128-SHA256", 
    "ECDHE-ECDSA-AES256-SHA", 
    "ECDHE-RSA-AES256-SHA", 
    "ECDHE-ECDSA-AES128-SHA", 
    "ECDHE-RSA-AES128-SHA", 
    "AES256-GCM-SHA384", 
    "AES256-CCM", 
    "AES128-GCM-SHA256", 
    "AES128-CCM", 
    "AES256-SHA256", 
    "AES128-SHA256", 
    "AES256-SHA", 
    "AES128-SHA", 
    "DHE-RSA-AES256-GCM-SHA384", 
    "DHE-RSA-CHACHA20-POLY1305", 
    "DHE-RSA-AES256-CCM", 
    "DHE-RSA-AES128-GCM-SHA256", 
    "DHE-RSA-AES128-CCM", 
    "DHE-RSA-AES256-SHA256", 
    "DHE-RSA-AES128-SHA256", 
    "DHE-RSA-AES256-SHA", 
    "DHE-RSA-AES128-SHA", 
    "PSK-AES256-GCM-SHA384", 
    "PSK-CHACHA20-POLY1305", 
    "PSK-AES256-CCM", 
    "PSK-AES128-GCM-SHA256", 
    "PSK-AES128-CCM", 
    "PSK-AES256-CBC-SHA", 
    "PSK-AES128-CBC-SHA256", 
    "PSK-AES128-CBC-SHA", 
    "DHE-PSK-AES256-GCM-SHA384", 
    "DHE-PSK-CHACHA20-POLY1305", 
    "DHE-PSK-AES256-CCM", 
    "DHE-PSK-AES128-GCM-SHA256", 
    "DHE-PSK-AES128-CCM", 
    "DHE-PSK-AES256-CBC-SHA", 
    "DHE-PSK-AES128-CBC-SHA256", 
    "DHE-PSK-AES128-CBC-SHA", 
    "ECDHE-PSK-CHACHA20-POLY1305", 
    "ECDHE-PSK-AES256-CBC-SHA", 
    "ECDHE-PSK-AES128-CBC-SHA256", 
    "ECDHE-PSK-AES128-CBC-SHA"]
    enabledCiphers = []
    if isinstance(port, str):
        port = int(port)
    for cipher in ciphers:
        if testSocketConnection(cipher, hostname, port):
            enabledCiphers.append(cipher)
        else:
            pass
    return enabledCiphers
    
#main function that drives the multiprocessing 
def main(hostname, ports, returnCiphers):
    print("starting test for {0}".format(hostname))
    if isinstance(ports, list):
        portCiphers = {}
        for port in ports:
            print("starting test for {0}".format(port))
            enabledCiphers = testServerConnection(hostname, port)
            portCiphers[port] = enabledCiphers
        returnCiphers[hostname] = portCiphers
    else:
        port = ports
        print("starting test for {0}".format(port))
        enabledCiphers = testServerConnection(hostname, port)
        returnCiphers[hostname] = enabledCiphers






         



#The body of the script that establishes the multiprocessing for the main function
if __name__ == "__main__":
    start = time.time()
    manager = multiprocessing.Manager()
    hostCiphers = manager.dict()
    
    dictHosts = {'google.com': 443, 'bing.com': 443, 'youtube.com': 443}
    
    processList = []
    for host in dictHosts.keys():
        process = multiprocessing.Process(target=main, args=[host, dictHosts[host], hostCiphers])
        process.start()
        processList.append(process)
    
    for process in processList:
        process.join()
    end = time.time()
    print("process finished in {}".format(end - start))
    print(hostCiphers)
    with open('results.json', 'w') as resultsFile:
        resultsFile.write(json.dumps(hostCiphers.copy()))
    
    

