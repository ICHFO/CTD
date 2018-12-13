from flask import render_template, redirect, url_for, request, session, flash
from app import app, get_db, db_handler, VALID_KEYS_VALS
from app.models import Resource
from jsonpickle import decode
import app.ctdcore.loading_RESM as lresm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route("/resource")
def resource():
    return render_template("resource.html")


@app.route('/add_resource', methods=['GET', 'POST'])
def add_resource():
    if request.method == 'POST':
        # save file
        if 'resfile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['resfile']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        file.save(file.filename)
        # parse file and get resource
        output = lresm.add_from_pdf('DEV',file.filename)
        resource_id = output[0]['res_id']
        resource = Resource(resource_id)
        # update session['resource_ids']
        session['resource'] = resource.serialize()
        session['resource_ids'] = db_handler.get_resource_ids()
        return render_template('modify_resource.html'
                               , resource=resource
                               , resource_ids=session['resource_ids']
                               , choices=VALID_KEYS_VALS)
    return render_template('add_resource.html')


@app.route('/modify_resource', methods=['GET', 'POST'])
def modify_resource():
    if 'resource_ids' not in session:
        session['resource_ids'] = db_handler.get_resource_ids()
    # POST
    if request.method == 'POST':
        # Load Resource
        if request.form.get('res_sel'):
            session['resource'] = Resource(request.form['res_sel']).serialize()
        # Modify keys
        else:
            resource = decode(session['resource'])
            mod_keys = list()
            for key in resource.keys:
                mod_key = dict(KEY_ID=key['KEY_ID'], KEY_NAAM=key['KEY_NAAM']
                               , KEY_GELDIG=int(request.form[key['KEY_NAAM']]))
                mod_keys.append(mod_key)
            resource.update_keys(mod_keys)
            session['resource'] = resource.serialize()
    # GET
    else:
        if 'resource' not in session:
            session['resource'] = Resource(session['resource_ids'][0]).serialize()
    return render_template('modify_resource.html'
                           , resource=decode(session['resource'])
                           , resource_ids=session['resource_ids']
                           , choices=VALID_KEYS_VALS)


@app.route('/resource_map', methods=['GET', 'POST'])
def resource_map():
    if 'resource_ids' not in session:
        session['resource_ids'] = db_handler.get_resource_ids()
    if request.method == 'POST':
        session['resource'] = Resource(request.form['res_sel']).serialize()
    else:
        if 'resource' not in session:
            session['resource'] = Resource(session['resource_ids'][0]).serialize()
    return render_template('resource_map.html', resource_ids=session['resource_ids'],
                           resource=decode(session['resource']))


@app.route('/best_vacancies', methods=['POST'])
def best_vacancies():
    resource = decode(session['resource'])
    vacancies = db_handler.get_five_best(resource.id)
    resource_ids = db_handler.get_resource_ids()
    return render_template('resource_map.html', resource_ids=resource_ids,
                           resource=decode(session['resource']),
                           vacancies=vacancies)


@app.route('/sixty_percent', methods=['GET', 'POST'])
def sixty_percent():
    if request.method == 'POST':
        resource_ids = db_handler.get_resource_ids()
    return render_template('resource_map.html', resource_ids=resource_ids,
                           resource=session['resource'])
#test

@app.route('/nog_iets', methods=['GET', 'POST'])
def nog_iets():
    if request.method == 'POST':
        resource_ids = db_handler.get_resource_ids()
    return render_template('resource_map.html', resource_ids=resource_ids,
                           resource=session['resource'])
