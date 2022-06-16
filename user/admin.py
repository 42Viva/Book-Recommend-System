from django.contrib import admin

from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "password", "name", "address", "email")
    search_fields = ("username", "name", "address", "phone", "email")

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "sump", "good")
    search_fields = ("title", "author", "good")
    list_filter = ("author", "good")


class CommenAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "good", "create_time")
    search_fields = ("user", "book", "good")
    list_filter = ("user", "book")


class LiuyanAdmin(admin.ModelAdmin):
    list_display = ("user", "create_time")
    search_fields = ("user",)
    list_filter = ("user",)

class NumAdmin(admin.ModelAdmin):
    list_display = ("users", "books", "comments", "actions", "message_boards")

    def get_queryset(self, request):
        users = User.objects.all().count()
        books = Book.objects.all().count()
        comments = Comment.objects.all().count()
        message_boards = MessageBoard.objects.all().count()
        if Num.objects.all().count() == 0:
            Num.objects.create(users=users, books=books, comments=comments,
                               message_boards=message_boards, )
        else:
            for num in Num.objects.all():
                num.users = users
                num.books = books
                num.comments = comments
                num.message_boards = message_boards
                num.save()
        return super().get_queryset(request)

admin.site.register(Tags)
admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Comment, CommenAdmin)
admin.site.register(MessageBoard, LiuyanAdmin)
admin.site.register(Num, NumAdmin)

