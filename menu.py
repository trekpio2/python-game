import PyQt5.QtWidgets as pq
import PyQt5.QtCore as pqC
from PyQt5.QtGui import QCursor

class Menu:
    def __init__(self):
        self.app = pq.QApplication([])
        self.window = pq.QWidget()
        self.window.setFixedSize(800, 650)
        self.window.setWindowTitle('Menu')

        self.started = False
        self.saveData = [1, 100, 0]

        self.layout = pq.QVBoxLayout()
        self.newGameButton = pq.QPushButton('New Game')
        self.newGameButton.clicked.connect(self.newGame)
       
        self.loadButton = pq.QPushButton('Load')
        self.loadButton.clicked.connect(self.load)

        self.quitButton = pq.QPushButton('Quit')
        self.quitButton.clicked.connect(self.quitGame)

        self.setApperance()

        self.layout.addWidget(self.newGameButton)
        self.layout.addWidget(self.loadButton)
        self.layout.addWidget(self.quitButton)

        self.window.setLayout(self.layout)
        
        self.window.show()
        self.app.exec_()

    def setApperance(self):
        """
        Funkcja ustawiajaca wyglad menu
        """
        self.newGameButton.setCursor(QCursor(pqC.Qt.PointingHandCursor))
        self.loadButton.setCursor(QCursor(pqC.Qt.PointingHandCursor))
        self.quitButton.setCursor(QCursor(pqC.Qt.PointingHandCursor))

        self.window.setStyleSheet('QWidget{background-color : lightblue;} QPushButton{background-color: white; height: 200px; font-size: 100px; border-radius: 50px; } QPushButton:hover{background-color: lightgray;}')

    def newGame(self):
        """
        Funkcja startujaca gre od nowa
        """
        self.started = True
        self.close()

    def load(self):
        """
        Funkcja startujaca gre od zapisanego stanu
        """
        self.started = True
        saveFile = open('saves/save.txt', 'r')
        for i in range(3):
            self.saveData[i] = int(saveFile.readline().rstrip('\n'))
        
        saveFile.close()
        self.close()

    def quitGame(self):
        """
        Funkcja wyjscia - gra sie  nie wlacza
        """
        self.close()

    def close(self):
        """
        Funkcja zamykajaca okno i zamykajaca aplikacje menu
        """
        self.window.close()
        self.app.exit()

gameMenu = Menu()