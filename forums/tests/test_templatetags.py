from django.test import TestCase
from django import forms

from pages.templatetags.form_tags import field_type, input_class

# Create your tests here.
class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        fields = ('name', 'password')
        
class FieldTypeTests(TestCase):
    ''' A test case to verify field widget types '''
    def test_field_widget_type(self):
        form = ExampleForm()
        self.assertEquals('TextInput', field_type(form['name']))
        self.assertEquals('PasswordInput', field_type(form['password']))
        
class InputClassTests(TestCase):
    def test_unbound_field_initial_state(self):
        form = ExampleForm()  # unbound form
        self.assertEquals('form-control ', input_class(form['name']))
        
    ''' A test case to verify bound fields are valid '''
    def test_valid_bound_field(self):
        form = ExampleForm({'name': 'jack', 'password': '123'})  # bound form (field + data)
        self.assertEquals('form-control is-valid', input_class(form['name']))
        self.assertEquals('form-control ', input_class(form['password']))
        
    ''' A test case to verify invalid bound fields '''
    def test_invalid_bound_field(self):
        form = ExampleForm({'name': '', 'password': '123'})  # bound form (field + data)
        self.assertEquals('form-control is-invalid', input_class(form['name']))