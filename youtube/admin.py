from django.contrib import admin
from.models import DownloadTask,fileCreation,processdownload
class DownloadTaskAdmin(admin.ModelAdmin):
    list_display= ('name','link','image','user')
    list_filter=('user','fileVideo')
    search_fields=('name','fileVideo_name')


class fileCreationAdmin(admin.ModelAdmin):
    list_display=('name','link','image','title','errormessage','file_path')
    search_fields=('name')



class processdownload(admin.ModelAdmin):
    list_display=('created','updated','session_key')
    search_fields=('session_key')
