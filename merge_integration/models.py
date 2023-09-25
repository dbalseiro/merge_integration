import pdb
from typing import Callable, Optional, TypeVar
from merge.resources.crm.types.account import Account
from merge.resources.crm.types.contact import Contact
from merge.resources.crm.types.contact_account import ContactAccount
from pydantic import BaseModel


A = TypeVar("A")
B = TypeVar("B")


def opt_chain(a: Optional[A], f: Callable[[A], Optional[B]]) -> Optional[B]:
    if v := a:
        return f(v)
    else:
        return None


class ThrvContact(BaseModel):
    name: str
    contact_id: str
    email: Optional[str]
    account: Optional[str]


def get_account_name(c: ContactAccount) -> Optional[str]:
    match c:
        case Account() as acc:
            return acc.name
        case str() as s:
            return s


def make_contact(c: Contact) -> ThrvContact:
    fname = c.first_name or ""
    lname = c.last_name or ""
    name = f"{fname} {lname}"
    cid = c.id or ""

    email = c.email_addresses[0].email_address if c.email_addresses else None

    account_name = opt_chain(c.account, get_account_name)

    return ThrvContact(name=name, email=email, account=account_name, contact_id=cid)
