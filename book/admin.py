from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import messages

from book.models import subscriber,books,receipt,comments

class SubscriberAdmin(admin.ModelAdmin):
    list_display = [ 'user','is_subscribed','reg_no','is_complete']
    ordering = ['reg_no']
    def has_subscribed(self, request, queryset):
        for q in queryset:
            if q.is_complete == True:
                q.is_subscribed = True
                q.save()
        messages.info(request , "Reminder : Only Complete profile can be subscribed")
    has_subscribed.short_description = "Mark selected users as subscribed"
    actions = [has_subscribed]
    



class subscriberInline(admin.StackedInline):
    model = subscriber
    can_delete = False
    verbose_name_plural = 'subscriber'

  

   


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (subscriberInline,)
    def has_subscribed(self, request, queryset):
        for q in queryset:
            if q.is_complete == True:
                q.is_subscribed = True
                q.save()
        messages.info(request , "Reminder : Only Complete profile can be subscribed")
    has_subscribed.short_description = "Mark selected users as subscribed"
    actions = [has_subscribed]

class BookAdmin(admin.ModelAdmin):
    list_display = ['name','bookid','is_available']
    ordering = ['name']
    search_fields = ('name', )
    list_filter = ['is_available']
    def make_available(self, request, queryset):
        queryset.update(is_available=True)
    make_available.short_description = "Mark selected books as available"
    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)
    make_unavailable.short_description = "Mark selected books as unavailable"
    actions = [make_unavailable,make_available]


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['subscriber','book','status']
    ordering = ['subscriber']
    search_fields = ['subscriber','book']
    list_filter = ['status']
    def book_returned(self, request, queryset):
        print_list = []
        for q in queryset:
            if q.status == 'I':
                q.status = 'R'
                q.book.is_available=True
                q.book.save()
                q.save()
                print_list.append(q)
        if(len(print_list)>0):
            messages.info(request, "The following books were returned" + str(print_list))
        else:
            messages.info(request, "No books matched the criteria. Please select only issued books")
    book_returned.short_description = "Mark selected issues as returned "

    def book_issued(self,request,queryset):
        print_list = []
        for q in queryset:
            if q.status == 'PB':
                q.status = 'I'
                q.save()
                print_list.append(q)
        if(len(print_list)>0):
           messages.info(request, "The following books were issued : " + str(print_list))
        else:
            messages.info(request, "No books matched the criteria. Please select only Pre-Booked books")
    book_issued.short_description = "Mark selected pre-bookings as issued "

    def cancel_issue(self,request,queryset):
        print_list = []
        for q in queryset:
            if q.status == 'PB':
                q.book.is_available = True
                q.book.save()
                print_list.append(q)
                q.delete()
        if(len(print_list)>0):
            messages.info(request, "The following pre-bookings were cancelled : " + str(print_list))
        else:
            messages.info(request, "No books matched the criteria. Please select only Pre-Booked books")
    cancel_issue.short_description = "Mark selected pre-bookings as cancelled and delete transactions"






    actions = [book_returned,book_issued,cancel_issue]
    

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subscriber','book','comment']
    ordering = ['subscriber']
    search_fields = ['subscriber','book']
    



# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(subscriber, SubscriberAdmin)
admin.site.register(books,BookAdmin)
admin.site.register(receipt,ReceiptAdmin)
admin.site.register(comments,CommentAdmin)