import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtGui, QtCore
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
import sqlite3
from datetime import datetime



class serialThreadClass( QtCore.QThread ):  # Seri Porttan veri okuma işlemi için QThread Kullanıldı.

    message = QtCore.pyqtSignal( str )

    def __init__(self, parent=None):

        super( serialThreadClass, self ).__init__( parent )
        self.serialPort = serial.Serial()
        self.stopflag = True

    def stop(self):
        self.stopflag = False

    def run(self):
        while True:
            if (self.stopflag):
                self.stopflag = True
                break
            elif (self.serialPort.isOpen()):  # eğer seri Port bağlı değil iken veri okumayı denersek hata verir.
                try:  # bu hatayı yakalayabilmek için "try" bloğu kullanıldı.
                    self.data = self.serialPort.readline()
                except:
                    print( "HATA\n" )
                self.message.emit( str( self.data.decode() ) )


class Pencere( QtWidgets.QWidget ):  # arayüz sınıfı
    def __init__(self):
        super().__init__()
        self.connect_database()
        self.connect_temp_database()
        self.connect_measure_database()
        self.initUi()

    def connect_database(self):
        connection = sqlite3.connect( "my_data.db" )
        self.cursor = connection.cursor()
        self.cursor.execute("Create Table If Not Exists All_data(Sicaklik INT , Nem INT , Veri_tarihi)")
        connection.commit()

    def connect_temp_database(self):
        connection = sqlite3.connect("my_data.db")
        self.cursor = connection.cursor()
        self.cursor.execute("Create Table If Not Exists Sicaklik_data(Sicaklik INT , Veri_tarihi)")
        connection.commit()

    def connect_measure_database(self):
        connection = sqlite3.connect("my_data.db")
        self.cursor = connection.cursor()
        self.cursor.execute("Create Table If Not Exists Nem_data(Nem INT , Veri_tarihi)")
        connection.commit()




    def initUi(self):
        ############### Com Port Combo box ###############
        self.portComboBox = QtWidgets.QComboBox()
        self.ports = serial.tools.list_ports.comports()  # Com portlar listelendi.
        for i in self.ports:
            self.portComboBox.addItem( str( i ) )
        ################### Baudrate Combo Box########################
        self.baudComboBox = QtWidgets.QComboBox()
        baud = ["300", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "74880", "115200", "230400", "250000",
                "500000", "1000000", "2000000"]
        for i in baud:
            self.baudComboBox.addItem( i )  # baud dizisinin içerisindeki değerler eklendi.
        self.baudComboBox.setCurrentText( baud[4] )  # pencere ilk açıldığında baudrate 9600 olsun.
        ########################## Butonlar ##################################

        self.baglan = QtWidgets.QPushButton( "Bağlan" )
        self.baglantiKes = QtWidgets.QPushButton( "Bağlantıyı Kes" )
        self.sicaklikbaglan = QtWidgets.QPushButton( "Sıcaklık Grafiğine Bağlan" )
        self.check_system_button = QtWidgets.QPushButton( "Sistem Donanımını Kontrol Et" )
        self.nembaglan = QtWidgets.QPushButton( "Nem Grafiğine Bağlan" )
        self.all_data_write = QtWidgets.QPushButton("Tüm Verileri Yazdır")
        self.temizle = QtWidgets.QPushButton( "Seri Port İletilerini Temizle" )

        ######################################################################
        self.label1 = QtWidgets.QLabel(
            '<font color=red>COM port bağlı değil!!!</font>' )  # böyle yazıldığı zaman yazı rengi kırmızı olacak.

        portVbox = QtWidgets.QVBoxLayout()

        portVbox.addWidget( self.portComboBox )
        portVbox.addWidget( self.baudComboBox )
        portVbox.addWidget( self.baglan )
        portVbox.addWidget( self.baglantiKes )

        portVbox.addWidget( self.label1 )

        self.portGroup = QtWidgets.QGroupBox( "Port Seçme" )
        self.portGroup.setLayout( portVbox )
        buttonHbox1 = QtWidgets.QHBoxLayout()
        buttonHbox1.addWidget( self.check_system_button )

        buttonHbox2 = QtWidgets.QHBoxLayout()
        buttonHbox2.addWidget( self.sicaklikbaglan )

        buttonHbox3 = QtWidgets.QHBoxLayout()
        buttonHbox3.addWidget( self.nembaglan )



        buttonHbox4 = QtWidgets.QHBoxLayout()
        buttonHbox4.addWidget(self.temizle)

        self.message = QtWidgets.QTextEdit()
        self.message.setReadOnly(True )  # bu satırda text edit sadece okunabilir olarak ayarlandı. Yani textedit'in içine yazı yazılamaz.
        self.messageTitle = QtWidgets.QLabel( "Gelen Mesaj" )

        self.title1 = QtWidgets.QLabel( '<font color=Black>Python - Arduino Serial Read</font>' )
        self.title1.setFont( QtGui.QFont( "Arial", 15, QtGui.QFont.Bold ) )
        self.title2 = QtWidgets.QLabel( "Seçkin Şevki ÖZER " )
        self.title2.setFont( QtGui.QFont( "Arial", 10, QtGui.QFont.Normal ) )
        self.title3 = QtWidgets.QLabel( "seckinsevkiozer.pythonanywhere.com " )
        self.title3.setFont( QtGui.QFont( "Arial", 10, QtGui.QFont.Normal ) )
        self.title4 = QtWidgets.QLabel( "GitHub : Seckinozer01" )
        self.title4.setFont(QtGui.QFont("Arial",10 , QtGui.QFont.Normal))
        self.title5 = QtWidgets.QLabel("1031120533 Seçkin Şevki Özer")
        self.title5.setFont(QtGui.QFont("Arial",10 , QtGui.QFont.Normal ))



        vBox = QtWidgets.QVBoxLayout()
        vBox.addStretch()
        vBox.addWidget( self.title1 )
        vBox.addWidget( self.title2 )
        vBox.addWidget( self.title3 )
        vBox.addWidget(self.title4)
        vBox.addWidget( self.portGroup )
        vBox.addLayout( buttonHbox1 )
        vBox.addLayout( buttonHbox2 )
        vBox.addLayout(buttonHbox3)
        vBox.addLayout(buttonHbox4)
        vBox.addWidget( self.messageTitle )
        vBox.addWidget( self.message )
        vBox.addWidget(self.title5)
        vBox.addStretch()

        hBox = QtWidgets.QHBoxLayout()
        hBox.addStretch()
        hBox.addLayout( vBox )
        hBox.addStretch()

        self.setLayout( hBox )
        self.setWindowTitle( "Mikro İşlemci Ve Gömülü Sistemler" )

        self.mySerial = serialThreadClass()
        self.mySerial.message.connect(self.messageTextEdit )
        self.mySerial.start()

        self.baglan.clicked.connect(self.serialConnect )
        self.baglantiKes.clicked.connect( self.serialDisconnect )
        self.sicaklikbaglan.clicked.connect(self.connect_temp_graph)
        self.check_system_button.clicked.connect(self.check_system_parts)
        self.nembaglan.clicked.connect(self.nemgrafikbaglan)
        self.temizle.clicked.connect( self.clear )

        self.show()

    def serialConnect(self):

        self.portText = self.portComboBox.currentText()
        self.port = self.portText.split()
        self.baudrate = self.baudComboBox.currentText()
        self.mySerial.serialPort.baudrate = int( self.baudrate )
        self.mySerial.serialPort.port = self.port[0]

        try:
            self.mySerial.serialPort.open()
        except:
            self.message.append( "Bağlantı Hatası!!" )
        if (self.mySerial.serialPort.isOpen()):
            self.label1.setText('<font color=green>Bağlantı Başarılı</font>' )
            self.baglan.setEnabled(False)
            self.portComboBox.setEnabled( False )
            self.baudComboBox.setEnabled( False )

    def serialDisconnect(self):
        if self.mySerial.serialPort.isOpen():
            self.mySerial.serialPort.close()
            if self.mySerial.serialPort.isOpen() == False:
                self.label1.setText( '<font color=red>Bağlantı Kesildi</font>' )
                self.baglan.setEnabled( True )
                self.portComboBox.setEnabled( True )
                self.baudComboBox.setEnabled( True )
        else:
            self.message.append( "Seriport Zaten Kapalı." )

    def messageTextEdit(self):
        self.incomingMessage = str( self.mySerial.data.decode() )
        self.message.append( self.incomingMessage )



    def check_system_parts(self):
        if self.mySerial.serialPort.isOpen():
            self.message.append("Sistem Donanımları İçin Test Başlatılıyor...")
            self.mySerial.serialPort.write( "4".encode() )
            if self.mySerial.serialPort.readline == []:

                self.message.append( "Sistem Veri Göndermedi" )
            else:
                self.message.append( "Sistem Donanımlarından Veri Alınıyor..." )
        else:
            self.message.append("Seri Port Bağlı Değil Lütfen Önce Seri Port Bağlantısını Sağlayın.")
    def connect_temp_graph(self):

        connection = sqlite3.connect( "my_data.db" )#veri tabanı bağlantısı sağlandı
        self.cursor = connection.cursor()


        def add_data(sicaklik, Veri_tarihi):#veri tabanına veri eklemek için gerekli olan veri parametreleri belirledik
            self.cursor.execute( "Insert Into Sicaklik_data Values (?,?)", (sicaklik, Veri_tarihi) )
            connection.commit()
        my_data_list = ['']#veri tabanından çekeceğimiz veriler için bir boş liste oluşturduk

        if self.mySerial.serialPort.isOpen():#seri port kontrol edildi
            data = np.array( [] )#grafik için bir data değişkeni oluşturduk.
            plt.figure()#veri tabanının açılmasını sağladık
            plt.ion()
            plt.show()
            i = 1
            while True:#aksini belirten bir komut gelmediği sürece fonksiyonu çalıştaracak döngüye sokuyoruz.
                self.mySerial.serialPort.write("1".encode())#seri port üzerinden arduinoya 1 mesajı gönderildi.
                myData = str( self.mySerial.serialPort.readline().decode().strip( '\r\n' ) )#arduinodan gelen verileri anlık olarak değişen myData değişkenine eşitledik
                i += 1
                my_data_list.append( myData )#veri tabanı için oluşturduğumuz listeye arduinodan gelen myData verisini yazdık

                for sicaklik in my_data_list:#liste üzerinde gezinerek grafiğin oluşması için gerekli verileri çektik
                    if my_data_list != ['']:#data listesini kontrol ettik eğer liste boş ise sistem hata verecek
                        print( "Sicaklik Verisi : ", sicaklik )#grafiği doğrulamak için veriyi terminalde yazdırdık.
                        my_data_list.pop( 0 )#program ilk başladığı anda boş sıcaklık verisi yazacağı için ilk boş veriyi listeden sildik.
                        data_time = datetime.now()#verinin alındığı anı belirledik.
                        Veri_tarihi = data_time#veri tarihini veri tabanına eklemek için gerekli değişkeni belirledik.
                        if sicaklik != (''):
                            add_data( sicaklik, Veri_tarihi )#aldığımız sıcaklık ve zaman verisini veri tabanına gerçek zamanlı olarak ekledik.
                        x = data_time#grafiğimizde x ekseni zamanı belirtecek
                        y = my_data_list#y ekseni sıcaklık verimizi belirleyecek.
                        b = float( myData)
                        data = np.append( data, b )#burada grafik sabit kalacak ve yeni gelen veri sürekli grafik doğrusunun sonuna eklenecek.
                        plt.ylabel( "Sıcaklık" )
                        plt.xlabel( "Zaman" )
                        plt.plot( data )
                        plt.pause( 0.01 )
                        plt.show()

    def nemgrafikbaglan(self):
        connection = sqlite3.connect( "my_data.db" )#veri tabanına bağlandı
        self.cursor = connection.cursor()

        def add_data(Nem, data_time):#veri tabanına ekleyeceğimiz veriler için gererkli parametreleri oluşturduk.
            self.cursor.execute( "Insert Into Nem_data Values (?,?)", (Nem, Veri_tarihi) )
            connection.commit()

        my_data_list = ['']#veri tabanından çekeceğimiz bir veriler için boş bir liste oluşturduk.

        if self.mySerial.serialPort.isOpen():  # seri port kontrol edildi
            data = np.array( [] )  # grafik için bir data değişkeni oluşturduk.
            plt.figure()  # veri tabanının açılmasını sağladık
            plt.ion()
            plt.show()
            i = 1
            while True:#aksini belirten bir komut gelmediği sürece fonksiyonu çalıştaracak döngüye sokuyoruz.
                self.mySerial.serialPort.write( "3".encode() )#seri port üzerinden arduinoya 3 mesajı gönderildi.
                myData = str( self.mySerial.serialPort.readline().decode().strip( '\r\n' ) )#arduinodan gelen verileri anlık olarak değişen myData değişkenine eşitledik
                i += 1
                my_data_list.append( myData )#veri tabanı için oluşturduğumuz listeye arduinodan gelen myData verisini yazdık

                for nem in my_data_list:#liste üzerinde gezinerek grafiğin oluşması için gerekli verileri çektik
                    if my_data_list != ['']:#data listesini kontrol ettik eğer liste boş ise sistem hata verecek
                        print( "Sicaklik Verisi : ",nem )#grafiği doğrulamak için veriyi terminalde yazdırdık.
                        my_data_list.pop( 0 )#program ilk başladığı anda boş sıcaklık verisi yazacağı için ilk boş veriyi listeden sildik.
                        data_time = datetime.now()#verinin alındığı anı belirledik.
                        Veri_tarihi = data_time#veri tarihini veri tabanına eklemek için gerekli değişkeni belirledik.
                        if nem != (''):
                            add_data( nem, Veri_tarihi )#aldığımız nem ve zaman verisini veri tabanına gerçek zamanlı olarak ekledik.
                        x = data_time#grafiğimizde x ekseni zamanı belirtecek
                        y = my_data_list#grafiğimizde y ekseni nem değerini belirtecek.
                        b = float( myData )
                        data = np.append( data, b )#burada grafik sabit kalacak ve yeni gelen veri sürekli grafik doğrusunun sonuna eklenecek.
                        plt.ylabel( "Nem" )
                        plt.xlabel( "Zaman" )
                        plt.plot( data,color = "Blue")
                        plt.pause( 0.01)
                        plt.show()
    def clear(self):
        self.message.clear()#message veriline silmek için oluşturduk.


if __name__ == '__main__':
    app = QtWidgets.QApplication( sys.argv )
    pen = Pencere()
    sys.exit( app.exec_() )