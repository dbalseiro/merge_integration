import uuid
from typing import Optional
from merge.resources.crm.types.note_request import NoteRequest
from merge.resources.crm.types.paginated_contact_list import PaginatedContactList
from merge.resources.crm.types import CategoriesEnum
from merge.client import Merge


def get_link_token(merge_client: Merge) -> str:
    origin = uuid.uuid4()
    ltok = merge_client.crm.link_token.create(
        end_user_email_address="dbalseiro@stackbuilders.com",
        end_user_organization_name="SB",
        end_user_origin_id=str(origin),
        categories=[CategoriesEnum.CRM],
    )
    return ltok.link_token


def get_private_token(merge_client: Merge, public_token: str) -> str:
    tok = merge_client.crm.account_token.retrieve(public_token)
    return tok.account_token


def get_all_notes_from_contact(merge_client: Merge, cid: Optional[str]) -> list[str]:
    if cid == "":
        return []
    notes = merge_client.crm.notes.list(contact_id=cid)
    return [x.content for x in notes.results or [] if x.content]


def get_all_contacts(merge_client: Merge, page: Optional[str]) -> PaginatedContactList:
    contacts = merge_client.crm.contacts.list(
        cursor=page, page_size=10, expand="account"
    )
    return contacts


def add_note(merge_client: Merge, note: str, cid: str) -> None:
    noteModel = NoteRequest(
        content=note,
        contact=cid,
        owner=None,
        account=None,
        opportunity=None,
        integration_params=None,
        linked_account_params=None,
        remote_fields=None,
    )
    result = merge_client.crm.notes.create(model=noteModel)
    if result.errors:
        raise Exception("Error adding note")
