from ctypes import c_long,py_object,pythonapi
from inspect import isclass
from wx import ID_NEW, ID_ANY, Icon, EVT_MENU, Menu, Frame, App, Exit
from wx.adv import TaskBarIcon
import readAsHTML
from threading import Thread
from webbrowser import open as op
from socket import gethostname,getaddrinfo,gethostbyname
from sys import exit as ex
# HOST = gethostbyname(getfqdn(gethostname()))
HOST = getaddrinfo(gethostname(),None)[5][-1][0]
class MyTaskBarIcon(TaskBarIcon):
    ICON = "static/favicon.ico"
    ID_EXIT = ID_ANY
    ID_SHOW_WEB = ID_NEW
    TITLE = "Flask_demo"
    flag = False

    def __init__(self):
        TaskBarIcon.__init__(self)
        self.SetIcon(Icon(self.ICON), self.TITLE)
        self.Bind(EVT_MENU, self.onExit, id=self.ID_EXIT)
        self.Bind(EVT_MENU, self.onShowWeb, id=self.ID_SHOW_WEB)

    def onExit(self, event):
        Exit()

    def onShowWeb(self, event):
        op(f'http://{HOST}:{readAsHTML.app.config["PORT"]}')


    def CreatePopupMenu(self):
        menu = Menu()
        for mentAttr in self.getMenuAttrs():
            menu.Append(mentAttr[1], mentAttr[0])
        return menu

    def getMenuAttrs(self):
        return [('进入程序', self.ID_SHOW_WEB),
                ('退出', self.ID_EXIT)]


class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        MyTaskBarIcon()


class MyApp(App):
    def OnInit(self):
        MyFrame()
        return True


def _async_raise(tid, exctype):
    tid = c_long(tid)
    if not isclass(exctype):
        exctype = type(exctype)
    res = pythonapi.PyThreadState_SetAsyncExc(tid, py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)
    ex()

def main():	
        p = Thread(target=readAsHTML.app.run, args=(HOST,))
        p.start()
        app = MyApp()
        app.MainLoop()
        stop_thread(p)
        ex()
        
if __name__ == "__main__":
    main()
