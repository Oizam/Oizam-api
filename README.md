# Welcome to Oizam-Api!

Hello this is our Api to get and post some description of bird
The purpose of this **API** is to be us with ***Oizam-Kivy*** (Is an application python we can use for a app to android), so Oizam-Api is the back end *our organisation Oizam*

# Contents

Inide we have a file is call OiseauxFini.csv, is't our database we upload our postgreSQL databate, We use the data from [oiseaux.net](https://www.oiseaux.net/)

## instructions for launching it locally

In your favorite IDE, 

 1°) start to clone the project :

    https://github.com/Oizam/Oizam-api.git

 2°) You need to create an environment for python

    python3 -m venv myenv

 3°) Update your pip install 

    pip install --upgrade pip
    
 4°) Intall all package necessary

    pip install -r requirements.txt

5°) Before to start the application, you must change the 
DATABASE_URL = "<span style="color:red">YOUR_DATABASE_URL</span>"*** in file ***.env
