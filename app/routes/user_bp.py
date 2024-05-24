from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.user import db, User

user_bp = Blueprint('user_bp', __name__)
