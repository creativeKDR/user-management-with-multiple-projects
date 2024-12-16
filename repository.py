from typing import Union

from config import Config as config
from firestoreDb import db
from schemas import ProjectOneUser, ProjectTwoUser, ProjectThreeUser
from utils import Utilities, cipher


class UserRepository:

    def __init__(self):
        self.user_collection = db.collection(config.collection_name)

    async def get(self):
        users = []
        for doc in self.user_collection.stream():
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            users.append(user_data)
        return users

    async def create(self, source: str, request: Union[ProjectOneUser, ProjectTwoUser, ProjectThreeUser]):
        doc_id = str(Utilities.generateID())
        data = request.dict()
        data['password'] = cipher.encrypt(data['password'])
        self.user_collection.document(doc_id).set(data)
        model = Utilities.check_model_source(source)
        return model(**self.user_collection.document(doc_id).get().to_dict()), doc_id

    async def update(self, source: str, request: Union[ProjectOneUser, ProjectTwoUser, ProjectThreeUser], user_id: str):
        model = Utilities.check_model_source(source)
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
