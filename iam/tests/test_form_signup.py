from django.test import TestCase

from ..forms import SignUpForm

# Create your tests here.
class SignUpFormTest(TestCase):
    ''' A test case to confirm form has appropriate fields '''
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)