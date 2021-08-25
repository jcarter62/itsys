from flask import Flask, render_template, request, redirect
from db import DB
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


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

    data = DB()
    data.save_one_system(sys_id, sys_name, sys_ip, sys_url)
    url = '/edit/{}'.format(sys_id)
    return redirect(url)


@app.route('/add')
def route_add_system():
    data = DB()
    sys_id = data.add_system()
    url = '/edit/{}'.format(sys_id)
    return redirect(url)


if __name__ == '__main__':
    app.run()
