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

<br>

# Todo

- [ ] **Differentiate admins** : In login method, return a boolean / str indicating whether the logged in admin is actually the admin of the website ( This arises because the user for one website can be the admin for another )
- [x] Add upvotes and downvotes to User
- [x] **Change the Annotation Model** : Store the annotation by using `XPath` instead of `data-` attribute
- [x] Debug CREATE website issue
- [x] Create `User Preference` model
- [x] Create defaults and basic API for user preference model ~~(OPTIONAL - Handled in the frontend)~~
- [x] Add a secondary field for identifying HTML node ( in case xpath fails )
- [x] Fix edge cases in comment voting

- [x] Configure logger
- [ ] Write tests for APIs :
  - [x] AuthAPI
  - [ ] UserAPI (PUT and DELETE are left)
  - [x] TokenAPI
  - [x] WebsiteAPI
  - [x] AnnotationAPI
  - [x] CommentAPI
  - [ ] UserPreferenceAPI (**OPTIONAL**) 
- [ ] Write the documentation for testing (**OPTIONAL**)

# Features 

- [x] User Login / Signup
- [x] Authentication and Authorization using JWT
- [x] Admin Dashboard
- [x] Annotation Management
- [x] Comment Management
- [ ] ~~Pricing Options~~


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
    TOKEN {
      user_id : str
      api_key : str
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
        node_xpath : str 
        tags : str 
        resolved : bool

        created_at : datetime.datetime
        updated_at : datetime.datetime

        created_by_id : str
        created_by : str
        
        modified_by_id : str
        modified_by : str
        
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

- [ ] Include `openapi.yaml` file
- [ ] Include Insomnia API file

# Optional Featues (May be added in the future)

($P_i$ stands for priority and $P_1 > P_2 > ... P_n$)

- ($P_1$) Nested comments ( DB implementation present but need to parse it properly )
- ($P_1$) Import and Export as Excel / CSV Jobs
- ($P_2$) Using webhooks for sending emails and SMS notifications
- ($P_2$) Groups and IAM for organizations
