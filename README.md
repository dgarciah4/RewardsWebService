# Rewards Web Service

# Description: This application immitates a basic rewards web service to spend and keep track points and from payer and user

# Database: SQLite

# Front-End Tools
## Tables 
    1.) user: Contains timestamp, payer and points data for each transaction
    2.) amounts: Reference database used to track total amount of points
    3.) accUser: Accounting database used to track balances of each payer after spending

# Programming Languages: Python, Javascript, HTML/CSS
# Environment: Flask
# Technologies Used for Development: Atom, Visual Code, Git, DB Browser

## STEPS TO CREATE AND RUN FLASK ENVIRONMENT FOR WEBSITES

1.)	Navigate to folder where environment will be created

2.)	Ensure requirements.txt file is in the folder where the environment will be startted locally.

3.)	Create the virtual environment using conda as followed:
- conda create -n <environment_name> python=3.7

4.)	Activate environment using the method below:
- activate <environment_name>

5.)	Inside the environment we will install the modules from the requirements file as followed
- pip install -r requirements.txt

6.) To run application, user must run the following command in their terminal
- python app.py

7.) Once the terminal notifies that the application is running, use your web browser and enter the following entry into the URL to open the web service
- http://127.0.0.1:5000/

8.) To quit the web service environment, user can enter the following at any point into their terminal.
- CTRL + C

# Screenshots
![1](capture2.png)
![2](capture3.png)
![3](capture4.png)
![4](capture5.png)
![6](capture6.png)
![7](capture1.png)

