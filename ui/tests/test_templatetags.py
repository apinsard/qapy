# -*- coding: utf-8 -*-
from django import forms
from django.test import TestCase

from ..templatetags.bs import bs_field


class TestForm(forms.Form):
    boolean_field = forms.BooleanField(label="Boolean Field", required=False)
    char_field = forms.CharField(label="Char Field", max_length=10)
    choice_field = forms.ChoiceField(choices=[
        ('c1', "Choice 1"),
        ('c2', "Choice 2"),
        ('c3', "Choice 3"),
    ])
    date_field = forms.DateField(label="Date Field", label_suffix=" =")
    datetime_field = forms.DateTimeField(label_suffix=" =")
    decimal_field = forms.DecimalField(max_digits=6, decimal_places=2)
    duration_field = forms.DurationField()
    email_field = forms.EmailField(initial="toto@cocoonr.fr")
    file_field = forms.FileField()
    image_field = forms.ImageField()
    integer_field = forms.IntegerField(help_text="An integer")
    multiplechoice_field = forms.MultipleChoiceField(choices=[
        ('c1', "Choice 1"),
        ('c2', "Choice 2"),
        ('c3', "Choice 3"),
    ])
    nullboolean_field = forms.NullBooleanField()
    url_field = forms.URLField(error_messages={
        'invalid': "Invalid URL",
    })
    splitdatetime_field = forms.SplitDateTimeField(error_messages={
        'invalid_date': "Invalid date",
        'invalid_time': "Invalid time",
    }, label_suffix=" =", help_text="foobar")
    hidden_field = forms.CharField(widget=forms.HiddenInput)
    password_field = forms.CharField(widget=forms.PasswordInput)
    textarea_field = forms.CharField(widget=forms.Textarea, initial="foo bar")


