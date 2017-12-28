import os

from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from forms import UploadForm, ColumnLabelForm

from attribute_table import build_attributes, build_key_string
from load_csv import load_csv_main
from database_calls import create_database, load_data_into_table


app = Flask(__name__)

with open('app.secrets', 'r') as f:
    secret_key = f.read().strip()

app.config['SECRET_KEY'] = secret_key

manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
        else:
            raw_data = form.csv_file.data
            filename = secure_filename(raw_data.filename)
            raw_data.save(os.path.join(
                app.instance_path, 'csv_files', filename
            ))
            
            session['csv_filename'] = filename
            
            return redirect(url_for('column_names'))
            
    return render_template('index.html', form=form)


@app.route('/column_names', methods=['GET', 'POST'])
def column_names():
    form = ColumnLabelForm()
    data = session['csv_filename']
    return render_template('column_names.html', form=form, data=data)


if __name__ == "__main__":
    manager.run()
