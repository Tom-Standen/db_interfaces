import os
from google.cloud import bigquery
from google.oauth2 import service_account
import datetime
from typing import Dict, Optional, Any, List
import logging
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class SelectModel(BaseModel):
    table_id: str
    select_cols: Optional[List[str]]
    filters: Optional[Dict[str, Any]]

class InsertModel(BaseModel):
    table_id: str
    params: Dict[str, Any]

class UpdateModel(BaseModel):
    table_id: str
    updates: Dict[str, Any]
    filters: Dict[str, Any]

class DeleteModel(BaseModel):
    table_id: str
    filters: Dict[str, Any]
    

class BigQueryInterface:
    def __init__(self):
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
        self.dataset_id = os.getenv("BIGQUERY_DATASET_ID")
        self.client = bigquery.Client(
            credentials=service_account.Credentials.from_service_account_file(os.getenv('GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')),
            project=self.project_id
        )
        self.type_map = {
            str: "STRING",
            int: "INT64",
            float: "FLOAT64",
            bool: "BOOL",
            bytes: "BYTES",
            datetime.datetime: "DATETIME",
            datetime.date: "DATE",
            datetime.time: "TIME",
        }

    def _get_query_job_config(self, params: Optional[Dict]) -> bigquery.QueryJobConfig:
        try:
            return bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter(name, self.type_map[type(value)], value) for name, value in params.items()]
            )
        except Exception as e:
            logging.error(f"Error in _get_query_job_config: {e}")
            raise

    def select(self, table_id: str, select_cols: Optional[List[str]] = None, filters: Optional[Dict[str, Any]] = None):
        try:
            # Prepare the where clause if filters are provided
            where_clause = " AND ".join([f"{field} = @{field}" for field in filters.keys()]) if filters else ""
            if where_clause:
                where_clause = "WHERE " + where_clause
            
            query = f"SELECT {', '.join(select_cols) or '*'} FROM `{self.project_id}.{self.dataset_id}.{table_id}` {where_clause}"
            job_config = self._get_query_job_config(filters or {})
            result = self.client.query(query, job_config=job_config).result()
            return [dict(row) for row in result]  # Convert to list of dicts
        except Exception as e:
            logging.error(f"Error in select: {e}")
            raise


    def insert(self, table_id: str, params: Dict):
        try:
            fields = ', '.join(params.keys())
            values = ', '.join([f'@{key}' for key in params.keys()])
            query = f"INSERT INTO `{self.project_id}.{self.dataset_id}.{table_id}` ({fields}) VALUES ({values})"
            job_config = self._get_query_job_config(params)
            self.client.query(query, job_config=job_config).result()
        except Exception as e:
            logging.error(f"Error in insert: {e}")
            raise

    def update(self, table_id: str, updates: Dict, filters: Optional[Dict[str, Any]] = None):
        try:
            set_clause = ', '.join([f"{key} = @{key}" for key in updates.keys()])
            # Prepare the where clause if filters are provided
            where_clause = " AND ".join([f"{field} = @{field}" for field in filters.keys()]) if filters else ""
            if where_clause:
                where_clause = "WHERE " + where_clause
            
            query = f"UPDATE `{self.project_id}.{self.dataset_id}.{table_id}` SET {set_clause} {where_clause}"
            job_config = self._get_query_job_config({**updates, **(filters or {})})
            self.client.query(query, job_config=job_config).result()
        except Exception as e:
            logging.error(f"Error in update: {e}")
            raise

    def delete(self, table_id: str, filters: Optional[Dict[str, Any]] = None):
        try:
            # Prepare the where clause if filters are provided
            where_clause = " AND ".join([f"{field} = @{field}" for field in filters.keys()]) if filters else ""
            if where_clause:
                where_clause = "WHERE " + where_clause

            query = f"DELETE FROM `{self.project_id}.{self.dataset_id}.{table_id}` {where_clause}"
            job_config = self._get_query_job_config(filters or {})
            self.client.query(query, job_config=job_config).result()
        except Exception as e:
            logging.error(f"Error in delete: {e}")
            raise
