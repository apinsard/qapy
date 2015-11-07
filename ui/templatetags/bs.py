# -*- coding: utf-8 -*-
from django.forms.utils import flatatt
from django.template import Library
from django.utils.html import format_html
from django.utils.safestring import mark_safe


register = Library()


class BsField(object):
    """Handle the bootstrap-like rendering of a form field.
    This class is only intended to be wrapped through `bs_field()`.
    """

    def __init__(self, field, **kwargs):
        """See `bs_field()` simple_tag."""
        self.html = ''
        self.field = field
        self.form_group = kwargs.get('form_group', True)
        self.label = kwargs.get('label', True)

        if self.label is True:
            self.label = field.label
            if field.field.label_suffix:
                self.label += field.field.label_suffix

        self.build_widget()
        if self.field.errors:
            self.build_errors()
        if self.help_text:
            self.build_help_text()
        if self.label:
            self.build_label()
        if self.form_group:
            self.build_form_group()

    def build_widget(self):
        """Build the field widget itself."""
        self.html += self.field.as_widget(attrs=self.widget_attrs)

    def build_errors(self):
        """Build error messages."""
        error_messages = []
        for error in self.field.errors:
            error_messages.append('<li>{}</li>'.format(error))
        self.html += '<ul class="error-block">{}</ul>'.format(
            ''.join(error_messages))

    def build_help_text(self):
        """Build the help text."""
        help_text_attrs = {'class': 'text-muted', 'id': self.help_text_id}
        self.html += format_html('<div{}>{}</div>', flatatt(help_text_attrs),
                                 mark_safe(self.help_text))

    def build_label(self):
        """Build the label."""
        if self.widget_name == 'CheckboxInput':
            self.html = format_html('<label>{}&nbsp;{}</label>',
                                    mark_safe(self.html), self.label)
            self.html = '<div class="checkbox">{}</div>'.format(self.html)
        else:
            label_classes = ['control-label']
            if self.field.field.required:
                label_classes.append('required')
            label_attrs = {}
            label_attrs['class'] = ' '.join(label_classes)
            label_attrs['for'] = self.field.id_for_label
            label_attrs = flatatt(label_attrs) if label_attrs else ''
            label_html = format_html('<label{}>{}</label>', label_attrs,
                                     self.label)
            self.html = label_html + self.html

    def build_form_group(self):
        """Build the form-group."""
        group_classes = ['form-group']
        if self.field.errors:
            group_classes.append('has-error')
        group_attrs = {'class': ' '.join(group_classes)}
        group_attrs = flatatt(group_attrs)
        self.html = format_html('<div{}>{}</div>', group_attrs,
                                mark_safe(self.html))

    @property
    def widget_name(self):
        """Return the widget name."""
        return self.field.field.widget.__class__.__name__

    @property
    def widget_classes(self):
        """Return the widget classes according to the widget name and whether
        there are errors or not.
        """
        classes = []
        if self.widget_name != 'CheckboxInput':
            classes.append('form-control')
            if self.field.errors:
                classes.append('form-control-error')
        return classes

    @property
    def widget_attrs(self):
        """Return the widget extra attributes."""
        attrs = {}
        classes = self.widget_classes
        if classes:
            attrs['class'] = ' '.join(classes)
        if self.field.field.required:
            attrs['required'] = 'required'
        if self.help_text:
            attrs['aria-describedby'] = self.help_text_id
        return attrs

    @property
    def help_text(self):
        """Return the help text."""
        return self.field.field.help_text

    @property
    def help_text_id(self):
        """Return the ID of the help text."""
        return self.field.id_for_label + '_help_text'


@register.simple_tag
def bs_field(field, **kwargs):
    """Render a bootstrap-like form field.
    - `field`: the `django.forms.Field` to be rendered
    - `kwargs`:
      - `form_group`: whether the field and label should be within a
        form-group. (default: True)
      - `label`: the label to display as a string, or True to display the
        default label, or False skip label rendering. (default: True)
    """
    return mark_safe(BsField(field, **kwargs).html)
