# ReMark Backend

This is the backend for ReMark (a website annotation tool). It is built using `Flask`. The APIs are RESTful and are made using `Flask-RESTful`.

<br>

# Basic setup

Follow these steps to setup the backend server locally

<br>

Clone the project
```bash
  git clone ...
```

Go to the project directory
```bash
  cd my-project
```

Create a virtual environment in the project folder

```bash
  python3 -m venv /path/to/new/virtual/environment
```

Install the dependencies using pip
```bash
  pip install - r requirements.txt
```

Run the development server 
```bash
  python main.py
```

<!-- Run the redis server
```bash
  redis-server
```
Run the celery server ( Main workers )
```bash
  celery -A app.celery worker -l INFO
```
Run the celery server ( Schedulers )
```bash
  celery -A app.celery beat --max-interval 1 -l info
``` -->
<br>

# Features 

- [] User Login / Signup
- [] Authentication and Authorization using JWT
- [] Admin Dashboard
- [x] Annotation Management
- [x] Comment Management
- [] Using webhooks for sending emails and SMS notifications and reminders
- [] Import and Export as Excel / CSV Jobs
- [] Pricing Options


# Specifications

### Models :

<br>

-  ```
    USER {
        user_id : str
        username : str
        email_id : str
        bio : str
        authority : str
        created_at : datetime.datetime
        modified_at : datetime.datetime
    }

    ```
-  ```
    WEBSITE {
        website_id : str
        website_url : str
        admin : str
        admin_type : str
        n_annotations : int
        annotation_limit : int
    }

   ```
-  ```
    ANNOTATION {
        annotation_id : str
        annotation_name : str
        website_id : str    
        website_uri : str 
        html_node_data_tag : str 
        tags : str 
        resolved : bool

        created_at : datetime.datetime
        updated_at : datetime.datetime

        created_by : str
        comments : list
    }
    ```
-  ```
    COMMENT {
        comment_id : str
        annotation_id : str
        content : str
        content_html : str

        parent_node : str

        upvotes : int
        downvotes : int
        
        mod_required : bool
        
        created_at : datetime.datetime
        updated_at : datetime.datetime

        created_by : str
    }

    ```

### API Documentation :

- [] Include `openapi.yaml` file