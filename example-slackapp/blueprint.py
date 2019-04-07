from flask import Blueprint


blueprint = Blueprint(__package__, __name__,
                      url_prefix="/api/v1",
                      static_folder='static')




