from __future__ import absolute_import, unicode_literals
from celery import shared_task


from cmdb.models import InventoryPool
from .utils.handle_command import HandleCommand
from .utils.ansible_api import  ResultCallback,MyAnsiable2



@shared_task
def task_ansible(command):
    inventorys = InventoryPool.objects.all()
    handler = HandleCommand(command, inventorys)
    ret = handler.exec_command()
    return ret
    
@shared_task
def add(n):
    import time 
    time.sleep(10)
    print(n)
    return n+10


@shared_task
def ansible_run(inventory,remote_user,connection,hosts,args,module):
    print(inventory,remote_user,connection,hosts,args,module)
    ansible2 = MyAnsiable2(
        inventory=inventory,
        remote_user=remote_user,
        connection=connection,
    )
    # 执行自定义任务，执行对象是 nginx 组
    ansible2.run(hosts=hosts, module=module, args=args)
    # 打印结果
    ret=ansible2.get_result()
    return ret



