import json
import shutil
import urllib.parse
import dearpygui.dearpygui as dpg
import urllib3
import os
import Download_project

http = urllib3.PoolManager()

# 读取配置
with open("config.json", "rb+") as file:
    config = file.read()
    pconfig = json.loads(config)


def get_project():
    url = dpg.get_value("DownloadUrl")
    path = dpg.get_value("DownloadPath")
    if (url == "" or path == ""):
        print(2)
        return
    url = urllib.parse.urlparse(url)[2].split('/')[2]
    detail = http.request('GET', f'https://icodeshequ.youdao.com/api/works/detail?id=%s' % url)
    detail = json.loads(detail.data.decode("UTF-8"))
    print(1)
    dpg.configure_item("downloading", show=True)
    dpg.configure_item("downloadingtext", show=True)
    Download_project.get_project("https://icode.youdao.com/scratch/project/" + url, ".~temp~")
    ppath = os.path.abspath("./.~temp~.sb3")
    shutil.move(ppath, path + "/" + detail["data"]["title"] + ".sb3")
    dpg.configure_item("downloadingtext", show=False)
    dpg.configure_item("downloading", show=False)
    dpg.configure_item("downloadingstext", show=True)


def debug():
    with dpg.window(label=pconfig["debugMenu"]["title"]):
        dpg.add_text(default_value=pconfig["debugMenu"]["tooltip"])


def tool():
    dpg.configure_item("tools", show=True)


dpg.create_context()

# 注册字体
with dpg.font_registry():
    with dpg.font(pconfig["font"], 20) as font1:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
    dpg.bind_font(font1)

with dpg.window(label=pconfig["toolsMenu"]["title"], tag="tools", show=False):
    dpg.add_button(label=pconfig["toolsMenu"]["tools"][0])
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
with dpg.window(tag="mainMenu", label="GUIturing主菜单", no_close=True, width=200, height=500):
    dpg.add_button(label=pconfig["mainMenu"]["debug"], callback=debug)
    dpg.add_button(label="工具", callback=tool)
dpg.create_viewport(title="GUIturing")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
