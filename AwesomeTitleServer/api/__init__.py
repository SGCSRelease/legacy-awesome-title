from flask import Blueprint


bp = Blueprint('api', __name__)


from AwesomeTitleServer.api import user 
