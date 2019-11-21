from django.contrib import admin

# Register your models here.
from cmdb.models import (Asset,IDC,Cabinet,SysUsers,
                                     Server,Memory,Disk)

class AssetAdmin(admin.ModelAdmin):  
    pass

class IDCAdmin(admin.ModelAdmin):  
    pass

class CabinetAdmin(admin.ModelAdmin):  
    pass

class SysUsersAdmin(admin.ModelAdmin):  
    pass

class ServerAdmin(admin.ModelAdmin):  
    pass

class MemoryAdmin(admin.ModelAdmin):  
    pass

class DiskAdmin(admin.ModelAdmin):  
    pass
# 注册
from . import models
admin.site.register(Asset, AssetAdmin)
admin.site.register(IDC, IDCAdmin)
admin.site.register(Cabinet, CabinetAdmin)
admin.site.register(SysUsers, SysUsersAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Memory, MemoryAdmin)
admin.site.register(Disk, DiskAdmin)
admin.site.register(models.TreeNode)
admin.site.register(models.Tag)
admin.site.register(models.Connection)
admin.site.register(models.InventoryPool)
admin.site.register(models.Variable2Server)
admin.site.register(models.Variable2Group)

