from flask import Flask, render_template, request, redirect, make_response, send_file, url_for
from db import DB
from flask_bootstrap import Bootstrap
import csv
import os
from importcsv import ImportCSV

app = Flask(__name__)
Bootstrap(app)

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


@app.before_request
def load_config():
    app.config.from_object('config')
    return


@app.route('/')
def route_main():
    data = DB()
    systems = data.load_systems()
    context = {
        "systems": systems,
        "title": "Systems"
    }
    return render_template('systems.html', context=context)


@app.route('/edit/<sys_id>', methods=['GET'])
def route_edit_system_get(sys_id):
    data = DB()
    system = data.load_one_system(sys_id)
    context = {
        "system": system,
        "title": "Edit System "
    }
    return render_template('edit.html', context=context)


@app.route('/save', methods=['POST'])
def route_save_system_post():
    sys_id = request.form['sys_id']
    sys_name = request.form['sys_name']
    sys_ip = request.form['sys_ip']
    sys_url = request.form['sys_url']
    sys_type = request.form['sys_type']
    sys_location = request.form['sys_location']
    sys_note = request.form['sys_note']

    data = DB()
    data.save_one_system(sys_id, sys_name, sys_ip, sys_url, sys_type, sys_location, sys_note)
    url = '/edit/{}'.format(sys_id)
    return redirect(url)


@app.route('/add')
def route_add_system():
    data = DB()
    sys_id = data.add_system()
    url = '/edit/{}'.format(sys_id)
    return redirect(url)


@app.route('/maintenance')
def route_maintenance():
    context = {
        "title": "Maintenance"
    }
    return render_template('maintenance.html', context=context)


# def quote_str(s) -> str:
#     if s is None:
#         return '""'
#     else:
#         return '"' + s + '"'


@app.route('/export')
def route_export():
    data = DB()
    all_data = data.load_systems()

    with open('/temp/systems.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['name', 'ip', 'url', 'systype', 'location', 'note'])
        for row in all_data:
            csv_writer.writerow([row['name'], row['ip'], row['url'], row['systype'], row['location'], row['note']])

    return send_file('/temp/systems.csv')


@app.route('/upload')
def route_upload():
    # ref: https://medevel.com/flask-tutorial-upload-csv-file-and-insert-rows-into-the-database/
    context = {
        "title": "Maintenance"
    }
    return render_template('uploadcsv.html', context=context)


@app.route('/upload-post', methods=['POST'])
def route_upload_post():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
    # save the file
    imp = ImportCSV()
    data = imp.parseCSV(file_path)
    db = DB()
    db.load_from_array(data)

    return redirect('/')


@app.route('/delete/<sys_id>', methods=['GET'])
def route_delete_system_get(sys_id):
    data = DB()
    system = data.load_one_system(sys_id)
    context = {
        "system": system,
        "title": "Edit System "
    }
    return render_template('delete-confirm.html', context=context)


@app.route('/delete-confirmed', methods=['POST'])
def route_delete_confirmed_post():
    sys_id = request.form['sys_id']
    data = DB()
    data.delete_one_system(sys_id)
    return redirect('/')


if __name__ == '__main__':
    app.run()
