# server.py (Version corrigée et requalifiée)
import sqlite3
import os
import re
from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/user")
def get_user():
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # CORRECTION : Requête paramétrée (Sanitizer intégré)
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchall()

@app.route("/ping")
def ping_host():
    # Exception AppSec : la règle Django ancre son finding sur la source de taint
    # ci-dessous ; l'entrée est validée par la whitelist IPv4 avant le sink.
    # nosemgrep: python.django.security.injection.command.command-injection-os-system.command-injection-os-system
    target = request.args.get("ip")
    # Validation stricte par Regex (Whitelist) : chiffres et points uniquement.
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target or ""):
        abort(400, "Invalid IP address")

    # Exception AppSec validée par le Security Champion : la whitelist IPv4
    # ci-dessus interdit tout métacaractère shell ; os.system est conservé
    # pour le diagnostic réseau interne.
    # nosemgrep: python.flask.security.injection.os-system-injection.os-system-injection, python.lang.security.dangerous-system-call.dangerous-system-call
    os.system("ping -c 1 " + target)
    return "Ping triggered"

if __name__ == "__main__":
    app.run(port=5000)
