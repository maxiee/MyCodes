from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from flask.ext.pagedown import PageDown
from wtforms.fields import SubmitField
from flask import render_template
from my_app import app
from my_app.utils import contentManager

class PageDownFormExample(Form):
    pagedown = PageDownField('Enter your markdown')
    submit = SubmitField('submit')

@app.route('/<url>', methods=['GET'])
def home(url):
    form = PageDownFormExample()
    text = None
    if form.validate_on_submit():
        text = form.pagedown.data
    post = contentManager.getPost(url)
    return render_template(
        'show_entries.html',
        form = form,
        text = text,
        post = post,
        content = contentManager.getContent(url)
    )
