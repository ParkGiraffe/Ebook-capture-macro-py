# -*- coding: euc-kr -*-


import sys
from PyQt5.QtWidgets import QProgressBar,QMainWindow, QFileDialog,QInputDialog,  QApplication, QWidget, QPushButton, QToolTip, QAction, qApp, QFileDialog
# from PyQt5.QtGui import QIcon
import pyautogui
import time
from pynput import mouse
# import PyQt5
from PIL import Image

page = 0   # ���� ������ ��  
picture_size = [] #���� ��� ��ǥ , ������ �ϴ� ��ǥ

next_page = []  #���� �������� ��ǥ
msg = "������� �����ϼ���. ��ư�� ���콺�� �ø��� ������ ���ɴϴ�."

def get_mouse_point(x, y, button, pressed):
    if pressed and button==mouse.Button.left: 
        print('�Է¹��� ��ǥ : ', (x, y))
        picture_size.append(x)
        picture_size.append(y)
    return False

def png_to_pdf(fname):
    imglist = []
    for idx, file in enumerate(fname):
        globals()['img_{}'.format(idx)] = (Image.open(file)).convert("RGB")
        imglist.append(globals()['img_{}'.format(idx)])
    img_0.save('New_pdf.pdf',save_all=True, append_images=imglist)

def get_next_page(x, y, button, pressed):
    if pressed and button==mouse.Button.left: 
        next_page.append((x, y))
    return False
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ebook_To_Pdf')
        self.statusBar().showMessage(msg)
        #--------ProgressBar
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 300, 200, 40)
        self.pbar.setValue(0)
# ���� �� �Ű������� â�� x, y ��ġ�� �����ϰ�, ���� �� �Ű������� ���� â�� �ʺ�� ���̸� �����մϴ�.
        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip("open new file")
        openFile.triggered.connect(self.show_file)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&��PDF�� ��ȯ�ϱ�')
        filemenu.addAction(openFile)
        page_btn = QPushButton('1.ĸ���� ������ ��', self)
        page_btn.resize(page_btn.sizeHint())
        page_btn.move(30, 50)
        page_btn.clicked.connect(self.page_input)

        btn_start_point = QPushButton('2.���� ��� ��ǥ ����', self)
        btn_start_point.setToolTip('�̹����� ���� ��� �������� ���콺�� �ø���, Ŭ���մϴ�.')
        btn_start_point.move(30,100)
        btn_start_point.resize(btn_start_point.sizeHint())
        btn_start_point.clicked.connect(self.Event_start_point)
        
        btn_end_point = QPushButton('3.���� �ϴ� ��ǥ ����', self)
        btn_end_point.setToolTip('�̹��� ���� �ϴ� �������� ���콺�� �ø���, Ŭ���մϴ�.')
        btn_end_point.move(30,150)
        btn_end_point.resize(btn_end_point.sizeHint())
        btn_end_point.clicked.connect(self.Event_end_point)

        btn_next_page = QPushButton('4.���� ������ ��ư ��ǥ ����', self)
        btn_next_page.setToolTip('���� �̹����� �ѱ� ��ư�� ���콺�� �ø���, Ŭ���մϴ�.')
        btn_next_page.move(30,200)
        btn_next_page.resize(btn_next_page.sizeHint()) 
        btn_next_page.clicked.connect(self.Event_next_page)

        btn_run = QPushButton('5.�����ϱ�', self)
        btn_run.setToolTip('ȭ�� �״�� �����ϴ�. �ٸ� ���α׷��� �̹����� ������ �ʵ��� ���ּ���.')
        btn_run.move(30, 250)
        btn_run.resize(btn_run.sizeHint()) 
        btn_run.clicked.connect(self.get_picture)
        self.setGeometry(400,400,500,500)
        self.show()
    def page_input(self):
        global page , picture_size
        picture_size = []
        page, ok = QInputDialog.getText(self, 'Input Dialog', '���� ������ ��:')
        if ok:
            page = int(page)
            msg = "���� ������ �� : %d, ���� �ҿ�ð� : %f��"%(page, page*0.8)
            self.status(msg)
            self.pbar.setValue(15)


    def show_file(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file' , './')
        fname[0].sort()
        if fname[0]:
            png_to_pdf(fname[0])

    def status(self,msg):
        self.statusBar().showMessage(msg)

    def Event_start_point(self):
        with mouse.Listener(on_click=get_mouse_point) as listener:
            listener.join()
            msg = "���� ��� ��ǥ : (%s, %s)"%(picture_size[0],picture_size[1])
            self.status(msg)
            self.pbar.setValue(30)

    def Event_end_point(self):
        with mouse.Listener(on_click=get_mouse_point) as listener:
            listener.join()
            msg = "���� �ϴ� ��ǥ : (%s, %s)"%(picture_size[0],picture_size[1])
            self.status(msg)
            self.pbar.setValue(45)
    def Event_next_page(self):
        with mouse.Listener(on_click=get_next_page) as listener:
            listener.join()
            msg = "'����������'��ư ��ǥ : %s"%next_page
            self.status(msg)
            self.pbar.setValue(60)

    # ��ũ����
    def get_picture(self):
        rest_of_percent = 40//page
        for i in range(page):
            # if len(picture_size) >= 4:
                # pyautogui.screenshot("%s.png" % i, region=(picture_size[0], picture_size[1],
                # picture_size[2]-picture_size[0],picture_size[3]-picture_size[1]))
            pyautogui.keyDown('winleft')
            pyautogui.press('printscreen')
            pyautogui.keyUp('winleft')
            time.sleep(0.8)
            pyautogui.click(*next_page)
            rest_of_percent += 40//page
            self.pbar.setValue(60+rest_of_percent)
            time.sleep(0.8)
        self.pbar.setValue(100)
        msg = "�̹��� ĸ�� �Ϸ�. PDF�޴��� ���� PDF�� ��ȯ�ϼ���!"
        self.status(msg)


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())