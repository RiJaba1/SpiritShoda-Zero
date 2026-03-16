import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from shodan_api import ShodanClient
from exporter import export_excel, export_json
from config_manager import get_api_key, set_api_key


class FiltersHelpWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("READ THE FUCKING MANUAL - Filters & Examples")
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout()

        info = QTextEdit()
        info.setReadOnly(True)

        # html manual (aquí es donde me gustaría una aportación de traducción y ampliación de conetenido por vuestra parte, querida comunidad. NO SEÁIS VGAGOS)
        help_text = """
<h1>The Fucking Manual</h1>
<p>Este manual recoge los filtros más útiles de la API/buscador de Shodan y ejemplos de consultas listas para copiar y pegar en el campo de búsqueda de la aplicación.</p>

<h2>Filtros básicos</h2>
<ul>
  <li><b>country:</b> Limita por país (código ISO). Ej: <code>apache country:ES</code></li>
  <li><b>city:</b> Limita por ciudad. Ej: <code>nginx city:\"Madrid\"</code></li>
  <li><b>port:</b> Filtra por puerto. Ej: <code>port:22 product:\"OpenSSH\"</code></li>
  <li><b>hostname:</b> Coincidencia con hostname. Ej: <code>hostname:\"example.com\"</code></li>
  <li><b>org:</b> Organización o ISP. Ej: <code>org:\"Microsoft\"</code></li>
  <li><b>asn:</b> Búsqueda por AS. Ej: <code>asn:AS15169</code></li>
</ul>

<h2>Filtros de servicio y banner</h2>
<ul>
  <li><b>product:</b> Producto detectado. Ej: <code>product:\"Apache httpd\"</code></li>
  <li><b>version:</b> Versión del servicio. Ej: <code>product:\"OpenSSH\" version:7.2</code></li>
  <li><b>http.title:</b> Título de la página web. Ej: <code>http.title:\"Login\"</code></li>
  <li><b>http.html:</b> Texto en el HTML. Ej: <code>http.html:\"phpMyAdmin\"</code></li>
  <li><b>ssl.cert.subject.cn:</b> CN del certificado. Ej: <code>ssl.cert.subject.cn:\"microsoft.com\"</code></li>
  <li><b>ssl.cert.issuer.cn:</b> Emisor del certificado. Ej: <code>ssl.cert.issuer.cn:\"Let's Encrypt\"</code></li>
</ul>

<h2>Filtros de red y localización</h2>
<ul>
  <li><b>net:</b> Rango de red en CIDR. Ej: <code>net:192.168.0.0/16</code></li>
  <li><b>geo:</b> Coordenadas + radio (km). Ej: <code>geo:40.4168, -3.7038</code></li>
  <li><b>before / after:</b> Fecha de indexación (YYYY-MM-DD). Ej: <code>apache before:2023-01-01</code></li>
</ul>

<h2>Consultas útiles para OSINT (genéricas)</h2>
<ul>
  <li><code>\"password\" port:21</code> – FTP que quizá devuelvan banners con credenciales.</li>
  <li><code>\"Authentication Required\" http.title</code> – Portales de login genéricos.</li>
  <li><code>\"webcamXP\" port:8080</code> – Posibles cámaras IP sin proteger.</li>
  <li><code>\"Remote Desktop Web Connection\"</code> – Portales RDP vía web.</li>
</ul>

<h2>Consultas relacionadas con Microsoft</h2>
<ul>
  <li><code>product:\"Microsoft-IIS\" port:80</code> – Servidores IIS HTTP.</li>
  <li><code>product:\"Microsoft-IIS\" port:443</code> – Servidores IIS HTTPS.</li>
  <li><code>\"X-AspNet-Version\" \"X-Powered-By: ASP.NET\"</code> – Aplicaciones ASP.NET.</li>
  <li><code>port:3389 product:\"Remote Desktop\"</code> – Servicios RDP expuestos.</li>
  <li><code>ssl.cert.subject.cn:\"*.microsoft.com\"</code> – Hosts con certificados de Microsoft.</li>
</ul>

<h2>Vulnerabilidades y CVE</h2>
<p>Shodan permite filtrar por etiquetas de vulnerabilidades cuando están disponibles en los datos.</p>
<ul>
  <li><b>vuln:</b> Filtra por identificador CVE. Ejemplos:
    <ul>
      <li><code>vuln:CVE-2021-26855</code> – Exchange ProxyLogon.</li>
      <li><code>vuln:CVE-2019-0708</code> – BlueKeep (RDP).</li>
      <li><code>vuln:CVE-2021-44228</code> – Log4Shell.</li>
    </ul>
  </li>
  <li>Combinar con otros filtros:
    <ul>
      <li><code>vuln:CVE-2021-44228 country:ES</code></li>
      <li><code>vuln:CVE-2019-0708 port:3389</code></li>
    </ul>
  </li>
</ul>

<h2>Patrones para dorks OSINT rápidos</h2>
<ul>
  <li><code>http.title:\"phpMyAdmin\" -port:443</code> – Paneles phpMyAdmin sin HTTPS.</li>
  <li><code>\"Remote Desktop Web Connection\" country:ES</code> – RDP web en España.</li>
  <li><code>\"Docker Registry\" port:5000 -authentication</code> – Registries Docker abiertos.</li>
  <li><code>\"Kibana\" port:5601</code> – Dashboards Kibana expuestos.</li>
  <li><code>\"MongoDB Server Information\" port:27017 -authentication</code> – Mongo sin auth.</li>
</ul>

<h2>Combos útiles</h2>
<ul>
  <li>Por tecnología + país:
    <ul>
      <li><code>product:\"Apache httpd\" country:ES</code></li>
      <li><code>product:\"nginx\" country:MX</code></li>
    </ul>
  </li>
  <li>Por paneles de administración:
    <ul>
      <li><code>http.title:\"Admin\" port:80</code></li>
      <li><code>http.title:\"Login\" org:\"Microsoft\"</code></li>
    </ul>
  </li>
  <li>Por organización concreta:
    <ul>
      <li><code>org:\"Amazon\" port:9200</code> – Clústeres Elasticsearch en Amazon.</li>
      <li><code>org:\"Google\" \"openresty\"</code></li>
    </ul>
  </li>
</ul>

<h2>Consejos</h2>
<ul>
  <li>Empieza con consultas amplias y ve refinando con filtros (country, port, org…).</li>
  <li>Combina <code>vuln:</code> con <code>country:</code>, <code>net:</code> o <code>org:</code> para priorizar hallazgos.</li>
  <li>Guarda tus mejores consultas para reutilizarlas desde esta GUI.</li>
</ul>
        """

        info.setHtml(help_text)
        layout.addWidget(info)

        self.setLayout(layout)


