import sys, platform, struct, serial, serial.tools.list_ports
from PyQt5 import QtWidgets, uic

qtCreatorFile = 'valkyrie.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class valkyrie(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Project Valkyrie')
        self.lcdNumber.setToolTip('Value of PWM in percent.')
        self.labelOS.setToolTip('Your operating system.')
        self.labelPort.setToolTip('Your active serial port.')
        self.sliderLang.valueChanged[int].connect(self.Slider)
        self.sliderLang.setToolTip('Adjust PWM.')
        self.pushButtonInitialize.clicked.connect(self.Initialize)
        self.pushButtonInitialize.setToolTip('Initialize your systems.')
        self.pushButtonConnect.clicked.connect(self.Connect)
        self.pushButtonConnect.setToolTip('Please connect your device.')
        self.comboBoxBaudrate.activated[str].connect(self.ChooseBaudrate)
        self.comboBoxBaudrate.setToolTip('Choose baudrate.')
        self.textEditLog.setText('16/404566/PTK/10983')
        self.textEditLog.setToolTip('Comunication Logger.')
        
    def Initialize(self):
        print(platform.system(), platform.release())
        self.labelOS.setText(platform.system() + ' ' + platform.release())
        portList = list(serial.tools.list_ports.comports())
        print(portList)
        for port in portList:
            if 'VID:PID=2341:0043' in port[0]\
            or 'VID:PID=2341:0043' in port[1]\
            or 'VID:PID=2341:0043' in port[2]:
                self.textEditLog.setText('Found Arduino Uno.')
                self.pushButtonConnect.setEnabled(True)
            else:
                self.textEditLog.setText('No Arduino Uno was found.')
            self.unoPort = port[0]            
            self.labelPort.setText(self.unoPort)
            #please note: it is not sure [0]
            #returned port[] is no particular order
            #so, may be [1], [2]
        
    def ChooseBaudrate(self, text):
        self.baudrate = text
        
    def Connect(self):
        if self.pushButtonConnect.text() == 'Connect':
            self.ser = serial.Serial(self.unoPort, self.baudrate, timeout=0.1)
            if self.ser.isOpen():
                self.sliderLang.setEnabled(True)
                self.pushButtonConnect.setText('Disconnect')
                self.textEditLog.append('Opening serial port.')
            else:
                self.textEditLog.append('Can not open serial port.')
        else:
            if self.ser.isOpen():
                self.ser.close()
            self.sliderLang.setEnabled(False)
            self.pushButtonConnect.setText('Connect')
            self.textEditLog.append('Closing serial port.')
    
    def Slider(self, value):
        self.sliderLang.valueChanged.connect(self.lcdNumber.display)
        self.ser.write(struct.pack('>B', value))
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = valkyrie()
    window.show()
    sys.exit(app.exec_())