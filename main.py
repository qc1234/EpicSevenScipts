# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import time

from PIL import ImageGrab
import aircv
import win32api
import win32con
import win32gui
import win32process as wproc

class Shop:
    prefix = "F:\\BlueStacks\\screenshots"
    refreshPng = "refresh.png"
    confirmPng = "confirm.png"

    def __init__(self, purchase_list):
        self.remote_thread = None
        self.window = None
        self.parentWindow = None
        self.purchaseList = purchase_list
        self.bookmark = 0
        self.medal = 0
        self.stone = 0
        self.coin = 0
        self.execTime = 0

    def getWindow(self):
        parentWindow = win32gui.FindWindow(0, "BlueStacks App Player")
        window = win32gui.FindWindowEx(parentWindow, 0, "Qt5154QWindowIcon", "HD-Player")
        self.remote_thread, _ = wproc.GetWindowThreadProcessId(window)
        wproc.AttachThreadInput(win32api.GetCurrentThreadId(), self.remote_thread, True)
        self.window = window
        self.parentWindow = parentWindow
        return window

    def screenShot(self):
        window = self.window
        # app = QApplication(sys.argv)
        # screen = QApplication.primaryScreen()
        left, top, right, bottom = win32gui.GetWindowRect(self.window)
        box = (left, top, right, bottom)
        img = ImageGrab.grab(box)
        # img.show()
        img.save(Shop.prefix + "\\screenshot.png")

    def recognize(self, imgObj, confidence=0.8):
        imgSrc = aircv.imread(Shop.prefix + "\\screenshot.png")
        imgTarget = aircv.imread(Shop.prefix + "\\" + imgObj)
        match_result = aircv.find_template(imgSrc, imgTarget, confidence)
        x, y = match_result["result"]
        return int(x), int(y)

    def click(self, x, y):
        print(int(x), int(y))
        win32gui.SetFocus(self.window)
        longPosition = win32api.MAKELONG(int(x), int(y))
        a = win32api.PostMessage(self.window, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, longPosition)
        b = win32api.PostMessage(self.window, win32con.WM_LBUTTONUP, 0, longPosition)
        time.sleep(0.75)

    def clickAndMove(self, x, y):
        print(int(x), int(y))
        win32gui.SetFocus(self.window)
        longPosition = win32api.MAKELONG(x, y)
        targetPosition = win32api.MAKELONG(x, y - 400)
        win32api.PostMessage(self.window, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, longPosition)
        win32api.PostMessage(self.window, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, targetPosition)
        win32api.PostMessage(self.window, win32con.WM_LBUTTONUP, 0, targetPosition)
        time.sleep(0.75)

    def refresh(self):
        x = 85 + random.random() * 375
        # y1 = 785 - 30
        y = 785 + random.random() * 77
        print("refresh: ")
        self.stone += 3
        self.click(x, y)

    def confirm(self):
        # x1 = 800 - 30
        # y1 = 515 - 15
        x = 800 + random.random() * 255
        y = 515 + random.random() * 75
        print("confirm: ")
        self.click(x, y)

    def purchase(self, targetY):
        x = 1328 + 20 + random.random() * 180
        y = targetY + 5 + random.random() * 50
        print("purchase: ")
        self.click(x, y)

    def confirmPurchase(self):
        x = 730 + random.random() * 347
        y = 598 + random.random() * 75
        print("confirmPurchase: ")
        self.click(x, y)

    def recognizeAndPurchase(self):
        self.screenShot()
        for item in self.purchaseList:
            try:
                # 识别
                x, y = self.recognize(item)
                print("get bookmark!!!!!!!" + item)
                if item == "bookmark.png":
                    self.coin += 184000
                    self.bookmark += 1
                elif item == "medal.png":
                    self.coin += 280000
                    self.medal += 1
                self.purchase(y)
                self.confirmPurchase()
            except:
                pass

    def shopByLoop(self, loopTime):
        # 1.获取窗口句柄
        self.window = self.getWindow()
        win32gui.SetWindowPos(self.window, win32con.HWND_TOPMOST, 0, 0, 1600, 900, win32con.SWP_SHOWWINDOW)
        # 2.获取长宽高，分辨率
        left, top, right, bottom = win32gui.GetWindowRect(self.window)
        print("坐标:", "宽", right, "高", bottom, "顶", top, "左", left)
        # 3.截取图片，识别书签
        i = loopTime
        while i > 0:
            i -= 1
            # 刷新商店
            self.refresh()
            # 确认刷新
            self.confirm()
            # 识别第一张
            self.recognizeAndPurchase()
            self.clickAndMove(1000, 800)
            # 识别第二张
            self.recognizeAndPurchase()
        print("共花费天空石：", self.stone, "\n共花费金币：", self.coin, "\n出现书签：", self.bookmark, "次\n出现神秘奖牌：", self.medal, "次")

    def shopByTime(self, timeMin):
        # 1.获取窗口句柄
        self.window = self.getWindow()
        win32gui.SetWindowPos(self.window, win32con.HWND_TOPMOST, 0, 0, 1600, 900, win32con.SWP_SHOWWINDOW)
        # win32gui.MoveWindow(self.parentWindow, 0, 0, 1600, 900, True)
        # win32gui.SetActiveWindow(self.window) 可模拟后台点击，需要截图支持后台才能实现自动后台点击
        # win32gui.SetForegroundWindow(self.window)
        # win32gui.SetCursor(self.window)
        # 2.获取长宽高，分辨率
        left, top, right, bottom = win32gui.GetWindowRect(self.window)
        print("坐标:", "宽", right, "高", bottom, "顶", top, "左", left)
        # 3.截取图片，识别书签
        startTime = time.time()
        while True:
            curTime = time.time()
            print("已执行", int(curTime - startTime), "秒")
            self.execTime += 1
            if curTime - startTime >= timeMin * 60:
                break
            # 刷新商店
            self.refresh()
            # 确认刷新
            self.confirm()
            # 截图
            self.recognizeAndPurchase()
            self.clickAndMove(1000, 800)
            self.recognizeAndPurchase()
        print("共执行：", self.execTime, "次\n共花费天空石：", self.stone, "\n共花费金币：", self.coin, "\n出现书签：", self.bookmark, "次\n出现神秘奖牌：", self.medal, "次")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 支持按照次数、时间
    mode = int(input("choose mode: \n1.按次数\n2.按时间(min)\n"))
    print("mode: ", mode)
    purchaseList = ('bookmark.png', 'medal.png')
    shop = Shop(purchaseList)
    print("请勿将窗口最小化，否则程序会退出")
    if mode == 1:
        loopTime = int(input("执行次数："))
        print("任务开始，执行", loopTime, "次")
        shop.shopByLoop(loopTime)
    elif mode == 2:
        timeMin = int(input("执行时间(min)："))
        print("任务开始，执行", timeMin, "分钟")
        shop.shopByTime(timeMin)
    else:
        pass
