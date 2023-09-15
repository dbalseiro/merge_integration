from merge.resources.crm.types.contact import Contact
from merge.resources.crm.types.paginated_contact_list import PaginatedContactList
from merge_integration.models import ThrvContact

from merge.client import Merge


def get_all_contacts(merge_client: Merge) -> list[ThrvContact]:
    def make_contact(c: Contact) -> ThrvContact:
        name = f"{c.first_name} {c.last_name}"
        email = c.email_addresses[0].email_address if c.email_addresses else None
        return ThrvContact(name=name, email=email)

    def make_contacts(paginated_contacts: PaginatedContactList) -> list[ThrvContact]:
        match paginated_contacts.results:
            case None:
                return []
            case l:
                contacts = [make_contact(c) for c in l]
                match paginated_contacts.next:
                    case None:
                        return contacts
                    case next:
                        return contacts + make_contacts(
                            merge_client.crm.contacts.list(cursor=next)
                        )

    contacts = merge_client.crm.contacts.list()
    return make_contacts(contacts)
