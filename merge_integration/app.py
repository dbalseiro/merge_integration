from flask import Flask, render_template
from merge.client import Merge
from merge_integration.controllers import get_all_contacts
from merge_integration.environment import MergeCfg, get_configuration_value

app = Flask(__name__)

api_key = get_configuration_value(MergeCfg.MERGE_API_KEY)
account_token = get_configuration_value(MergeCfg.MERGE_ACCOUNT_TOKEN)
merge_client = Merge(api_key=api_key, account_token=account_token)

@app.route("/")
def index():
    contacts = get_all_contacts(merge_client)
    return render_template("index.html", contacts=contacts)
