#Author: Curtis Powers
#Intent: To create a module that can be imported later for use with other scripts when I need information regarding a Windows installation



#Import the libraries needed
import winreg
import platform

#Returns an array of subkeys for a given key path and hive
def enumSubKeys(strPath, hive):
    hive = winreg.ConnectRegistry(None, hive)
    key = winreg.OpenKey(hive, strPath)
    
    arrSubKeyPaths = []
    
    counter = 0
    while True:
        try:
            SubKeyPath = winreg.EnumKey(key, counter)
            arrSubKeyPaths.append(strPath + "\\" + SubKeyPath)
            counter+=1
        except:
            break
    return arrSubKeyPaths
    
#Returns a dictionary of values for a registry key
def enumKeyValues(strPath, hive):
    hive = winreg.ConnectRegistry(None, hive)
    key = winreg.OpenKey(hive, strPath)
    
    dictKeyValues = {}
    
    counter = 0
    while True:
        try:
            keyValue = winreg.EnumValue(key, counter)
            dictKeyValues[keyValue[0]] = keyValue[1]
            counter+=1
        except:
            break
    return dictKeyValues

#Returns a dictionary of installed software on the local machine
def enumInstalledSoftware():
    hive = winreg.HKEY_LOCAL_MACHINE
    if platform.architecture()[0] == '64bit':
        #Software install locations on 64 bit windows devices
        keys = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall']
    else:
        #On 32 bit windows devices, software is only installed here
        keys = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall']
    
    dictInstalledSoftware = {}
    
    #Iterates through all the sub keys for the keys specified above and adds all the values from those subkeys to a dictionary for the installed software
    for key in keys:
        arrSubKeys = enumSubKeys(key, hive)
        for subKey in arrSubKeys:
            dictSubKeyValues = enumKeyValues(subKey, hive)
            try:
                if dictSubKeyValues['DisplayName'] and dictSubKeyValues['DisplayVersion']:
                    dictInstalledSoftware[subKey.split("\\")[-1]] = dictSubKeyValues
            except KeyError:
                pass
    
    return dictInstalledSoftware

#Returns a dictionary of the os information from the local machine  
def getOsInformation():
    hive = winreg.HKEY_LOCAL_MACHINE
    key = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion'
    
    osDetails = enumKeyValues(key, hive)
    
    keysToKeep = ['CurrentBuild', 'DisplayVersion', 'ProductName']
    
    osInformation = {key: osDetails[key] for key in keysToKeep}
    
    return osInformation
    
    
    
    
    
    
    
if __name__ == "__main__":
    installedSoftware = enumInstalledSoftware()
    versionInfo = getOsInformation()
    for software in installedSoftware.keys():
        print(installedSoftware[software]['DisplayName'], "-------------", installedSoftware[software]['DisplayVersion'])
        
    for info in versionInfo.keys():
        print(info, "-------------", versionInfo[info])
