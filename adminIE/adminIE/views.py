from django.shortcuts import render

from cmdb.models import Asset
from django.views import View

# [
# {value:, name:'type_qs.'},
# {value:35, name:'rose6'},
# {value:30, name:'rose7'},

# ]

from django.db.models import Count
from django.http import JsonResponse
class IndexView(View):
    def get(self, request):
        node_root = TreeNode.objects.filter(node_upstream=None)
        return render(request, 'base.html',{'roots': node_root})




class DashView(View):
    def get(self, request):
        type_qs = (
            Asset.objects.filter(device_status_id=1)
            .values_list("device_type_id")
            .annotate(value=Count("device_type_id"))
        )
        
        type_value = list(dict(list(type_qs)).values())  # (3,1)
        type_key = list(dict(list(type_qs)).keys())
        # print(type_key)
        qst = []
        for m in type_key:
            qst .append(dict(Asset.device_type_choices).get(m))
            

        li = []
        a = zip(qst, type_value)
        for k, v in a:
            dic = {}
            dic["name"] = k
            dic["value"] = v
            li.append(dic)
        # print(li)

        return JsonResponse(li, safe=False)



def ajax_upload(request):
    """
    接收前端 Ajax 发送过来的数据和文件
    :param request:
    :return:
    """
    import os,json
    response = BaseReponse()
    try:
        print('reqpost数据>>:', request.POST)
        print('reqfile数据>>:', request.FILES)
        file_obj = request.FILES.get('sub_file_name')
        print('接收到的文件>>:', file_obj)
        print('参数key one 的值>>:', request.POST.get('one'))
        print('参数key two 的值>>:', request.POST.get('two'))

        # file_dir = os.path.join(settings.BASE_DIR, 'img') # 设置接收文件的绝对路径
        # print("文件保存的绝对路径>>:", file_dir)
        """下面的是把接收到的文件保存到服务器上"""
        file_path = os.path.join('static', file_obj.name) # 组合文件的完整路径
        new_file_obj = open(file_path, 'wb')
        [new_file_obj.write(chunk) for chunk in file_obj.chunks()]
        new_file_obj.close()

        """设置一下返回信息和状态"""
        response.status = True
        response.data = file_path
    except Exception as e:
        response.status = False
        response.error = "上传失败"

    return HttpResponse(json.dumps(response.__dict__))