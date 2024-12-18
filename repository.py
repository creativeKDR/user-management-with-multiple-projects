from fastapi import HTTPException, status
from google.cloud.firestore_v1 import FieldFilter

from config import Config as config
from firestoreDb import db
from schemas import RequestModel
from utils import Utilities, cipher


class UserRepository:

    def __init__(self):
        self.user_collection = db.collection(config.collection_name)

    async def get(self, project_id: str):
        users = []
        for doc in self.user_collection.where(filter=FieldFilter('project_id', '==', project_id)).stream():
            user_data = doc.to_dict()
            user_data['id'] = doc.id   # attaching a document id with object
            users.append(user_data)
        return users

    async def create(self, request: RequestModel, project_source: str, model):
        doc_id = str(Utilities.generateID())
        if project_source == 'project3':
            request.dob = request.to_firestore()
        if project_source == 'project1':
            doc_ref = self.user_collection.where(filter=FieldFilter('email', '==', request.email)).get()
            if len(doc_ref) != 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with email already existed')
            request.password = cipher.encrypt(request.password)
        else:
            doc_ref = self.user_collection.where(filter=FieldFilter('mobile_no', '==', request.mobile_no)).get()
            if len(doc_ref) != 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with mobile no already existed')
        self.user_collection.document(doc_id).set(request.dict())
        return model(**self.user_collection.document(doc_id).get().to_dict()), doc_id

    async def update(self, request: RequestModel, user_id: str, project_source: str, model):
        if project_source == 'project3':
            request.dob = request.to_firestore()
        if project_source == 'project1':
            request.password = cipher.encrypt(request.password)
        doc_ref = self.user_collection.document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.set(request.dict())
            return model(**self.user_collection.document(user_id).get().to_dict())
        else:
            return None

    async def delete(self, user_id: str):
        doc_ref = self.user_collection.document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.delete()
            return {"message": "User deleted successfully"}
        else:
            return None
