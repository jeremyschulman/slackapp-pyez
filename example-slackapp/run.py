
#  Copyright 2019 Jeremy Schulman, nwkautomaniac@gmail.com
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from app import create_app

# disable SSL warnings, and such ... this is only done here in the "app/run" so we don't hardcode
# this disable anywhere in the package files.

from urllib3 import disable_warnings
disable_warnings()

app = create_app()

if __name__ == "__main__":
    app.run(host=app.config["HOST"],
            port=app.config["PORT"],
            threaded=app.config["THREADING"])

