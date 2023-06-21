import os
from google.cloud import firestore
from google.oauth2 import service_account
from typing import Dict, Optional, Any, List
import logging
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class SelectModel(BaseModel):
    collection_id: str
    filters: Optional[Dict[str, Any]]
    order_by: Optional[List[OrderByModel]]
    limit: Optional[int]

class OrderByModel(BaseModel):
    field: str
    ascending: Optional[bool] = False

class InsertModel(BaseModel):
    collection_id: str
    inserts: Dict[str, Any]

class UpdateModel(BaseModel):
    collection_id: str
    doc_id: str
    updates: Dict[str, Any]

class DeleteModel(BaseModel):
    collection_id: str
    doc_id: str

class FirestoreInterface:
    def __init__(self, project_id=None, credentials_path=None):
        self.project_id = project_id if project_id else os.getenv('GOOGLE_CLOUD_PROJECT_ID')
        credentials_path = credentials_path if credentials_path else os.getenv('GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')
        self.client = firestore.Client(
            credentials=service_account.Credentials.from_service_account_file(credentials_path),
            project=self.project_id
        )
        # Include the models so they can be accessed easier outside the class
        self.SelectModel = SelectModel
        self.OrderByModel = OrderByModel
        self.UpdateModel = UpdateModel
        self.InsertModel = InsertModel
        self.DeleteModel = DeleteModel

    def select(self, model: SelectModel):
        try:
            collection = self.client.collection(model.collection_id)
            if model.filters:
                for field, value in model.filters.items():
                    collection = collection.where(field, '==', value)
            if model.order_by:
                for order in model.order_by:
                    direction = firestore.Query.ASCENDING if order.ascending else firestore.Query.DESCENDING
                    collection = collection.order_by(order.field, direction=direction)
            if model.limit:
                collection = collection.limit(model.limit)
            docs = collection.stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            logging.error(f"Error in select: {e}")
            raise

    def insert(self, model: InsertModel):
        try:
            doc_ref = self.client.collection(model.collection_id).document()
            doc_ref.set(model.inserts)
        except Exception as e:
            logging.error(f"Error in insert: {e}")
            raise

    def update(self, model: UpdateModel):
        try:
            doc_ref = self.client.collection(model.collection_id).document(model.doc_id)
            doc_ref.update(model.updates)
        except Exception as e:
            logging.error(f"Error in update: {e}")
            raise

    def delete(self, model: DeleteModel):
        try:
            doc_ref = self.client.collection(model.collection_id).document(model.doc_id)
            doc_ref.delete()
        except Exception as e:
            logging.error(f"Error in delete: {e}")
            raise
