"""Unit test for catalog forms."""

import datetime

from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewBookForm


class RenewBookFormTest(TestCase):
    """Test renew book form."""

    def test_renew_form_date_field_label(self):
        """Test date field label of renew book form."""
        form = RenewBookForm()
        self.assertTrue(
            form.fields['renewal_date'].label is None or
            form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        """Test date field help text of renew book form."""
        form = RenewBookForm()
        self.assertEqual(
            form.fields['renewal_date'].help_text,
            'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        """Test range in past for date field of renew book form."""
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        """Test range too far in future for date field of renew book form."""
        date = datetime.date.today() + datetime.timedelta(weeks=4) + \
            datetime.timedelta(days=1)

        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        """Test range today for date field of renew book form."""
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        """Test range max for date field of renew book form."""
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
