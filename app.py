import os
import uuid
from flask import Flask, flash, request, redirect, send_from_directory

app = Flask(__name__)


@app.route('/')
def root():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run()