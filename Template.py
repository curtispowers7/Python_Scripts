#---------------------------------------------------------------------------------------------------------------------

#IMPORT OTHER LIBRARIES NEEDED FOR THE MODULE

#---------------------------------------------------------------------------------------------------------------------
import os #used to access items relating to the OS
import sys #used to help with logging and adding custom code
sys.path.insert(1, os.getenv('PythonScripts')) #The environment variable for 'PythonScripts' is set to include a path to my scripts folder
import myfunc #custom functions created by me (like jprint)

#---------------------------------------------------------------------------------------------------------------------

#DEFINE THE GLOBAL VARIABLES

#---------------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------------------------

#DEFINE THE FUNCTIONS NEEDED

#---------------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------------------------

#DEFINE THE MAIN FUNCTION

#---------------------------------------------------------------------------------------------------------------------
def main():
    #configure logging
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s - %(message)s', 
        level=logging.DEBUG,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info('Initialized logging')
    
    

#---------------------------------------------------------------------------------------------------------------------

#THE BODY OF THE SCRIPT

#---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
