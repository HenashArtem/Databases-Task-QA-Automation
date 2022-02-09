To start this project, you should follow these steps:
(1):
   1. Create gmail test account.
   2. Place the email and password of the created account in the directory of this project in the
      file "tests/test_data/gmail_test_data.py" in the variables "email" and "password". 
   3. Follow the link: "https://console.cloud.google.com/".
   4. In the top panel select "Select a project" -> "New project".
   5. After the project is created in the side menu, select "APIs & Services" -> "OAuth consent screen".
   6. Select User Type - External, click "Create".
   7. In the "OAuth consent screen" tab, fill in only the required fields (the "App name" field must be
      different from the existing ones) - all other tabs leave the default field.
   8. After creating, click "Publish App".
   9. In the side menu, select "APIs & Services" -> "Library" -> enter "Gmail API" in the search field -> select from
      the proposed list "Gmail API" -> click "Enable".
   10. In the side menu, select "APIs & Services" -> "Credentials" -> at the top of the page, 
      click "+ Create Credentials" -> "OAuth Client ID" -> select the application type "Desktop app" -> save the file
      with the received credits to your computer in JSON format in the directory of this project to the 
      folder "tests/test_data/" and name the file "client_secret.json".

(2):
   1. Deploy mysql server locally, restore database from dump(https://github.com/a1qatraineeship/db_task_dump).
   2. Place the host and user and password of the database in the directory of this project in the
      file "tests/config/sql_params.py" to class "SqlParams" in the class fields
      "host", "user" and "db_password". 