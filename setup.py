from setuptools import setup, find_packages

setup(
    name='db_interfaces',
    version='0.1.0',
    url='https://github.com/Tom-Standen/db_interfaces',
    author='Tom-Standen',
    author_email='tstanden3@gmail.com',
    description='The DB Interfaces library provides a standardized way to interact with Firestore and BigQuery databases in Python projects. The library is designed to be easy to use, flexible, and compatible with modern cloud-based applications.',
    packages=find_packages(),
    install_requires=[
        'google-cloud-firestore>=2.11.1',
        'pydantic>=1.10.9',
        'python-dotenv>=1.0.0'
    ],
)
