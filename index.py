from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

import os
from os import path
import sys

import urllib.request
import pafy
import humanize


form_class,_= loadUiType(path.join(path.dirname(__file__),"main.ui"))


class MainApp(QMainWindow,form_class):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttons()




    def Handel_UI(self):
        self.setWindowTitle("PyDownloader")
        self.setFixedSize(580,280)

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)
        self.pushButton_7.clicked.connect(self.Get_Youtube_Video)
        self.pushButton_4.clicked.connect(self.Download_Youtube_Video)
        self.pushButton_3.clicked.connect(self.Save_Browse)
        self.pushButton_5.clicked.connect(self.PlayList_Download)
        self.pushButton_6.clicked.connect(self.Save_Browse)


    def Handel_Browse(self):
        save_file = QFileDialog.getSaveFileName(self, caption="Save As",directory=".",
                                              filter="All Files(*.*)")
        text= str(save_file)
        name = (text[2:].split(',')[0].replace("'",''))
        self.lineEdit_2.setText(name)


    def Handel_Progress(self, blocknum, blocksize,totalsize):
        read = blocknum * blocksize
        if totalsize > 0:
            percent = read * 100 / totalsize
            self.progressBar.setValue(percent)

            #Partial Solution For Not Responding
            QApplication.processEvents()


    def Download(self):
        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        try:
            urllib.request.urlretrieve(url,save_location,self.Handel_Progress)
        except Exception:
            QMessageBox.warning(self, "Download Error", "Download Failed")
            return

        QMessageBox.information(self,"Download Completed","Download Finished")

        self.progressBar.setValue(0)
        self.self.lineEdit.setText("")
        self.self.lineEdit_2.setText("")




    def Save_Browse(self):
        save = QFileDialog.getExistingDirectory(self,"Select Download Directory")
        self.lineEdit_4.setText(save)
        self.lineEdit_5.setText(save)





    def Get_Youtube_Video(self):
        video_link = self.lineEdit_3.text()
        v = pafy.new(video_link)

        '''
        print(v.title)
        print(v.duration)
        print(v.rating)
        print(v.author)
        print(v.length)
        print(v.keywords)
        print(v.thumb)
        print(v.videoid)
        print(v.viewcount)
        '''

        st = v.videostreams
        #print(st)

        for s in st:
            size = humanize.naturalsize(s.get_filesize())
            data = '{} {} {} {}' .format(s.mediatype, s.extension , s.quality, size)
            self.comboBox.addItem(data)


    def Download_Youtube_Video(self):
        video_link = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()
        v = pafy.new(video_link)
        st = v.videostreams
        quality = self.comboBox.currentIndex()

        down = st[quality].download(filepath='save_location')

        QMessageBox.information(self, "Download Completed", "The Video Download Finished")



    def PlayList_Download(self):
        Playlist_url = self.lineEdit_6.text()
        save_location = self.lineEdit_5.text()
        playlist = pafy.get_playlist(Playlist_url)

        videos = playlist['items']

        os.chdir(save_location)

        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))


        for video in videos:
            p= video['pafy']
            best = p.getbest(preftype="mp4")
            best.download()






def main():
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        app.exec_()

if __name__ == '__main__':
    main()



