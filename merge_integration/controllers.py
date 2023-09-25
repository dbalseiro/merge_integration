import pdb
from typing import Optional
from merge.resources.crm.types.note_request import NoteRequest
from merge.resources.crm.types.paginated_contact_list import PaginatedContactList

from merge.client import Merge


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
