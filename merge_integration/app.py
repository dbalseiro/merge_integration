from flask import Flask, make_response, render_template, request, redirect
from merge.client import Merge
from merge_integration.controllers import (
    add_note,
    get_all_contacts,
    get_all_notes_from_contact,
)
from merge_integration.environment import MergeCfg, get_configuration_value

import pdb

from merge_integration.models import make_contact

app = Flask(__name__)

api_key = get_configuration_value(MergeCfg.MERGE_API_KEY)
account_token = get_configuration_value(MergeCfg.MERGE_ACCOUNT_TOKEN)
merge_client = Merge(api_key=api_key, account_token=account_token)


@app.route("/")
def index():
    cursor = request.cookies.get("cursor")
    all_contacts = get_all_contacts(merge_client, cursor)
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
    all_notes = get_all_notes_from_contact(merge_client, cid)
    return render_template("notes.html", notes=all_notes, cid=cid)

@app.post("/new-note")
def new_note():
    cid = request.form.get("cid")
    note = request.form.get("note")
    if cid and note:
        add_note(merge_client, note, cid)
    response = make_response(redirect("/"))
    return response
