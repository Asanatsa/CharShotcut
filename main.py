import sys, os, time
import keyboard as kb
from pathlib import Path
from windows_toasts import WindowsToaster, Toast

hot_key = 'ctrl+win'
second_key = ["1","2","3","4","5","6","7","8","9","0"]
mapping_file = Path(Path.cwd(), "key.txt") #映射文件

status = True

def key_callback(str):
    global status
    if status == True:
        print("CharInput", str)
        time.sleep(0.1)
        kb.write(str)


def showToast(title="none", text="none"):
    toaster = WindowsToaster(title)
    newToast = Toast()
    newToast.text_fields = [text]
    toaster.show_toast(newToast)


#kb.add_hotkey(hot_key+"+"+second_key[0], test, args=["test"])
#读取文件，忽略井号开头的行，返回一个list
def read_mapping_file():
    f = open(mapping_file, encoding='utf-8',  mode = 'r')
    l = f.readlines()
    r = []
    for i in l:
        if i[0] == "#":
            continue
        r.append(i.rstrip())
    return r


def mapping(list):
    d = {}
    for v in second_key:
        n = second_key.index(v)
        if n > len(list) - 1:
            break 
        d[v] = list[n]
    
    return d


def init_hotkey(l):
    
    for k,v in l.items():
        print(k)
        kb.add_hotkey(hot_key+"+"+k, key_callback, args=[v])


def pause_listen():
    global status
    if status:
        showToast("CharShotcut", "已暂停监听按键，按Ctrl+Win+Del恢复")
        status = False
    else:
        showToast("CharShotcut", "已恢复监听按键，按Ctrl+Win+Del暂停")
        status = True

def exit_listen():
    showToast("CharShotcut", "已退出CharShotcut")
    time.sleep(1)
    os._exit(0)


if not mapping_file.exists():
    showToast("CharShotcut", "key.txt不存在")
    time.sleep(1)
    sys.exit(1)



mapping_list = mapping(read_mapping_file())

init_hotkey(mapping_list)

kb.add_hotkey(hot_key+"+p", pause_listen)
kb.add_hotkey(hot_key+"+e", exit_listen)

showToast("CharShotcut", "已成功启动，按Ctrl+Win+P暂停，按Ctrl+Win+E退出")


kb.wait("f1+f2+f3+f4+win")