class BsFieldTestCase(TestCase):

    def setUp(self):
        self.maxDiff = 1500
        self.form = TestForm()

    def test_booleanfield(self):
        field = self.form['boolean_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<div class="checkbox">'
            '<label><input id="id_boolean_field" name="boolean_field" '
            'type="checkbox" />&nbsp;Boolean Field</label>'
            '</div></div>'
        ))

    def test_charfield(self):
        field = self.form['char_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<label class="control-label required" for="id_char_field">'
            'Char Field</label><input class="form-control" '
            'id="id_char_field" maxlength="10" name="char_field" '
            'required="required" type="text" />'
            '</div>'
        ))

    def test_choicefield_without_form_group(self):
        field = self.form['choice_field']
        html = bs_field(field, form_group=False)
        self.assertMultiLineEqual(html, (
            '<label class="control-label required" for="id_choice_field">'
            'Choice field</label>'
            '<select class="form-control" id="id_choice_field" '
            'name="choice_field" required="required">\n'
            '<option value="c1">Choice 1</option>\n'
            '<option value="c2">Choice 2</option>\n'
            '<option value="c3">Choice 3</option>\n'
            '</select>'
        ))

    def test_datefield_without_label(self):
        field = self.form['date_field']
        html = bs_field(field, label=False)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<input class="form-control" id="id_date_field" name="date_field" '
            'required="required" type="text" />'
            '</div>'
        ))

    def test_datetimefield(self):
        field = self.form['datetime_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<label class="control-label required" for="id_datetime_field">'
            'Datetime field =</label>'
            '<input class="form-control" id="id_datetime_field" '
            'name="datetime_field" required="required" type="text" />'
            '</div>'
        ))

    def test_decimalfield_without_form_group_and_label(self):
        field = self.form['decimal_field']
        html = bs_field(field, form_group=False, label=False)
        self.assertMultiLineEqual(html, (
            '<input class="form-control" id="id_decimal_field" '
            'name="decimal_field" required="required" step="0.01" '
            'type="number" />'
        ))

    def test_duration_field(self):
        field = self.form['duration_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<label class="control-label required" for="id_duration_field">'
            'Duration field</label>'
            '<input class="form-control" id="id_duration_field" '
            'name="duration_field" required="required" type="text" />'
            '</div>'
        ))

    def test_emailfield_with_custom_label(self):
        field = self.form['email_field']
        html = bs_field(field, label="Your Mail")
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<label class="control-label required" for="id_email_field">'
            'Your Mail</label>'
            '<input class="form-control" id="id_email_field" '
            'name="email_field" required="required" type="email" '
            'value="toto@cocoonr.fr" />'
            '</div>'
        ))

    def test_filefield(self):
        field = self.form['file_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<label class="control-label required" for="id_file_field">'
            'File field</label>'
            '<input class="form-control" id="id_file_field" '
            'name="file_field" required="required" type="file" />'
            '</div>'
        ))

    def test_imagefield(self):
        field = self.form['image_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<label class="control-label required" for="id_image_field">'
            'Image field</label>'
            '<input class="form-control" id="id_image_field" '
            'name="image_field" required="required" type="file" />'
            '</div>'
        ))

    def test_integerfield(self):
        field = self.form['integer_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<label class="control-label required" for="id_integer_field">'
            'Integer field</label>'
            '<input aria-describedby="id_integer_field_help_text" '
            'class="form-control" id="id_integer_field" '
            'name="integer_field" required="required" type="number" />'
            '<div class="text-muted" id="id_integer_field_help_text">'
            'An integer</div>'
            '</div>'
        ))

    def test_multiplechoicefield(self):
        field = self.form['multiplechoice_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<label class="control-label required" '
            'for="id_multiplechoice_field">Multiplechoice field</label>'
            '<select multiple="multiple" class="form-control" '
            'id="id_multiplechoice_field" name="multiplechoice_field" '
            'required="required">\n'
            '<option value="c1">Choice 1</option>\n'
            '<option value="c2">Choice 2</option>\n'
            '<option value="c3">Choice 3</option>\n'
            '</select>'
            '</div>'
        ))

    def test_nullbooleanfield(self):
        field = self.form['nullboolean_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<label class="control-label required" '
            'for="id_nullboolean_field">Nullboolean field</label>'
            '<select class="form-control" id="id_nullboolean_field" '
            'name="nullboolean_field" required="required">\n'
            '<option value="1" selected="selected">Inconnu</option>\n'
            '<option value="2">Oui</option>\n'
            '<option value="3">Non</option>\n'
            '</select>'
            '</div>'
        ))

    def test_urlfield_with_errors(self):
        form = TestForm({'url_field': "toto"})
        field = form['url_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group has-error">'
            '<label class="control-label required" for="id_url_field">'
            'Url field</label>'
            '<input class="form-control form-control-error" id="id_url_field" '
            'name="url_field" required="required" type="url" value="toto" />'
            '<ul class="error-block">'
            '<li>Invalid URL</li>'
            '</ul>'
            '</div>'
        ))

    def test_splitdatetimefield_with_custom_label_and_errors(self):
        form = TestForm({'splitdatetime_field_0': "foo",
                         'splitdatetime_field_1': "bar"})
        field = form['splitdatetime_field']
        html = bs_field(field, label="hello")
        self.assertMultiLineEqual(html, (
            '<div class="form-group has-error">'
            '<label class="control-label required" '
            'for="id_splitdatetime_field_0">hello</label>'
            '<input aria-describedby="id_splitdatetime_field_0_help_text" '
            'class="form-control form-control-error" '
            'id="id_splitdatetime_field_0" name="splitdatetime_field_0" '
            'required="required" type="text" value="foo" />'
            '<input aria-describedby="id_splitdatetime_field_0_help_text" '
            'class="form-control form-control-error" '
            'id="id_splitdatetime_field_1" name="splitdatetime_field_1" '
            'required="required" type="text" value="bar" />'
            '<ul class="error-block">'
            '<li>Invalid date</li>'
            '<li>Invalid time</li>'
            '</ul>'
            '<div class="text-muted" id="id_splitdatetime_field_0_help_text">'
            'foobar</div>'
            '</div>'
        ))

    def test_hiddenfield(self):
        field = self.form['hidden_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<label class="control-label required" for="id_hidden_field">'
            'Hidden field</label><input class="form-control" '
            'id="id_hidden_field" name="hidden_field" '
            'required="required" type="hidden" />'
            '</div>'
        ))

    def test_passwordfield(self):
        field = self.form['password_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<label class="control-label required" for="id_password_field">'
            'Password field</label><input class="form-control" '
            'id="id_password_field" name="password_field" '
            'required="required" type="password" />'
            '</div>'
        ))

    def test_textareafield(self):
        field = self.form['textarea_field']
        html = bs_field(field)
        self.assertMultiLineEqual(html, (
            '<div class="form-group">'
            '<label class="control-label required" for="id_textarea_field">'
            'Textarea field</label><textarea class="form-control" cols="40" '
            'id="id_textarea_field" name="textarea_field" '
            'required="required" rows="10">\r\nfoo bar</textarea>'
            '</div>'
        ))
