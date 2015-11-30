import os
from update_country_demo.factory import create_app
app = create_app(os.environ['SETTINGS'])
