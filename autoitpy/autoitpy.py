from __future__ import print_function

import ctypes
from ctypes import windll
from ctypes.wintypes import LPCWSTR, LONG
import os
from pythoncom import LoadTypeLib
import sys

from .getobject import CoCreateInstanceFromDll, CoDllGetClassObject


class AutoIt(object):

    def __init__(self, dll_path):
        clsid = LoadTypeLib(dll_path).GetLibAttr()[0]
        # clsid = LoadTypeLib(dll_path).GetTypeInfo(1).GetTypeAttr().iid
        # self.autoit = CoCreateInstanceFromDll(dll_path, clsid)
        self.autoit = windll.LoadLibrary(dll_path)
        self.autoit.DllRegisterServer()
        self.autoit.DllUnregisterServer()
        # self.autoit.DllGetClassObject()
        self.autoit.AU3_Init()
        self.autoit.AU3_error()
        self.autoit.AU3_Opt(u"WinTitleMatchMode", 2)    # subStr

    def ControlClick(self, title, text, control, button=u"primary", clicks=1, x=-1, y=-1):
        return self.autoit.AU3_ControlClick(title, text, control, button, clicks, x, y)

    def ProcessWaitClose(self, pid, timeout=-1):
        return self.autoit.AU3_ProcessWaitClose(u"%d" % pid, timeout)

    def Run(self, exe_fullpath, show_flag=1):
        # working_dir, program = os.path.split(exe_fullpath)
        program = exe_fullpath
        working_dir = u""
        self.autoit.AU3_Run.argtypes = (LPCWSTR, LPCWSTR, LONG)
        self.autoit.AU3_Run.restype = LONG
        return self.autoit.AU3_Run(program, working_dir, show_flag)

    def Send(self, text, mode=1):
        return self.autoit.AU3_Send(text, mode)

    def WinActivate(self, title, text=u""):
        return self.autoit.AU3_WinActivate(title, text)

    def WinActive(self, title, text=u""):
        return self.autoit.AU3_WinActive(title, text)

    def WinClose(self, title, text=u""):
        return self.autoit.AU3_WinClose(title, text)

    def WinDisable(self, title, text=u"", flag=6):
        return self.autoit.AU3_WinSetState(title, text, flag)

    def WinEnable(self, title, text=u"", flag=5):
        return self.autoit.AU3_WinSetState(title, text, flag)

    def WinExists(self, title, text=u""):
        return self.autoit.AU3_WinExists(title, text)

    def WinHide(self, title, text=u"", flag=0):
        return self.autoit.AU3_WinSetState(title, text, flag)

    def WinMaximize(self, title, text=u"", flag=3):
        return self.autoit.AU3_WinSetState(title, text, flag)

    def WinMenuSelectItem(self, title, *items, **kwargs):
        text = kwargs.get("text", "")
        if not (0 < len(items) < 8):
            raise ValueError("accepted none item or number of items exceed eight")
        f_items = [LPCWSTR(item) for item in items]
        for i in xrange(8 - len(f_items)):
            f_items.append(LPCWSTR(""))
        print(f_items)
        ret = self.autoit.AU3_WinMenuSelectItem(LPCWSTR(title), LPCWSTR(text),
                                            *f_items)
        return ret

    def WinMinimize(self, title, text=u"", flag=2):
        return self.autoit.AU3_WinSetState(title, text, flag)

    def WinRestore(self, title, text=u"", flag=4):
        return self.autoit.AU3_WinSetState(title, text, flag)

    def WinShow(self, title, text=u"", flag=1):
        return self.autoit.AU3_WinSetState(title, text, flag)

    def WinWait(self, title, text=u"", timeout=-1):
        return self.autoit.AU3_WinWait(title, text, timeout)

    def WinWaitActive(self, title, text=u"", timeout=-1):
        return self.autoit.AU3_WinWaitActive(title, text, timeout)

    def WinWaitClose(self, title, text=u"", timeout=-1):
        return self.autoit.AU3_WinWaitClose(title, text, timeout)

    def WinWaitNotActive(self, title, text=u"", timeout=-1):
        return self.autoit.AU3_WinWaitNotActive(title, text, timeout)


def autoit_init():
    maxsize_64 = 9223372036854775807           # 64 bit
    platform = '64bit' if sys.maxsize == maxsize_64 else '32bit'
    dll_file = 'AutoItX3_x64.dll' if platform == '64bit' else 'AutoItX3.dll'
    dll_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AutoItX', dll_file)
    return AutoIt(dll_path)
