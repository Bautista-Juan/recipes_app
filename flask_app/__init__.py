from flask import Flask, session

app = Flask(__name__)
app.secret_key = "recipes_secret_key"