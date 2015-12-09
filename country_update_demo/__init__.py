import os
from country_update_demo.factory import create_app
app = create_app(os.environ['SETTINGS'])
