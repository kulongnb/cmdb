from django.shortcuts import render

# Create your views here.
from django.views.generic import View, ListView
from django.http import JsonResponse, HttpResponse
from cmdb.models import Server, Connection, InventoryPool
import subprocess
import os
import pexpect
from .utils.handle_command import HandleCommand, no_secret


class ConnectionView(ListView):
    queryset = Server.objects.filter(connection__user__isnull=False)
    # model=Server
    context_object_name = "server"
    template_name = "octopus/connection.html"

    def post(self, request):
        rerver_id = request.POST.get("server_id")
        server = Server.objects.filter(id=rerver_id).first()
        ip = server.manager_id
        user = server.connection.user
        pwd = server.connection.password
        port = server.connection.port
        shell_comm = "ssh-copy-id  -p {port} {user}@{ip}".format(
            port=port, user=user, ip=ip
        )
        no_secret = no_secret(shell_comm, pwd)
        if no_secret:
            server.connection.authed = True
            server.connection.save()
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False})


class EexcCommand(ListView):
    model = InventoryPool
    template_name = "octopus/run.html"
    context_object_name = "inventorypools"

    def post(self, request):
        command = request.POST.get("command")  # 获取提交命令(标签name)
        from .tasks import task_ansible

        task = task_ansible.delay(command)
        print(task)  # 必须调用delay方法,异步执行
        # print(task.task_id)
        return JsonResponse({"task_id": task.id})
        # return JsonResponse({"task_id": task})


class asyncDemoView(ListView):
    model = InventoryPool
    template_name = "octopus/async_demo.html"
    context_object_name = "async"

    def post(self, request):
        num = request.POST.get("num")
        from .tasks import add

        task = add.delay(int(num))
        return JsonResponse({"task_id": task.id})


from celery.result import AsyncResult


class get_task(View):
    def get(self, request):
        task_id = request.GET.get("task_id")
        task_obj = AsyncResult(id=task_id)
        task_json = {
            "id": task_obj.task_id,
            "status": task_obj.status,
            "success": task_obj.successful(),
            "result": task_obj.result,
        }
        print(task_json)
        return JsonResponse(task_json)


from .tasks import ansible_run


class ansible_api(ListView):
    model = InventoryPool
    context_object_name = "InventoryPool"
    template_name = "octopus/run.html"

    def post(self, request):
        inventory = request.POST.get("inv_path")
        remote_user = request.POST.get("remote_user")
        connection = request.POST.get("connection")
        hosts = request.POST.get("hosts")
        module = request.POST.get("module")
        args = request.POST.get("args")
        print(inventory, remote_user, connection, hosts, module, args)
        task = ansible_run.delay(
            inventory=inventory,
            remote_user=remote_user,
            connection=connection,
            hosts=hosts,
            args=args,
            module=module,
        )
        # print(task.id)
        return JsonResponse({"task_id": task.id})


# from multiprocessing import process

# return JsonResponse(ansible_data)


#         task_id = request.GET.get("task_id")

#         task_obj = AsyncResult(id=task_id)  # 得到task对象
#         print(task_obj)
#         #  获取数据，返回yemian
#         task_json = {
#             "id": task_obj.id,
#             "status": task_obj.status,
#             "success": task_obj.successful(),
#             "result": task_obj.result,
#         }
#         return JsonResponse(task_json)


# class EexcCommand(View):
# def get(self, request):
#     Inventory = InventoryPool.objects.all()
#     return render(request, "octopus/run.html", { "Inventory": Inventory })


# class ConnectionView(View):
#     def get(self, request):
#         conninfo = Server.objects.all()
#         return render(request, "octopus/connection.html", {"connection": conninfo})

