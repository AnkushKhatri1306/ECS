# ECS

Hi,	Greeting for the day

* In this project i have used Python, Django and PostgreSQL ( Database )

For requirement clarification you can see the ECS.ZIP file in project tree .

Steps to run the code :
	1. First install required dependencies mentioned in requirement.txt file in project directory.
	2. After that go to setting.py file and update the database information according to your Database name and configuration
	3. Go to the path where manage.py file is present and then run commands and mentioned
		- python manage.py makemigrations
		- python manage.py migrate
		- python manage.py runserver 127.0.0.1:5000
	4. Now you all set to run the program
	

After Django App is running
	1. Upload the data to the App or create it into database for this there is 2 API is given 
		- http://localhost:5000/course/data_upload/
		- http://localhost:5000/course/
		check both the API in views,py file for more information.
		

