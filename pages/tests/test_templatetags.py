from django.test import TestCase
from django import forms

from ..templatetags.form_tags import field_type, input_class

# Create your tests here.
''' Use this in subsequent test cases '''
class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        fields = ('name', 'password')
        
''' A test case to validate field types '''
class FieldTypeTests(TestCase):
    def test_field_widget_type(self):
        form = ExampleForm()
        self.assertEquals('TextInput', field_type(form['name']))
        self.assertEquals('PasswordInput', field_type(form['password']))
        
        
''' A test case to validate input types '''
class InputClassTests(TestCase):
    ''' Test an unbound form '''
    def test_unbound_field_initial_state(self):
        form = ExampleForm()  # unbound form
        self.assertEquals('form-control ', input_class(form['name']))
        
    ''' Test valid fields on bound form '''
    def test_valid_bound_field(self):
        form = ExampleForm({'name': 'jack', 'password': '123'})  # bound form (field + data)
        self.assertEquals('form-control is-valid', input_class(form['name']))
        self.assertEquals('form-control ', input_class(form['password']))
        
    ''' Test invalid fields on bound form '''
    def test_invalid_bound_field(self):
        form = ExampleForm({'name': '', 'password': '123'})  # bound form (field + data)
        self.assertEquals('form-control is-invalid', input_class(form['name']))
