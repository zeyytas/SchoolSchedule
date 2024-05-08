# Installation Guide

This guide will help you set up and run the application locally using Docker, and it will also cover endpoints and running tests.

## Prerequisites
Docker installed on your machine.
 
## Installation Steps
1. Clone the repository to your local machine.

    ```shell
    git clone https://github.com/zeyytas/SchoolSchedule.git
    ```

2. Go to the root directory of the project.
   
   ```shell
   cd SchoolSchedule
   ```

3. You need to create the database schooldb.
   1. Connect to the PostgreSQL server using the `psql` command-line utility.
   2. Once connected, you can create a new database with the following SQL command
      ```bash
      CREATE DATABASE schooldb;
      ```

4. Build the Docker images using Docker Compose.
   
   ```shell
   docker-compose build
   ```

5. Start all Docker containers.

   ```shell
   docker-compose up
   ```

6. The application should now be accessible at _http://localhost:8000_.


## Endpoints

### 1. GET /api/v1/schedule/  
Retrieve a list of schedules.  

**Query Parameters**

1. **class_name**: _string_

   Filter schedules by the name of the school class.  


3. **teacher_name**: _string_

   Filter schedules by the name of the teacher.   


5. **subject_name**: _string_

   Filter schedules by the name of the subject.  


5. **day_of_week**: _string_

   Filter schedules by the day of the week. Use a full name, e.g., "Monday", "Tuesday", etc.  


7. **hour**: _integer_

   Filter schedules by the hour. It should be between 8 and 15.  


9. **for_today**: _boolean_

   Filter schedules for the current day.  



**Example Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "day_of_week": "Monday",
      "hour": 14,
      "subject": {
        "name": "science"
      },
      "teacher": {
        "name": "James Sullivan"
      },
      "class": {
        "name": "8A",
        "student_count": 0
      }
    }
  ]
}
```

### 2. POST /api/token/  
Handles the generation and refreshing of access tokens.

**Example Body:**
```json
{
  "username": "<user-name>",
  "password": "<password>"
}
```

**Example Response:**    
```json
{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}
```  


## Running Tests  

To ensure the correctness and stability of the application, automated tests are provided. These tests cover various aspects of the application.

To run tests, follow these steps:
1. Ensure that the Docker containers are running.
2. Open a new terminal window.
3. Navigate to the project directory.
4. Run pytest.

   ```shell
   docker-compose exec web pytest school/tests/tests.py
   ```

## Additional Information
- The application uses Django Rest Framework for API development.
- PostgreSQL is used as the database.
- The Docker Compose configuration ensures that all services required by the application are running together seamlessly.
