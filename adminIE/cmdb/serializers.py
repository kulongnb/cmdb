from rest_framework import serializers
from .models import Asset, IDC, Cabinet, Server, SysUsers, Disk, Memory


class AssetSerializer(serializers.ModelSerializer):
    device_type = serializers.SerializerMethodField()
    device_status = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = "__all__"

    def get_device_type(self, obj):
        return obj.get_device_type_id_display()

    def get_device_status(self, obj):
        return obj.get_device_status_id_display()


class IDCSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDC
        fields = "__all__"


class CabinetSerializer(serializers.ModelSerializer):
    idc = IDCSerializer()

    class Meta:
        model = Cabinet
        fields = "__all__"

    def create(self, validated_data):
        return Cabinet.objects.create(**validated_data)


class SysUsersSerializer(serializers.ModelSerializer):
    user_type_id = serializers.SerializerMethodField()

    class Meta:
        model = SysUsers
        fields = "__all__"

    def get_user_type_id(self, obj):
        return obj.get_user_type_display()


class ServerSerializer(serializers.ModelSerializer):
    asset = AssetSerializer()
    # sysusers = SysUsersSerializer()
    class Meta:
        model = Server
        fields = "__all__"

    def create(self, validated_data):
        return Server.objects.create(**validated_data)


class MemorySerializer(serializers.ModelSerializer):
    server = ServerSerializer()

    class Meta:
        model = Memory
        fields = "__all__"

    def create(self, validated_data):
        return Server.objects.create(**validated_data)


class DiskSerializer(serializers.ModelSerializer):
    server = ServerSerializer()

    class Meta:
        model = Disk
        fields = "__all__"

    def create(self, validated_data):
        return Server.objects.create(**validated_data)


from .models import TreeNode

from .models import TreeNode
class subsubTreeNodeSerializer(serializers.ModelSerializer):
    sub_node = serializers.SerializerMethodField()
    class Meta:
        model = TreeNode
        fields = "__all__"
    def get_sub_node(self,obj):
        return []
        
class subTreeNodeSerializer(serializers.ModelSerializer):
    sub_node = subsubTreeNodeSerializer(many=True)
    class Meta:
        model = TreeNode
        fields = "__all__"

class TreeNodeSerializer(serializers.ModelSerializer):
    sub_node = subTreeNodeSerializer(many=True)
    class Meta:
        model = TreeNode
        fields = "__all__"