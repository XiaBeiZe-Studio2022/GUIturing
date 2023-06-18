'''


'''

import json
import os
import random
import shutil
import time
import urllib.parse
import platform
import zipfile

import dearpygui.dearpygui as dpg
import urllib3

from Libs import getInfo as GetInfo
from Tools import download_project

http = urllib3.PoolManager()

dpg.create_context()

with open("./Shit/"+str(random.randint(1,10))+".txt") as shit:
    print(shit.read())
# 读取配置
with open("config.json", "rb+") as file:
    config = file.read()
    config = json.loads(config)

with dpg.font_registry():
    with dpg.font(config["font"], 20) as font1:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
    dpg.bind_font(font1)

def download_vscode():
    dpg.configure_item("downloading",show=True)
    try:
        vscodium=http.request("GET","https://ydschool-online.nosdn.127.net/svg/Vscode.mp3")
    except:
        raise Exception("Time Out")
    with open("~temp~","wb+") as file:
        file.write(vscodium.data)
    dpg.configure_item("downloading",show=False)
    time.sleep(0.1)
    dpg.configure_item("unzip", show=True)
    with zipfile.ZipFile("~temp~") as zf:
        zf.extractall("vscode")
    dpg.configure_item("unzip",show=False)
    time.sleep(0.1)
    dpg.configure_item("complete",show=True)
    os.remove("~temp~")
if(not(platform.platform()!="Windows")):
    with dpg.window(label="不支持",no_close=True):
        dpg.add_text("不支持的系统")
    dpg.create_viewport(title="Error")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if(not(os.path.exists("./vscode"))):
    with dpg.window(label="缺少vscode"):
        dpg.add_button(label="下载",callback=download_vscode)
    with dpg.window(label="下载中",modal=True,show=False,tag="downloading",no_close=True):
        dpg.add_text("下载中")
        dpg.add_loading_indicator(style=1)
    with dpg.window(label="解压中",modal=True,show=False,tag="unzip",no_close=True):
        dpg.add_text("解压中")
        dpg.add_loading_indicator(style=1)
    with dpg.window(label="下载完成",modal=True,show=False,tag="complete",no_close=True):
        dpg.add_text("下载完成")
    dpg.create_viewport(title="Error")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

def get_project():
    url = dpg.get_value("DownloadUrl")
    path = dpg.get_value("DownloadPath")
    if url == "" or path == "":
        return
    url = urllib.parse.urlparse(url)[2].split('/')[2]
    detail = http.request('GET', f'https://icodeshequ.youdao.com/api/works/detail?id=%s' % url)
    detail = json.loads(detail.data.decode("UTF-8"))
    dpg.configure_item("downloading", show=True)
    dpg.configure_item("downloadingtext", show=True)
    download_project.get_project("https://icode.youdao.com/scratch/project/" + url, ".~temp~")
    ppath = os.path.abspath("./.~temp~.sb3")
    shutil.move(ppath, path + "/" + detail["data"]["title"] + ".sb3")
    dpg.configure_item("downloadingtext", show=False)
    dpg.configure_item("downloading", show=False)
    dpg.configure_item("downloadingstext", show=True)


def debug():
    with dpg.window(label=config["debugMenu"]["title"]):
        dpg.add_text(default_value=config["debugMenu"]["tooltip"])


def runBot(user_data):
    path="./Bots/"+user_data
    path=os.path.abspath(path)
def closeErrorWindow():
    time.sleep(0.1)
    dpg.configure_item("errorCookie", show=False)
    time.sleep(0.1)
    dpg.configure_item("login", show=True)


def getInfo():
    info = GetInfo.getInfo(dpg.get_value("cookie"))
    rightCookie = True
    try:
        userId = info["data"]["userId"]
    except KeyError:
        rightCookie = False
        dpg.configure_item("login", show=False)
        time.sleep(0.1)
        dpg.configure_item("errorCookie", show=True)
    except Exception as e:
        raise
    if (rightCookie):
        dpg.configure_item("mainMenu", show=True)
    return info


with dpg.window(label="机器人", show=False, tag="bot"):
    bots = os.listdir(".\\Bots")
    dpg.add_listbox(items=bots,label="请选择一个机器人",tag="chooseBot")
    dpg.add_button(label="确定",tag="runBot",user_data=dpg.get_value("chooseBot"))

with dpg.window(label=config["toolsMenu"]["title"], tag="tools", show=False):
    dpg.add_button(label=config["toolsMenu"]["tools"][0])
    with dpg.popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left, modal=True, tag="downloadpj"):
        with dpg.value_registry():
            dpg.add_string_value(tag="DownloadUrl")
            dpg.add_string_value(tag="DownloadPath")
        dpg.add_input_text(label="作品链接", source="DownloadUrl")
        dpg.add_input_text(label="下载地址", source="DownloadPath")
        dpg.add_button(label="确定", callback=get_project)
        dpg.add_loading_indicator(label="下载中", width=100, height=100, style=1, tag="downloading")
        dpg.add_text("下载中", tag="downloadingtext")
        dpg.add_text("下载完成", tag="downloadingstext")
        dpg.configure_item("downloading", show=False)
        dpg.configure_item("downloadingtext", show=False)
        dpg.configure_item("downloadingstext", show=False)

with dpg.window(tag="mainMenu", label="GUIturing主菜单", no_close=True, width=200, height=500, show=False):
    dpg.add_button(label=config["mainMenu"]["debug"], callback=debug)
    dpg.add_button(label="工具", callback=lambda: dpg.configure_item("tools", show=True))
    dpg.add_button(label="机器人",callback=lambda : dpg.configure_item("bot",show=True))
with dpg.window(tag="errorCookie", label="错误的cookie", modal=True, show=False):
    dpg.add_text(default_value="错误的cookie")
    dpg.add_button(label="确定", callback=closeErrorWindow)
# with dpg.window(tag="runBot",label="运行机器人")
with dpg.window(tag="login", label="登录", no_close=True, modal=True, height=300, width=500):
    dpg.add_text("输入cookie以登录小图灵账号")
    with dpg.value_registry():
        dpg.add_string_value(tag="cookie")
    dpg.add_input_text(label="cookie", source="cookie")
    dpg.add_button(label="确认", callback=getInfo)
    dpg.add_button(label="不登录", callback=lambda: dpg.configure_item("mainMenu", show=True))
dpg.create_viewport(title="GUIturing")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