class ShodanGUI(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Shoda SpiritAdmins GUI")

        self.setGeometry(200,200,900,600)

        self.api_key = get_api_key()

        self.init_ui()

        self.apply_dark_theme()


    def init_ui(self):

        layout = QVBoxLayout()

        # LOGO 
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        try:
            pixmap = QPixmap("assets/logo.png")
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaledToWidth(200, Qt.TransformationMode.SmoothTransformation))
        except Exception:
            pass
        layout.addWidget(self.logo_label)

        # API KEY

        self.key_input = QLineEdit(self.api_key)

        save_btn = QPushButton("Save Fucking API Key")

        save_btn.clicked.connect(self.save_key)

        layout.addWidget(QLabel("Shodan API Key"))
        layout.addWidget(self.key_input)
        layout.addWidget(save_btn)

        # query

        self.query_input = QLineEdit()

        layout.addWidget(QLabel("Query"))

        layout.addWidget(self.query_input)

        # limit

        self.limit = QSpinBox()
        self.limit.setValue(20)

        layout.addWidget(QLabel("Results"))

        layout.addWidget(self.limit)

        # search button

        search_btn = QPushButton("Search the on the Fucking Shoda Spirit")

        search_btn.clicked.connect(self.search)

        layout.addWidget(search_btn)

        # table results

        self.table = QTableWidget()

        layout.addWidget(self.table)

        # export 

        export_excel_btn = QPushButton("Export Excel")

        export_excel_btn.clicked.connect(self.export_excel)

        export_json_btn = QPushButton("Export JSON")

        export_json_btn.clicked.connect(self.export_json)

        layout.addWidget(export_excel_btn)

        layout.addWidget(export_json_btn)

        # filters and examples of use
        help_btn = QPushButton("Reference Guide and Examples of Use")
        help_btn.clicked.connect(self.open_filters_help)
        layout.addWidget(help_btn)

        # GIF + TEXT
        gif_container = QHBoxLayout()
        gif_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gif_label = QLabel()
        self.gif_label.setFixedSize(160, 120)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # SHADOW GIF
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 0)
        shadow.setColor(Qt.GlobalColor.black)
        self.gif_label.setGraphicsEffect(shadow)

        try:
            movie = QMovie("assets/shodan.gif")
            if movie.isValid():
                movie.setScaledSize(self.gif_label.size())
                self.gif_label.setMovie(movie)
                movie.start()
        except Exception:
            self.gif_label.setText("GIF")

        gif_text = QLabel("SpiritShoda Zero.\nA program for processing API requests to the Shodan platform.")
        gif_text.setWordWrap(True)

        gif_container.addWidget(self.gif_label)
        gif_container.addWidget(gif_text)

        layout.addLayout(gif_container)

        container = QWidget()

        container.setLayout(layout)

        self.setCentralWidget(container)


    def apply_dark_theme(self):

        self.setStyleSheet("""

        QMainWindow {background:#121212;}

        QLabel {color:white;}

        QLineEdit, QSpinBox {
            background:#1e1e1e;
            color:white;
            border:1px solid #9b59b6;
            padding:5px;
        }

        QPushButton {
            background:#8e44ad;
            color:white;
            padding:6px;
        }

        QPushButton:hover {
            background:#9b59b6;
        }

        QTableWidget {
            background:#1e1e1e;
            color:white;
        }

        """)


    def save_key(self):

        key = self.key_input.text()

        set_api_key(key)

        QMessageBox.information(self,"Loading","API key saved.")


    def search(self):

        query = self.query_input.text()

        limit = self.limit.value()

        client = ShodanClient(self.key_input.text())

        data = client.search(query,limit)

        self.data = data

        self.populate_table(data)


    def open_filters_help(self):

        help_window = FiltersHelpWindow(self)
        help_window.exec()


    def populate_table(self,data):

        if not data:
            return

        self.table.setRowCount(len(data))

        self.table.setColumnCount(len(data[0]))

        self.table.setHorizontalHeaderLabels(data[0].keys())

        for row_i,row in enumerate(data):

            for col_i,key in enumerate(row):

                self.table.setItem(row_i,col_i,QTableWidgetItem(str(row[key])))


    def export_excel(self):

        path = export_excel(self.data)

        QMessageBox.information(self,"Export","Excel saved:\n"+path)


    def export_json(self):

        path = export_json(self.data)

        QMessageBox.information(self,"Export","JSON saved:\n"+path)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ShodanGUI()

    window.show()

    sys.exit(app.exec())
