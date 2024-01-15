from flask import Flask, make_response, render_template, request, redirect
from merge.client import Merge
from merge_integration.controllers import (
    add_note,
    get_all_contacts,
    get_all_notes_from_contact,
    get_link_token,
    get_private_token,
)
from merge_integration.environment import MergeCfg, get_configuration_value, save_token
from merge_integration.models import make_contact

app = Flask(__name__)


class MyMerge:
    def __init__(self, m: Merge) -> None:
        self.merge = m


def update_merge_client(acctk: str, apik: str) -> Merge:
    merge_client = Merge(api_key=apik, account_token=acctk)
    return merge_client


api_key = get_configuration_value(MergeCfg.MERGE_API_KEY)

merge_client = MyMerge(
    update_merge_client(get_configuration_value(MergeCfg.MERGE_ACCOUNT_TOKEN), api_key)
)


@app.route("/")
def index():
    cursor = request.cookies.get("cursor")
    all_contacts = get_all_contacts(merge_client.merge, cursor)
    if contacts := all_contacts.results:
        thrv_contacts = [make_contact(a) for a in contacts]
        return render_template(
            "index.html",
            contacts=thrv_contacts,
            previous=all_contacts.previous,
            next=all_contacts.next,
            is_first_page=cursor == "" or cursor == None,
        )
    else:
        return "No contact found", 400


@app.route("/next")
def next():
    cursor = request.args.get("cursor")
    response = make_response(redirect("/"))
    response.set_cookie("cursor", cursor or "")
    return response


@app.route("/first")
def first():
    response = make_response(redirect("/"))
    response.set_cookie("cursor", "", expires=0)
    return response


@app.route("/notes")
def notes():
    cid = request.args.get("cid")
    all_notes = get_all_notes_from_contact(merge_client.merge, cid)
    return render_template("notes.html", notes=all_notes, cid=cid)


@app.post("/new-note")
def new_note():
    cid = request.form.get("cid")
    note = request.form.get("note")
    if cid and note:
        add_note(merge_client.merge, note, cid)
    return make_response(redirect("/"))


@app.get("/link-account")
def link_account():
    tok = get_link_token(merge_client.merge)
    return render_template("link-account.html", token=tok)


@app.get("/save-account-token")
def save_account_token():
    if pub_tok := request.args.get("public-token"):
        tok = get_private_token(merge_client.merge, pub_tok)
        save_token(tok)
        merge_client.merge = update_merge_client(tok, api_key)
        return make_response(redirect("/"))
    else:
        raise Exception("No token found")
