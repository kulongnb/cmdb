from django.db import models
from django.utils import timezone


class TreeNode(models.Model):
    node_name = models.CharField("节点名称", max_length=128)
    node_upstream = models.ForeignKey(
        "self",
        verbose_name="上级节点",
        related_name="sub_node",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "服务树节点表"
        verbose_name_plural = verbose_name
        db_table = "tree_node"

    def __str__(self):
        up_node = self.node_upstream.node_name if self.node_upstream else "根节点"
        return f"{up_node}-->{self.node_name}"


class Tag(models.Model):
    name = models.CharField("标签", max_length=64)
    latest_date = models.DateField(
        verbose_name="更新时间", default=timezone.now, null=True, blank=True
    )
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "标签信息表"
        verbose_name_plural = verbose_name
        db_table = "tag"

    def __str__(self):
        return self.name


class IDC(models.Model):
    """
    IDC 机房信息
    """

    name = models.CharField("机房名称", max_length=128)
    addr = models.CharField("地址", max_length=256)
    phone = models.CharField("联系电话", max_length=11)
    latest_date = models.DateField(
        verbose_name="更新时间", default=timezone.now, null=True, blank=True
    )
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "机房信息表"
        verbose_name_plural = verbose_name
        db_table = "idc"

    def __str__(self):
        return self.name


class SysUsers(models.Model):
    users_choices = (("1", "超级用户"), ("2", "sudo用户"), ("3", "普通用户"))
    name = models.CharField("用户名", max_length=16)
    user_type = models.CharField(
        "用户类型", choices=users_choices, default="3", max_length=1
    )

    class Mate:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        db_table = "sysusers"

    def __str__(self):
        return self.name


class Cabinet(models.Model):
    """
    机柜信息
    """

    name = models.CharField("机柜编号", max_length=128)
    idc = models.ForeignKey(
        "idc", related_name="cabinet", verbose_name="所属机房", on_delete=models.CASCADE
    )
    latest_date = models.DateField(
        verbose_name="更新时间", default=timezone.now, null=True, blank=True
    )
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "机柜信息表"
        verbose_name_plural = verbose_name
        db_table = "cabinet"

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    资产信息表，所有资产公共信息（交换机，服务器，防火墙等）
    """

    device_type_choices = (("1", "服务器"), ("2", "路由器"), ("3", "交换机"), ("4", "防火墙"))
    device_status_choices = (("1", "上架"), ("2", "在线"), ("3", "离线"), ("4", "下架"))

    device_type_id = models.CharField(
        choices=device_type_choices, max_length=1, default="1", help_text="设备类型"
    )
    device_status_id = models.CharField(
        choices=device_status_choices, max_length=1, default="1", help_text="设备状态"
    )
    cabinet = models.ForeignKey(
        "cabinet", verbose_name="所属机柜", related_name="asset", on_delete=models.CASCADE
    )
    # cabinet = models.CharField("机柜", max_length=128)
    node = models.ForeignKey(
        "TreeNode", verbose_name="节点", related_name="assets", on_delete=models.CASCADE
    )
    tag = models.ManyToManyField("Tag", verbose_name="标签", related_name="assets")
    latest_date = models.DateField(
        verbose_name="更新时间", default=timezone.now, null=True, blank=True
    )
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "资产表"
        verbose_name_plural = verbose_name
        db_table = "asset"

    def __str__(self):
        return f"{self.tag.all()[0]}-{self.node}-{self.cabinet.name}"


class Server(models.Model):
    #'host_name', 'os_name', 'model_name','physical_count'
    asset = models.OneToOneField(
        Asset,
        related_name="server",
        verbose_name="资产",
        blank=True,
        on_delete=models.CASCADE,
    )
    os_name = models.CharField("操作系统", max_length=520)
    manager_id = models.GenericIPAddressField(
        verbose_name="IP地址", protocol="both", default="", null=True
    )
    machine = models.CharField("系统架构", max_length=520)
    host_name = models.CharField("主机名", max_length=520)
    os_version = models.CharField("系统版本", max_length=520)
    kernel = models.CharField("内核信息", max_length=520)
    model_name = models.CharField("cpu名称", max_length=128)
    cpu_type = models.CharField("cpu类型", max_length=128)
    physical_count = models.IntegerField("cpu物理颗数")
    cpu_cores = models.IntegerField("每颗cpu核心数")
    connection = models.ForeignKey(
        "Connection",
        verbose_name="连接信息",
        blank=True,
        null=True,
        related_name="server",
        on_delete=models.CASCADE,
    )
    latest_date = models.DateField(
        verbose_name="更新时间", default=timezone.now, null=True, blank=True
    )
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "服务器表"
        verbose_name_plural = verbose_name
        db_table = "server"

    def __str__(self):
        return self.host_name


class Memory(models.Model):
    capacity = models.CharField("内存容量", max_length=100, null=True)
    slot = models.CharField("插槽", max_length=128, null=True)
    model = models.CharField("内存类型", max_length=128, null=True)
    speed = models.CharField("速率", max_length=128, null=True)
    manufacturer = models.CharField("内存厂商", max_length=128, null=True)
    sn = models.CharField("产品序列号", max_length=128, null=True)
    server = models.ForeignKey(
        "Server", verbose_name="服务器", related_name="memory", on_delete=models.CASCADE
    )
    latest_date = models.DateField(
        verbose_name="更新时间", default=timezone.now, null=True, blank=True
    )
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "内存表"
        verbose_name_plural = verbose_name
        db_table = "memory"

    def __str__(self):
        return f"{self.slot}--{self.capacity}"


class Disk(models.Model):

    coreced = models.CharField("强制磁盘容量", max_length=200, null=True)
    pd = models.CharField("接口类型", max_length=10, null=True)
    raw = models.CharField("原始磁盘容量", max_length=200, null=True)
    slot = models.CharField("插槽号", max_length=10, null=True)
    server = models.ForeignKey(
        "Server", verbose_name="服务器", related_name="disk", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "硬盘表"
        verbose_name_plural = verbose_name
        db_table = "disk"

    def __str__(self):
        return self.slot


class Connection(models.Model):
    user = models.CharField("ssh用户", max_length=64)
    password = models.CharField("连接密码", max_length=1024)
    port = models.PositiveIntegerField(verbose_name="sshd监听端口")
    authed = models.BooleanField(default=False, verbose_name="是否认证", help_text="是否建立互信")

    class Meta:
        verbose_name = "服务器连接表"
        verbose_name_plural = verbose_name
        db_table = "connection"

    # def __str__(self):
    #     return "用户:{}".format(self.user)


class InventoryPool(models.Model):
    group = models.CharField(max_length=64)
    server = models.ManyToManyField("Server", related_name="Inventorypool")

    class Meta:
        verbose_name = "主机组"
        verbose_name_plural = verbose_name
        db_table = "Inventorypool"

    def __str__(self):
        return self.group




class Variable2Group(models.Model):
    """
    变量到组的关系表
    """
    key = models.CharField("变量名", max_length=64)
    val = models.CharField("变量值", max_length=512)
    group = models.ForeignKey("InventoryPool",
                                 verbose_name="所属组",
                                 related_name="inv2vars",
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)
    class Meta:
        verbose_name = "Ansible 组变量表"
        verbose_name_plural = verbose_name
        db_table = "var_group"

    def __str__(self):
        return "{}:{}={}".format(self.group.group, self.key, self.val)

class Variable2Server(models.Model):
    """
    变量到主机的关系表
    """
    key = models.CharField("变量名", max_length=64, default='')
    val = models.CharField("变量值", max_length=512, default='')
    host = models.ForeignKey("Server",
                                 verbose_name="所属主机",
                                 related_name="server2vars",
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)
    class Meta:
        verbose_name = "Ansible 主机变量表"
        verbose_name_plural = verbose_name
        db_table = "var_host"

    def __str__(self):
        return "{}:{}={}".format( self.host.host_name, self.key, self.val)



