# Captain
A mini-project and lab monitoring system for students and teachers to facilitate mini-project tracking and grading, course content management, student-teacher communication and interactive quizzes

## Run the app    
Note: Try with sudo   
Build for the first time:    
$ docker-compose -f docker-compose-dev.yml build    
Run:    
$ docker-compose -f docker-compose-dev.yml up     
To create the db:   
$ docker-compose -f docker-compose-dev.yml run users python manage.py recreate-db     
To fill db with dummy data:   
$ docker-compose -f docker-compose-dev.yml run users python manage.py seed-db     
     
Navigate to https://localhost:5001 to access    

### Troubleshooting/Documentation  
https://docs.google.com/document/d/1RD5zemjI8HsrGBTnk9Rd5r8WR7XYNg7RAyZBk2NE32U/edit?usp=sharing
