from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from flask.ext.pagedown import PageDown
from wtforms.fields import SubmitField
from flask import render_template
from my_app import app

class PageDownFormExample(Form):
    pagedown = PageDownField('Enter your markdown')
    submit = SubmitField('submit')

@app.route('/', methods=['GET'])
def home():
    form = PageDownFormExample()
    text = None
    if form.validate_on_submit():
        text = form.pagedown.data
    return render_template(
            'show_entries.html',
            form = form,
            text = text)


