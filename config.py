from schemas import ProjectOneUser, ProjectTwoUser, ProjectThreeUser


class Config:
    version = 'v1'
    firestore_db_path = "user-managment-system-f4375-firebase-adminsdk-bnrd8-2d0dd56a61.json"
    collection_name = 'users'
    aes_iv = bytearray(16)
    aes_key = 'QTdIBCPpxA103nxx'
    project_source = {
        'p1': ProjectOneUser,
        'p2': ProjectTwoUser,
        'p3': ProjectThreeUser
    }
