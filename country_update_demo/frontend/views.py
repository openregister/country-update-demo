from flask import (
    current_app,
    Blueprint,
    render_template,
    request,
    redirect,
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
    country = request.form['country'].upper()
    citizen_names = request.form['citizen_names']
    end_date = request.form['end_date']
    name = request.form['name']
    official_name = request.form['official_name']
    start_date = request.form['start_date']
    text = request.form['text']

    return create_record_in_register(
        render_template(
            'create-record.html',
            country=country,
            citizen_names=citizen_names,
            end_date=end_date,
            name=name,
            official_name=official_name,
            start_date=start_date,
            text=text
        ),
        country,
        citizen_names,
        end_date,
        name,
        official_name,
        start_date,
        text
    )


@frontend.route('/update-record/<record_id>')
def render_update_record_form(record_id):
    resp = requests.get(current_app.config['READ_API_URL'] + "/country/" + record_id + ".json")

    record_json = json.loads(resp.content)['entry']

    return render_template(
        'update-record.html',
        country=record_json['country'],
        citizen_names=record_json.get('citizen-names', ''),
        end_date=record_json.get('end-date', ''),
        name=record_json.get('name', ''),
        official_name=record_json.get('official-name', ''),
        start_date=record_json.get('start-date', ''),
        text=record_json.get('text', '')
    )


@frontend.route('/update-record/<record_id>', methods=['POST'])
def update_record(record_id):
    return create_record_in_register(
        redirect("/update-record/" + record_id),
        record_id,
        request.form['citizen_names'],
        request.form['end_date'],
        request.form['name'],
        request.form['official_name'],
        request.form['start_date'],
        request.form['text']
    )


def create_record_in_register(error_response, country, citizen_names, end_date, name, official_name, start_date, text):
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

    resp = requests.post(current_app.config['MINT_SERVICE_URL'] + "/load", json_line)

    if (resp.status_code == 200):
        return render_template('success.html')

    return error_response
