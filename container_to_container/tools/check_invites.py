import pymongo

def check_invites(email_to_find: str,container_name:str = "overleafmongo", port: int = 27017) -> bool:
    client = pymongo.MongoClient(container_name, port)
    db = client.sharelatex
    project_invites = db.projectInvites

    search_result = project_invites.find_one({"email": email_to_find})
    if search_result is None:
        return False
    else:
        return True

