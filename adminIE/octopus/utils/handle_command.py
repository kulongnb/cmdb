import subprocess
from adminIE.settings import INVENT_PATH as invent_path   # 导入资产清单路径
import pexpect

# 判断输入shell命令的正确性


class HandleCommand:
    ret_msg = {"status": False, "msg": "命令格式错误"}

    def __init__(self, command, inventorys):
        self.command = command
        self.invent_path = invent_path
        self.inventorys = inventorys
        self.command_tpl = "{} -i {} -{}"
        self.rewrite()

    def checked(self):
        try:
            ansib, arg = self.command.split("-", 1)
            self.command = self.command_tpl.format(
                ansib, self.invent_path, arg)  # 简单判断ansible命令
        except Exception as e:
            print(e)

        return self.command

    def exec_command(self):
        comm = self.checked()
        if comm:
            stat, r = subprocess.getstatusoutput(comm)
            if not stat:
                self.ret_msg["status"] = True
            self.ret_msg["msg"] = r
        return self.ret_msg

    def rewrite(self):
        tpl_group = "[{}]\n"
        tpl_host = "{}\n"
        content_list = []
        for g in self.inventorys:
            content_list.append(tpl_group.format(g.group))
            for h in g.server.all():
                content_list.append(tpl_host.format(h.manager_id))
        with open(self.invent_path, 'w', encoding="utf-8") as f:
            f.writelines(content_list)


#  实现免密无交互
class no_secret:
    def __init__(self, command, pwd):
        self.command = command
        self.pwd = pwd

    def no_interaction(self):
        try:
            child = pexpect.spawn(self.command)
        except Exception as e:
            print(e)
        index = child.expect(
            ["yes/no", "password", "exist", pexpect.exceptions.EOF, pexpect.TIMEOUT],
            timeout=20,
        )
        try:
            # print ("开始向%s上传公钥"%(server))
            child.sendline("yes")
            child.expect("password")
            child.sendline(self.pwd)
            child.expect("added")
            # print ("已向%s上传公钥"%(server))
            return True
        except Exception as e:
            return False
