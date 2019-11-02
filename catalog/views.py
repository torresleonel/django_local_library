"""View's functions for catalog."""

import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.forms import RenewBookForm
from catalog.models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_genres = Genre.objects.count()
    num_book_title_word = Book.objects.filter(title__icontains='de').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_book_title_word': num_book_title_word,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class AuthorListView(generic.ListView):
    """Inherit class-based ListView."""

    model = Author
    paginate_by = 1
    # Model have METADATA for records order, not need this.
    # queryset = Author.objects.order_by('last_name')


class AuthorDetailView(generic.DetailView):
    """Inherit class-based DetailView."""

    model = Author


class AuthorCreate(PermissionRequiredMixin, CreateView):
    """Generic editing views for creating views based on models Author."""

    model = Author
    fields = '__all__'
    # This is for sample
    initial = {'first_name': 'Author'}
    permission_required = 'catalog.can_manage'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    """Generic editing views for editing views based on models Author."""

    model = Author
    # For get all fields to use '__all__'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_manage'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    """Generic editing views for deleting views based on models Author."""

    model = Author
    permission_required = 'catalog.can_manage'
    success_url = reverse_lazy('authors')


class BookListView(generic.ListView):
    """Inherit class-based ListView."""

    model = Book
    paginate_by = 2
    queryset = Book.objects.order_by('title')


class BookDetailView(generic.DetailView):
    """Inherit class-based DetailView."""

    model = Book


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        """Return Book Instance on loan to current user."""
        return BookInstance.objects.filter(
            borrower=self.request.user).filter(status__exact='o').order_by(
            'due_back')


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan."""

    model = BookInstance
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_all_borrowed.html'

    def get_queryset(self):
        """Return Book Instance on loan status."""
        return BookInstance.objects.filter(
            status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request
        # (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + \
            datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class BookCreate(PermissionRequiredMixin, CreateView):
    """Generic editing views for creating views based on models Book."""

    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_manage'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    """Generic editing views for editing views based on models Book."""

    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_manage'


class BookDelete(PermissionRequiredMixin, DeleteView):
    """Generic editing views for deleting views based on models Book."""

    model = Book
    permission_required = 'catalog.can_manage'
    success_url = reverse_lazy('books')
