"""Admin models for catalog."""

from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)


class BooksInline(admin.TabularInline):
    """To add Inline editing of associated records."""

    model = Book
    extra = 0
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        """Return the ability to edit the record inline ."""
        return False


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    """To change how a model is displayed in the admin interface."""

    list_display = (
        'last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    # Add Inline editing of associated records
    inlines = [BooksInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    """To add Inline editing of associated records."""

    model = BookInstance
    extra = 0
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        """Return the ability to edit the record inline ."""
        return False


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """To change how a model is displayed in the admin interface."""

    list_display = ('title', 'author', 'display_genre')

    # Add Inline editing of associated records
    inlines = [BooksInstanceInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """To change how a model is displayed in the admin interface."""

    list_display = ('id', 'book', 'borrower', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {'fields': ('book', 'imprint', 'id')}),
        ('Availability', {'fields': ('status', 'due_back', 'borrower')}),
    )
