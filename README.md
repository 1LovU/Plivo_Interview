# Plivo Interview GIT Repository

Objective : Working on Plivo's REST API to send SMS, check Balance , check Price plan, and confirm if the transaction was successful.

Environment : 
            1. Python 3.0+ interpreter.
            2. All the modules must be installed.
            3. Tested on Windows machine only (should work on any system).
           
Steps to Run :
            1. Keep the files "main.py", "api.ini", "url_hit.py" in a folder.
            2. Open command prompt and give the command "python <folder_path>/main.py sender_number reciever_number"
                  Example : python C:\Users\AMiT\PycharmProjects\plivo_api\main.py 13238318440 14153014770
NOTE :
            1. Please make sure to install the modules before running the script.
            2. After Message POST API hit, there is 200 Second pause because, it takes time to get the data updated.
            3. For PRICING API, I needed to use admin Auth_ID and Auth_Token. It was giving authorization Error otherwise.

Please mail me at theamitcoder@gmail.com for any Query.
            



