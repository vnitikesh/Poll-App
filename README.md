

This is a sample polling application where the students of various colleges are participated 
in their respective domains.
The registered person can vote for the participants according to their choices.

Those participant(s) who got the maximum number of votes at the end of day will be assigned as 
the "winner of the day" and the respective college will gain some amount of upthrust in their
performance chart.

The person who wants to be the part of this poll can participate on behalf of their college by
hitting pull request for their registration process.


Setup Process:- 
Make sure python3 is installed on your machine. If not goto https://www/python.org/downloads and download the current version
of python and add it to the necessary path.

1. Open the command line terminal by pressing 'windows key + r', enter cmd in Run prompt and hit enter.
2. In the terminal switch to the directory where you want to run this project by entering 'cd dir_name'.
3. Now switch to virtual environment by following steps:-
      a).In the terminal, install the virtual environment configuration by inputting command 'pip install virtualenvwrapper'.
      b).After virtual environment is installed, create a virtual env. by inputting command 'mkvirtualenv venv'.
      
  If you have virtual env. installed in your system previously, skip the step (a).
  
Note:- Make sure git for desktop is installed in your system for easily cloning of the project otherwise you can download
   the zip file in the directory where you want to run this project.
  
4. For git desktop users)Clone the project by giving the command:- git clone https://github.com/ankuspidy/Poll-App.git
5. In the terminal, switch to the directory of the project by inputting 'cd Poll-App'. 
6. Install the necessary dependencies for the project by giving the command:- 'pip install -r requirements.txt'




Your project is ready to run on your local server environment.

7. Give the command:- 'python manage.py runserver'
8. Open the browser and in the url pad type 127.0.0.1:8000//dappx/register
9. Register yourself by providing username, password and email.

That's all you are registered for the website.

10. Now go to login section, provide necessary credentials and wholla!!! you have access to the dashboard.


***  Test cases for the project is present at the location Poll-App/dappx/tests.py 

In order to Run all the test cases:- Go to terminal and enter the command 'python manage.py test dappx' 


***  In order to get the coverage report follow the steps:-
            Step1:- pip install coverage
            Step2:- coverage erase(Erase all the previous variables.)
            Step3:- coverage run manage.py test dappx
            Step4:- coverage report -m
      
   
   
   
   
    
