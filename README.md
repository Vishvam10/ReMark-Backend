# ReMark Backend

This is the backend server for ReMark (a website annotation tool. More about that [here](https://github.com/Vishvam10/ReMark-Client)). It is built using `Flask`. The APIs are RESTful and are made using `Flask-RESTful`. The primary database, for development, testing and production is `sqlite3`. That is used with `SQLAlchemy` and `Flask-Migrate` to abstract the database. **The production DB however will be migrated to `PostgreSQL` in the near future**

<br>

# Basic setup (Self hosting)

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

Activate the virtual environment
```
  .\venv\Scripts\activate
```

**NOTE :** Please visit this [link](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/) to know more about installing virtual environments

<br>

Install the dependencies using pip
```bash
  pip install - r requirements.txt
```

Run the development server 
```bash
  python app.py
```

<br>

# Testing

The backend is tested mostly using `pytest 7.1.2` and a bit of `coverage`. For the time being, the tests are all unit tests. Integration tests and other higher order tests will be performed in the future. 

For testing :
  - `app.config["TESTING"]` is set to `True`
  - the `app.config[SQLALCHEMY_DATABASE_URI]` is set to a local testing database in the `db_directory` folder


Please check whether `pytest` is installed in out local sytem by doing a quick :

```
  $ pytest --version
  (Output) pytest 7.1.2
```

If you get any errors, just do a pip install :

```
  pip install pytest coverage
```

For running a specific test file, use the `pytest` command. 

```
  pytest .\tests\unittests\APITests\test_Something.py
```

For redirecting the output to stdout (to show the `print()` statements), use the `-s` flag.

```
  pytest -s .\tests\unittests\APITests\test_Something.py
```

For testing a specific function in a testfile, use the `-k` flag :

```
 pytest -s .\tests\unittests\APITests\test_Something.py -k function_name
```

<br>

# Todo

- [x] **Differentiate admins** : In login method, return a boolean / str indicating whether the logged in admin is actually the admin of the website ( This arises because the user for one website can be the admin for another )
- [x] Add upvotes and downvotes to User
- [x] **Change the Annotation Model** : Store the annotation by using `XPath` instead of `data-` attribute
- [x] Debug CREATE website issue
- [x] Create `User Preference` model
- [x] Create defaults and basic API for user preference model ~~(OPTIONAL - Handled in the frontend)~~
- [x] Add a secondary field for identifying HTML node ( in case xpath fails )
- [x] Fix edge cases in comment voting

- [x] Configure logger
- [x] Write tests for APIs :
  - [x] AuthAPI
  - [x] UserAPI ~~(PUT and DELETE are left)~~
  - [x] TokenAPI
  - [x] WebsiteAPI
  - [x] AnnotationAPI
  - [x] CommentAPI
  - [ ] UserPreferenceAPI (**OPTIONAL**) 
- [ ] Write the documentation for testing (**OPTIONAL**)

# Features 

- ✅ **Works on any static site and delivers a good result on interactive components like popups, slideshows, hovering cards, etc.**
- ✅ **Works on various HTML elements** like `div`, `span`, `img`, `p`, all the `h` tags, `section`, and many more. Check out the [Remark Client documentation](https://github.com/Vishvam10/ReMark-Client) to know more.  
- ✅ Annotation Management 
- ✅ Comment Management with Upvotes, Downvotes and Nesting
- ✅ User and Admin Login / Signup
- ✅ Authentication and Authorization using JWT
- ✅ Admin Dashboard

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
        upvotes: str
        downvotes: str
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
        annotation_id: str
        annotation_name: str
        website_id: str
        website_uri: str
        node_xpath: str
        html_id: str
        html_tag: str
        html_text_content: str
        tags: str
        resolved: bool

        created_at: datetime.datetime
        updated_at: datetime.datetime

        created_by_id: str
        created_by: str

        modified_by_id: str
        modified_by: str

        comments: list
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

        created_by_id : str
        created_by : str
    }
    ```
-  ```
    USERPREFERENCE {
        user_id : str
        show_moderated_comments : bool
        comments_limit_per_annotation : int
        default_theme : str
        brand_colors : str
    }
    ```

### API Documentation :

- [] Include `openapi.yaml` file (**OPTIONAL**)
- [x] Include Insomnia API file (**OPTIONAL**)

<br>

# Optional Featues 

These be added in the future. (Pi stands for priority and P1 > P2 > ... Pn)

- (P1) Nested comments ( DB implementation present but need to parse it properly )
- (P1) Import and Export as Excel / CSV Jobs
- (P2) Using webhooks for sending emails and SMS notifications
- (P2) Groups and IAM for organizations

<br>

# Limitations

All though it can work with interactive components, there are cases where it **fails to annotate dynamic content**. For example, say there is a website that shows the whether of a location **given by the user**. Remark can annotate the weather modal component of (say) New York alone but upon rendering a completely new data, the annotation is lost (though it is present in the DB)

> **Workaround** : Instead of annotating the dynamically changing child container :
>  - Annotate the parent container or
>  - Annotate an element that triggers the change or
>  - In the worst case, annotate the nearest static element

Dynamic content (the ones that are received from the server) are hard to annotate in general. Remark uses 4+ different checks to get the annotated DOM elemets. These include : `html_id` check, `html_class` check, `html_node_xpath` check (This was particularly hard to implement), `html_tag` + `html_text_content` check. Dynamic content have usually breaks all the checks because, well, it is dynamic. **Note that dynamic content that actually passes one of the checks are rendered properly. It is only those that fail all of them are not rendered.** Usually, the `html_id` remains the same. So, there are cases where the annotations are rendering properly. But to be in the same side, please follow the workarounds. 
