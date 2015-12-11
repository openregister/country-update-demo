from flask import (
    current_app,
    Blueprint,
    render_template,
    request,
    redirect,
    json,
    jsonify,
    Flask
)

from flask.ext.basicauth import BasicAuth

import requests

app = Flask(__name__)

basic_auth = BasicAuth(app)

frontend = Blueprint('frontend', __name__, template_folder='templates')


headers = {'Content-type': 'application/json'}

##TODO: reformat this method
@frontend.route('/countries.json')
def countries():
    url = "%s/records.json?page-size=200" % current_app.config['READ_API_URL']
    resp = requests.get(url, headers=headers)
    countries = []
    current_countries_code = []
    for e in resp.json():
        if e['entry']['country'] not in current_countries_code :
            current_countries_code.append(e['entry']['country'])
            countries.append(e['entry'])
    sorted_countries = sorted(countries, key=lambda country: country['name'])
    return jsonify({'entries': sorted_countries})


@frontend.route('/country/<country_code>')
def country_record_in_register(country_code):
    url = "%s/country/%s" % (current_app.config['READ_API_URL'], country_code)
    return redirect(url)


@frontend.route('/')
@basic_auth.required
def index_page():
    return render_template('index.html')

@frontend.route('/', methods=['POST'])
@basic_auth.required
def index_form_selection_submit():

    form_action = request.form.get('radio-record-group')

    if form_action == 'Update' :
        ##TODO: check that a country is selected
        return redirect('/update-record/' + request.form.get('country'))

    return redirect('/create-record')


@frontend.route('/create-record')
@basic_auth.required
def render_create_record_form():
    return render_template('create-record.html')


@frontend.route('/create-record', methods=['POST'])
@basic_auth.required
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
        'create-record-success.html',
        country,
        citizen_names,
        end_date,
        name,
        official_name,
        start_date,
        text
    )


@frontend.route('/update-record/<record_id>')
@basic_auth.required
def render_update_record_form(record_id):
    url = "%s/country/%s.json" % (current_app.config['READ_API_URL'], record_id)
    resp = requests.get(url)

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
@basic_auth.required
def update_record(record_id):
    return create_record_in_register(
        redirect("/update-record/" + record_id),
        'update-record-success.html',
        record_id,
        request.form['citizen_names'],
        request.form['end_date'],
        request.form['name'],
        request.form['official_name'],
        request.form['start_date'],
        request.form['text']
    )


def create_record_in_register(error_response, success_page, country, citizen_names, end_date, name, official_name, start_date, text):
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

    loadUrl = "%s/load" % current_app.config['MINT_SERVICE_URL']
    resp = requests.post(loadUrl, auth=('openregister', current_app.config['MINT_API_PASSWORD']), data=json_line)

    if (resp.status_code == 200):
        return render_template(success_page, country = country)

    return error_response
