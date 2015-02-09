from wtforms import TextAreaField
from wtforms.widgets import TextArea

class MarkdownTextarea(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'markdown')
        return super(MarkdownTextarea, self).__call__(field, **kwargs)

class MarkdownField(TextAreaField):
    widget = MarkdownTextarea()