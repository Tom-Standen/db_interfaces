DB Interfaces Library
The DB Interfaces library provides a standardized way to interact with Firestore and BigQuery databases in Python projects. The library is designed to be easy to use, flexible, and compatible with modern cloud-based applications.

Features
Easy integration with Firestore and BigQuery databases
Convenient models for select, insert, update, and delete operations
Handles setup and teardown of database connections
Can be used in any Python project or microservice
Installation
To install the library, you can use pip:

arduino
Copy code
pip install git+https://github.com/your_username/your_repository.git
Make sure to replace your_username and your_repository with your actual GitHub username and repository name.

Usage
First, import the interfaces you want to use:

python
Copy code
from db_interfaces import FirestoreInterface, BigQueryInterface
Then, initialize an instance of the interface:

python
Copy code
firestore_interface = FirestoreInterface()
bigquery_interface = BigQueryInterface()
You can then use the provided methods to interact with the database. For example:

python
Copy code
from db_interfaces import SelectModel

# Define the model for the select operation
select_model = SelectModel(collection_id="my_collection", filters={"field": "value"})

# Execute the select operation
documents = firestore_interface.select(select_model)

# The returned documents are a list of dictionaries
for document in documents:
    print(document)
Testing
This library includes a suite of tests to ensure everything is working as expected. To run the tests, you can use the following command:

Copy code
pytest
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

License
This project is licensed under the terms of the MIT license.