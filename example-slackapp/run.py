
from app import create_app

# disable SSL warnings, and such ... this is only done here in the "app/run" so we don't hardcode
# this disable anywhere in the package files.

from urllib3 import disable_warnings
disable_warnings()

app = create_app()

if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"])

