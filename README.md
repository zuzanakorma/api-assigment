# API ASSIGNMENT

This application uses Flask with Python 3.

## API Structure
* List all packages
  
    ```url
    http://127.0.0.1:5000/api/v1.0/packages
    ```
    The response includes all the packages in the JSONPath $.packages

* List a package details
  
    ```url
    http://127.0.0.1:5000/api/v1.0/packages/<package_name>
    ```

    The response includes the package details: package, description, dependencies (including alternates), and reverse dependencies

## Installation

Clone this repo.
```shell
git clone https://github.com/zuzanakorma/api-assigment.git
```

(Optional) Create a virtualenv and activate.
```shell
python3 -m venv venv
source venv/bin/activate
```

Install application requirements.
```shell
pip install -r requirements.txt
```

Run the application.
```shell
flask run
```

Test the application.
* List all packages: http://127.0.0.1:5000/api/v1.0/packages
* List screen package: http://127.0.0.1:5000/api/v1.0/packages/screen
