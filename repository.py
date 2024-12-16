from fastapi import HTTPException, status
from google.cloud.firestore_v1 import FieldFilter

from config import Config as config
from firestoreDb import db
from schemas import RequestModel
from utils import Utilities, cipher


class UserRepository:

    def __init__(self):
        self.user_collection = db.collection(config.collection_name)

    async def get(self):
        users = []
        for doc in self.user_collection.stream():
            user_data = doc.to_dict()
            user_data['id'] = doc.id   # attaching a document id with object
            users.append(user_data)
        return users

    async def create(self, request: RequestModel):
        model_type = request.model_type  # capturing model type to check model
        del request.model_type
        doc_id = str(Utilities.generateID())
        data = request.dict()
        if model_type == 'p1':
            doc_ref = self.user_collection.where(filter=FieldFilter('email', '==', request.email)).get()
            if len(doc_ref) != 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with email already existed')
            data['password'] = cipher.encrypt(data['password'])
        self.user_collection.document(doc_id).set(data)
        model = Utilities.check_model_source(model_type)
        return model(**self.user_collection.document(doc_id).get().to_dict()), doc_id

    async def update(self, request: RequestModel, user_id: str):
        model_type = request.model_type  # capturing model type to check model
        del request.model_type
        model = Utilities.check_model_source(model_type)
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
