

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

1. Open the IDE of your choice.
2. Switch to the directory where you want to store the projects file.
3. Activate the virtual environment.
4. Install the necessary dependencies by giving the command:- 'pip install -r requirements.txt'
5. Make sure git for desktop is installed in your system for easily cloning of the project otherwise you can download
   the zip file and setup the path variables.
6. Clone the project by giving the command:- git clone https://github.com/ankuspidy/Poll-App.git

Your project is ready to run on your local server environment.

7. Give the command:- 'py manage.py runserver'
8. Open the browser and in the url pad type 127.0.0.1:8000//dappx/register
9. Register yourself by providing username, password and email.

That's all you are registered for the website.

10. Now go to login section, provide necessary credentials and wholla!!! you have access to the dashboard.


*** The project also covers 'tests.py' file in the app section(dappx).
   a). Go to dappx.
   b). Open 'tests.py' file
   c). In order to check the test cases hit the command:- "py manage.py test dappx"
   d). There are some comment statement in tests.py file where some updates needs to be done.
   
   
   You can also check the coverage report through following steps.
   S1). coverage erase(erase all the old variables).
   S2). coverage run manage.py test dappx.
   S3). coverage report -m.
    
