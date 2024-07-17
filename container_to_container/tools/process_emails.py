from email_validator import validate_email  # type: ignore
import email_validator
import json

from check_invites import check_invites
from check_user import check_user
from create_account import create_account

def process_emails(
    mail_address: str,
    config_file: str = "allowed_domains.json",
    blocked_user_file: str = "blocked_users.json",
    container_name_mongo:str = "overleafmongo", 
    port_mongo: int = 27017,
    container_name_overleaf: str = "overleafserver",
) -> bool:

    with open(config_file, "r") as file:
        allowed_domains: dict = json.load(file)

    with open(blocked_user_file, "r") as file:
        blocked_users: dict = json.load(file)

    if (mail_address == "") or (mail_address is None):
        return False
    try:
        emailinfo = validate_email(mail_address, check_deliverability=False)
        mail_address = emailinfo.normalized
    except email_validator.exceptions_types.EmailSyntaxError:
        return False
    except email_validator.exceptions_types.EmailNotValidError:
        return False

    for blocked_user in blocked_users["blocked_users"]:
        if mail_address == blocked_user:
            return False

    is_email_allowed: bool = False

    if check_invites(email_to_find=mail_address,container_name=container_name_mongo, port=port_mongo):
        is_email_allowed = True

    if check_user(email_to_find=mail_address,container_name=container_name_mongo, port=port_mongo):
        is_email_allowed = True

    if is_email_allowed is False:
        domain_found: bool = False
        for domain in allowed_domains["allowed_domains"]:
            if mail_address.endswith(domain):
                domain_found = True

        if domain_found is False:
            return False

    return create_account(email=mail_address, container_name=container_name_overleaf)

