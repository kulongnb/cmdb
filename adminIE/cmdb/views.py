from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .page import StandardResultsSetPagination
from rest_framework import viewsets
from .models import Asset, IDC, Cabinet, Server, Memory, Disk, SysUsers
from .serializers import (
    AssetSerializer,
    IDCSerializer,
    ServerSerializer,
    SysUsersSerializer,
    MemorySerializer,
    DiskSerializer,
    CabinetSerializer,
)

# Create your views here.
from rest_framework import generics
from rest_framework import filters
from django.views.generic import ListView

from pure_pagination.mixins import PaginationMixin
from django_filters.rest_framework import DjangoFilterBackend


class AssetListView(PaginationMixin, ListView):
    paginate_by = 10
    object = Asset
    model = Asset
    context_object_name = "assetList"
    template_name = "cmdb/asset-list-temp.html"


class AssetDetail_temp(DetailView):
    model = Asset
    context_object_name = "asset"

    def get_template_names(self):
        names = []
        type_asset = self.object.get_device_type_id_display()
        if type_asset == "服务器":
            names.insert(0, "cmdb/asset-detail.html")
        elif type_asset == "路由器":
            names.insert(0, "cmdb/router-detail.html")
        elif type_asset == "交换机":
            names.insert(0, "cmdb/switch-detail.html")

        return names

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        asset = context["asset"]
        type_map = {"服务器": "server", "路由器": "router", "交换机": "switch"}
        asset_type = asset.get_device_type_id_display()
        type_obj = type_map.get(asset_type)
        context[type_obj] = getattr(asset, type_obj)
        # context["m"]
        server = context[type_obj]
        context["memory"] = getattr(server, "memory").all()
        # print(context["memory"])
        context["disk"] = getattr(server, "disk").all()
        print(context)
        return context


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        # filters.DjangoFilterBackend,
        filters.SearchFilter,
        # filters.OrderingFilter,
    ]
    filterset_fields = ["device_type_id", "cabinet"]
    search_fields = ["device_type_id", "cabinet"]


class IDCViewSet(viewsets.ModelViewSet):
    queryset = IDC.objects.all()
    serializer_class = IDCSerializer
    pagination_class = StandardResultsSetPagination


class SysUsersViewSet(viewsets.ModelViewSet):
    queryset = SysUsers.objects.all()
    serializer_class = SysUsersSerializer
    pagination_class = StandardResultsSetPagination


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    pagination_class = StandardResultsSetPagination


class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer
    pagination_class = StandardResultsSetPagination


class DiskViewSet(viewsets.ModelViewSet):
    queryset = Disk.objects.all()
    serializer_class = DiskSerializer
    pagination_class = StandardResultsSetPagination


class AssetDetail(DetailView):
    model = Asset
    context_object_name = "asset"
    template_name = "detail.html"


class CabinetViewSet(viewsets.ModelViewSet):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    pagination_class = StandardResultsSetPagination


from .models import TreeNode
from .serializers import TreeNodeSerializer


class TreeNodeViewSet(viewsets.ModelViewSet):
    queryset = TreeNode.objects.filter(node_upstream=None)
    serializer_class = TreeNodeSerializer


class ServerListView(ListView):
    template_name = "cmdb/asset-detail.html"
    context_object_name = "servers"

    def get_queryset(self):
        node_id = self.request.GET.get("node_id")
        if node_id:
            queryset = Server.objects.filter(asset__node__id=node_id)
        else:
            queryset = Server.objects.all()
        return queryset


class ServerDetailView(DetailView):
    model = Server
    context_object_name = "server"
    template_name = "cmdb/asset-detail.html"
