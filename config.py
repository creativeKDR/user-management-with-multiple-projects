from schemas import ProjectOneUser, ProjectTwoUser, ProjectThreeUser


class Config:
    version = 'v1'
    firestore_db_path = "stock-app-46ee5-firebase-adminsdk-pbbps-fb48412005.json"
    collection_name = 'users'
    aes_iv = bytearray(16)
    aes_key = 'QTdIBCPpxA103nxx'
    project_source = {
        'p1': ProjectOneUser,
        'p2': ProjectTwoUser,
        'p3': ProjectThreeUser
    }
