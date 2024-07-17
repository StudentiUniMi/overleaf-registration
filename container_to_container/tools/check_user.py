import pymongo

def check_user(email_to_find: str, container_name:str = "overleafmongo", port: int = 27017) -> bool:
    client = pymongo.MongoClient(container_name, port)
    db = client.sharelatex
    users = db.users

    search_result = users.find_one({"email": email_to_find})
    if search_result is None:
        return False
    else:
        return True

