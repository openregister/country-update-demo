from flask import (
    current_app,
    Blueprint,
    render_template,
    request,
    json
)
import requests

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/')
def index():
    return render_template('index.html')


@frontend.route('/create-record')
def render_create_record_form():
    return render_template('create-record.html')


@frontend.route('/create-record', methods=['POST'])
def create_record():
    country = request.form['country']
    citizen_names = request.form['citizen_names']
    end_date = request.form['end_date']
    name = request.form['name']
    official_name = request.form['official_name']
    start_date = request.form['start_date']
    text = request.form['text']

    json_line = json.dumps(
        {
            'country': country,
            'citizen-names': citizen_names,
            'end-date': end_date,
            'name': name,
            'official-name': official_name,
            'start-date': start_date,
            'text': text
        }
    )

    resp = requests.post(current_app.config['REGISTER_URL'], json_line)

    if (resp.status_code == 200):
        return render_template('success.html')

    return render_template(
        'create-record.html',
        country=country,
        citizen_names=citizen_names,
        end_date=end_date,
        name=name,
        official_name=official_name,
        start_date=start_date,
        text=text
    )
