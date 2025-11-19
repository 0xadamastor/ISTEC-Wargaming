from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame,
    QGridLayout, QScrollArea, QFileDialog, QMessageBox,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor
import json


class WelcomeWindow(QMainWindow):
    project_selected = pyqtSignal(str, str, str)  # project_type, category, template_json

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BeatRooter - Digital Investigation Platform")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)

        # Palette - mantida próxima à original, afinada para um visual mais moderno
        self.colors = {
            'dark_bg': '#0f0f23',
            'darker_bg': '#151622',
            'darkest_bg': '#0b1020',
            'card_bg': '#171726',
            'card_hover': '#23242f',
            'accent_blue': '#2563eb',
            'accent_purple': '#7c3aed',
            'accent_red': '#dc2626',
            'text_primary': '#e6eef8',
            'text_secondary': '#9aa8bf',
            'text_muted': '#6e7a8a',
            'border': '#2b3444'
        }

        # Mantém o dicionário de templates/categorias — sem emojis, só texto
        self.project_templates = {
            "blueteam": {
                "name": "Blue Team",
                "description": "Defensive security operations and incident response",
                "color": self.colors['accent_blue'],
                "gradient": f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {self.colors['accent_blue']}, stop:1 #3b82f6)",
                "icon": "BT",
                "categories": {
                    "incident_response": {
                        "name": "Incident Response",
                        "description": "Investigate security incidents and breaches with forensic tools",
                        "icon": "IR",
                        "color": "#1e40af"
                    },
                    "threat_hunting": {
                        "name": "Threat Hunting",
                        "description": "Proactive search for threats and indicators of compromise",
                        "icon": "TH",
                        "color": "#1d4ed8"
                    },
                    "malware_analysis": {
                        "name": "Malware Analysis",
                        "description": "Analyze malicious software in isolated environments",
                        "icon": "MA",
                        "color": "#4338ca"
                    },
                    "siem_investigation": {
                        "name": "SIEM Investigation",
                        "description": "Analyze security events and logs from multiple sources",
                        "icon": "SI",
                        "color": "#3730a3"
                    }
                }
            },
            "soc_team": {
                "name": "SOC Operations",
                "description": "Security Operations Center monitoring and analysis",
                "color": self.colors['accent_purple'],
                "gradient": f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {self.colors['accent_purple']}, stop:1 #8b5cf6)",
                "icon": "SOC",
                "categories": {
                    "alert_triage": {
                        "name": "Alert Triage",
                        "description": "Prioritize and investigate security alerts",
                        "icon": "AT",
                        "color": "#5b21b6"
                    },
                    "correlation_analysis": {
                        "name": "Correlation Analysis",
                        "description": "Connect related security events across multiple data sources",
                        "icon": "CA",
                        "color": "#6d28d9"
                    },
                    "compliance_monitoring": {
                        "name": "Compliance Monitoring",
                        "description": "Monitor regulatory compliance requirements and generate reports",
                        "icon": "CM",
                        "color": "#5b21b6"
                    }
                }
            },
            "redteam": {
                "name": "Red Team",
                "description": "Offensive security testing and penetration testing",
                "color": self.colors['accent_red'],
                "gradient": f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {self.colors['accent_red']}, stop:1 #ef4444)",
                "icon": "RT",
                "categories": {
                    "web_pentesting": {
                        "name": "Web Application Testing",
                        "description": "Web application security assessment and penetration testing",
                        "icon": "WP",
                        "color": "#991b1b"
                    },
                    "network_pentesting": {
                        "name": "Network Assessment",
                        "description": "Network infrastructure security evaluation",
                        "icon": "NA",
                        "color": "#b91c1c"
                    },
                    "social_engineering": {
                        "name": "Social Engineering",
                        "description": "Human factor security controls assessment",
                        "icon": "SE",
                        "color": "#b91c1c"
                    }
                }
            }
        }

        self.setup_ui()
        self.setup_animations()

    def start_project(self, project_type, category):
        template_data = {
            'project_type': project_type,
            'category': category,
            'template': f"{project_type}_{category}",
            'metadata': {
                'title': f"{self.project_templates[project_type]['name']} - {self.project_templates[project_type]['categories'][category]['name']}",
                'created': '',
                'template': f"{project_type}_{category}"
            }
        }
        self.project_selected.emit(project_type, category, json.dumps(template_data))
        self.close()

    # ---------------- UI BUILD ----------------
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = self.create_header()
        main_layout.addWidget(header)

        self.stacked_widget = QStackedWidget()

        self.welcome_screen = self.create_welcome_screen()
        self.project_type_screen = self.create_project_type_screen()
        self.category_screen = self.create_category_screen()

        self.stacked_widget.addWidget(self.welcome_screen)
        self.stacked_widget.addWidget(self.project_type_screen)
        self.stacked_widget.addWidget(self.category_screen)
        self.apply_cyber_modern_style()

        main_layout.addWidget(self.stacked_widget, 1)

        footer = self.create_footer()
        main_layout.addWidget(footer)

    def apply_cyber_modern_style(self):
        """Aplica o estilo cyber modern alinhado com o programa principal"""
        style = f"""
        /* ========== GLOBAL ========== */
        QWidget {{
            background-color: {self.colors['dark_bg']};
            color: {self.colors['text_primary']};
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            font-size: 13px;
        }}
        
        QMainWindow {{
            background-color: {self.colors['darkest_bg']};
        }}
        
        /* ========== HEADER ========== */
        QFrame {{
            background: transparent;
        }}
        
        /* Logo minimalista */
        QLabel[text="BR"] {{
            background-color: {self.colors['accent_blue']};
            color: white;
            font-size: 22px;
            font-weight: 700;
            border-radius: 8px;
        }}
        
        /* Títulos */
        QLabel[text="BEATROOTER"] {{
            color: {self.colors['text_primary']};
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 1px;
        }}
        
        QLabel[text="DIGITAL INVESTIGATION PLATFORM"] {{
            color: {self.colors['text_secondary']};
            font-size: 9px;
            font-weight: 600;
            letter-spacing: 2px;
        }}
        
        /* Versão */
        QLabel[text="v1.0.0"] {{
            color: {self.colors['text_muted']};
            font-size: 11px;
            font-family: 'Courier New', monospace;
            background-color: {self.colors['card_bg']};
            padding: 6px 12px;
            border-radius: 4px;
            border: 1px solid {self.colors['border']};
        }}
        
        /* ========== WELCOME SCREEN ========== */
        QLabel[text="Welcome to BeatRooter"] {{
            color: {self.colors['text_primary']};
            font-size: 38px;
            font-weight: 700;
        }}
        
        QLabel[text="Professional digital forensic and security analysis platform"] {{
            color: {self.colors['text_secondary']};
            font-size: 15px;
            font-weight: 500;
        }}
        
        QLabel[text="Advanced tools for comprehensive digital forensics, incident response and security analysis."] {{
            color: {self.colors['text_muted']};
            font-size: 13px;
        }}
        
        /* ========== CARDS ========== */
        QFrame[objectName*="card"] {{
            background-color: {self.colors['card_bg']};
            border: 1px solid {self.colors['border']};
            border-radius: 12px;
        }}
        
        QFrame[objectName*="card"]:hover {{
            background-color: {self.colors['card_hover']};
            border: 1px solid {self.colors['text_muted']};
        }}
        
        /* Card Icons */
        QLabel[objectName="card_icon"] {{
            background-color: rgba(255, 255, 255, 0.05);
            color: {self.colors['text_primary']};
            font-size: 24px;
            font-weight: 700;
            border-radius: 8px;
            border: 1px solid {self.colors['border']};
        }}
        
        /* Card Titles */
        QLabel[text="New Investigation"],
        QLabel[text="Open Project"],
        QLabel[text="API & Integrations"] {{
            color: {self.colors['text_primary']};
            font-size: 18px;
            font-weight: 600;
        }}
        
        /* ========== PROJECT TYPE CARDS - CORES ESPECÍFICAS ========== */
        
        /* Blue Team */
        QFrame[objectName="blueteam_card"] {{
            background-color: {self.colors['card_bg']};
            border-left: 3px solid {self.colors['accent_blue']};
            border-right: 1px solid {self.colors['border']};
            border-top: 1px solid {self.colors['border']};
            border-bottom: 1px solid {self.colors['border']};
            border-radius: 12px;
        }}
        
        QFrame[objectName="blueteam_card"]:hover {{
            background-color: {self.colors['card_hover']};
            border-left: 3px solid {self.colors['accent_blue']};
        }}
        
        QFrame[objectName="blueteam_card"] QLabel[objectName="card_header"] {{
            background-color: {self.colors['accent_blue']};
            border-radius: 8px;
        }}
        
        QFrame[objectName="blueteam_card"] QPushButton {{
            background-color: {self.colors['accent_blue']};
            color: white;
        }}
        
        QFrame[objectName="blueteam_card"] QPushButton:hover {{
            background-color: #3b82f6;
        }}
        
        /* SOC Team */
        QFrame[objectName="soc_team_card"] {{
            background-color: {self.colors['card_bg']};
            border-left: 3px solid {self.colors['accent_purple']};
            border-right: 1px solid {self.colors['border']};
            border-top: 1px solid {self.colors['border']};
            border-bottom: 1px solid {self.colors['border']};
            border-radius: 12px;
        }}
        
        QFrame[objectName="soc_team_card"]:hover {{
            background-color: {self.colors['card_hover']};
            border-left: 3px solid {self.colors['accent_purple']};
        }}
        
        QFrame[objectName="soc_team_card"] QLabel[objectName="card_header"] {{
            background-color: {self.colors['accent_purple']};
            border-radius: 8px;
        }}
        
        QFrame[objectName="soc_team_card"] QPushButton {{
            background-color: {self.colors['accent_purple']};
            color: white;
        }}
        
        QFrame[objectName="soc_team_card"] QPushButton:hover {{
            background-color: #8b5cf6;
        }}
        
        /* Red Team */
        QFrame[objectName="redteam_card"] {{
            background-color: {self.colors['card_bg']};
            border-left: 3px solid {self.colors['accent_red']};
            border-right: 1px solid {self.colors['border']};
            border-top: 1px solid {self.colors['border']};
            border-bottom: 1px solid {self.colors['border']};
            border-radius: 12px;
        }}
        
        QFrame[objectName="redteam_card"]:hover {{
            background-color: {self.colors['card_hover']};
            border-left: 3px solid {self.colors['accent_red']};
        }}
        
        QFrame[objectName="redteam_card"] QLabel[objectName="card_header"] {{
            background-color: {self.colors['accent_red']};
            border-radius: 8px;
        }}
        
        QFrame[objectName="redteam_card"] QPushButton {{
            background-color: {self.colors['accent_red']};
            color: white;
        }}
        
        QFrame[objectName="redteam_card"] QPushButton:hover {{
            background-color: #ef4444;
        }}
        
        /* ========== TEAM HEADERS ========== */
        QLabel[text="Blue Team"],
        QLabel[text="SOC Operations"],
        QLabel[text="Red Team"] {{
            color: white;
            font-size: 18px;
            font-weight: 600;
        }}
        
        /* Team Icons */
        QLabel[text="BT"],
        QLabel[text="SOC"],
        QLabel[text="RT"] {{
            background-color: rgba(255, 255, 255, 0.15);
            color: white;
            font-size: 16px;
            font-weight: 700;
            border-radius: 6px;
            padding: 8px;
        }}
        
        /* Category Icons - Blue Team */
        QLabel[text="IR"],
        QLabel[text="TH"],
        QLabel[text="MA"],
        QLabel[text="SI"] {{
            background-color: rgba(37, 99, 235, 0.15);
            color: {self.colors['accent_blue']};
            font-size: 10px;
            font-weight: 700;
            border-radius: 4px;
            padding: 4px 8px;
            border: 1px solid {self.colors['accent_blue']};
        }}
        
        /* Category Icons - SOC Team */
        QLabel[text="AT"],
        QLabel[text="CA"],
        QLabel[text="CM"] {{
            background-color: rgba(124, 58, 237, 0.15);
            color: {self.colors['accent_purple']};
            font-size: 10px;
            font-weight: 700;
            border-radius: 4px;
            padding: 4px 8px;
            border: 1px solid {self.colors['accent_purple']};
        }}
        
        /* Category Icons - Red Team */
        QLabel[text="WP"],
        QLabel[text="NA"],
        QLabel[text="SE"] {{
            background-color: rgba(220, 38, 38, 0.15);
            color: {self.colors['accent_red']};
            font-size: 10px;
            font-weight: 700;
            border-radius: 4px;
            padding: 4px 8px;
            border: 1px solid {self.colors['accent_red']};
        }}
        
        /* ========== BUTTONS ========== */
        QPushButton {{
            background-color: {self.colors['accent_blue']};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 13px;
            font-weight: 600;
        }}
        
        QPushButton:hover {{
            background-color: #3b82f6;
        }}
        
        QPushButton:pressed {{
            background-color: #1e40af;
        }}
        
        QPushButton:disabled {{
            background-color: {self.colors['card_bg']};
            color: {self.colors['text_muted']};
            border: 1px solid {self.colors['border']};
        }}
        
        /* Back Buttons */
        QPushButton[text*="Back"],
        QPushButton[text*="←"] {{
            background-color: transparent;
            color: {self.colors['text_secondary']};
            border: 1px solid {self.colors['border']};
        }}
        
        QPushButton[text*="Back"]:hover,
        QPushButton[text*="←"]:hover {{
            background-color: {self.colors['card_bg']};
            color: {self.colors['text_primary']};
            border: 1px solid {self.colors['text_muted']};
        }}
        
        /* ========== HEADERS E SUBTÍTULOS ========== */
        QLabel[text="Select Investigation Type"],
        QLabel[text*="Choose"] {{
            color: {self.colors['text_primary']};
            font-size: 26px;
            font-weight: 700;
        }}
        
        QLabel[text="Choose the specialized workflow for your analysis"],
        QLabel[text*="Select the specific investigation"] {{
            color: {self.colors['text_secondary']};
            font-size: 14px;
        }}
        
        QLabel[text="Available Specializations:"] {{
            color: {self.colors['text_secondary']};
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* ========== SCROLL AREAS ========== */
        QScrollArea {{
            border: none;
            background: transparent;
        }}
        
        QScrollBar:vertical {{
            background-color: {self.colors['darker_bg']};
            width: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {self.colors['card_bg']};
            border-radius: 5px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {self.colors['text_muted']};
        }}
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background-color: {self.colors['darker_bg']};
            height: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {self.colors['card_bg']};
            border-radius: 5px;
            min-width: 30px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {self.colors['text_muted']};
        }}
        
        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        /* ========== FOOTER ========== */
        QFrame[objectName="footer"] {{
            background-color: {self.colors['darker_bg']};
            border-top: 1px solid {self.colors['border']};
        }}
        
        QFrame[objectName="footer"] QLabel {{
            color: {self.colors['text_muted']};
            font-size: 11px;
        }}
        
        /* ========== STACKED WIDGET ========== */
        QStackedWidget {{
            background: transparent;
        }}
        """
        self.setStyleSheet(style)

    # ---------------- HEADER ----------------
    def create_header(self):
        header = QFrame()
        header.setFixedHeight(76)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 140))
        shadow.setOffset(0, 3)
        header.setGraphicsEffect(shadow)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(36, 8, 36, 8)

        # Logo simplificado - apenas o texto
        logo_label = QLabel("BR")
        logo_label.setFixedSize(56, 56)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_layout = QVBoxLayout()
        title = QLabel("BEATROOTER")
        subtitle = QLabel("DIGITAL INVESTIGATION PLATFORM")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        layout.addWidget(logo_label)
        layout.addSpacing(12)
        layout.addLayout(title_layout)
        layout.addStretch()

        # Versão sem frame
        v_label = QLabel("v1.0.0")
        layout.addWidget(v_label)

        return header

    # ---------------- WELCOME SCREEN ----------------
    def create_welcome_screen(self):
        screen = QWidget()

        layout = QVBoxLayout(screen)
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(48)

        # Welcome area - texto direto sem frames
        welcome_layout = QVBoxLayout()
        welcome_layout.setSpacing(18)

        welcome_title = QLabel("Welcome to BeatRooter")
        welcome_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        welcome_sub = QLabel("Professional digital forensic and security analysis platform")
        welcome_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        welcome_desc = QLabel("Advanced tools for comprehensive digital forensics, incident response and security analysis.")
        welcome_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_desc.setWordWrap(True)

        welcome_layout.addStretch(1)
        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_sub)
        welcome_layout.addWidget(welcome_desc)
        welcome_layout.addStretch(1)

        # Options area (cards)
        options_layout = QHBoxLayout()
        options_layout.setSpacing(28)
        options_layout.setContentsMargins(40, 0, 40, 20)

        new_card = self.create_option_card(
            title="New Investigation",
            description="Start a new digital forensic investigation with specialized templates and workflows.",
            button_text="Begin Analysis",
            callback=self.show_project_type_selection,
            color=self.colors['accent_blue'],
            enabled=True
        )

        open_card = self.create_option_card(
            title="Open Project",
            description="Continue working on an existing investigation file with full context restoration.",
            button_text="Open File",
            callback=self.import_existing_project,
            color=self.colors['accent_purple'],
            enabled=True
        )

        api_card = self.create_option_card(
            title="API & Integrations",
            description="Connect to external data sources and automation tools (coming soon).",
            button_text="Coming Soon",
            callback=self.show_api_development,
            color=self.colors['accent_red'],
            enabled=False
        )

        options_layout.addStretch()
        options_layout.addWidget(new_card)
        options_layout.addWidget(open_card)
        options_layout.addWidget(api_card)
        options_layout.addStretch()

        layout.addLayout(welcome_layout, 2)
        layout.addLayout(options_layout, 3)

        return screen

    def create_option_card(self, title, description, button_text, callback, color, enabled=True):
        card = QFrame()
        card.setFixedSize(340, 380)
        card.setCursor(Qt.CursorShape.PointingHandCursor if enabled else Qt.CursorShape.ArrowCursor)

        border_color = self.colors['border'] if enabled else self.colors['border']
        hover_extra = f"border: 1px solid {color}; background: {self.colors['card_hover']};" if enabled else ""

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(22)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 100))
        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 26, 22, 22)
        layout.setSpacing(14)

        # Ícone - apenas texto com estilo
        icon_label = QLabel(title.split()[0][:2].upper())
        icon_label.setFixedSize(64, 64)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setWordWrap(True)

        desc_label = QLabel(description)
        desc_label.setWordWrap(True)

        btn = QPushButton(button_text)
        btn.setFixedHeight(46)
        if enabled:
            btn.clicked.connect(callback)
        else:
            btn.setEnabled(False)

        layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addWidget(btn)

        return card

    # ---------------- PROJECT TYPE SCREEN ----------------
    def create_project_type_screen(self):
        screen = QWidget()

        layout = QVBoxLayout(screen)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(20)

        # Header - texto direto
        header_layout = QVBoxLayout()
        header_label = QLabel("Select Investigation Type")
        header_sub = QLabel("Choose the specialized workflow for your analysis")
        header_layout.addWidget(header_label)
        header_layout.addWidget(header_sub)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        h_layout = QHBoxLayout(container)
        h_layout.setSpacing(26)
        h_layout.setContentsMargins(12, 12, 12, 12)

        for project_type, config in self.project_templates.items():
            card = self.create_project_type_card(project_type, config)
            h_layout.addWidget(card)

        scroll.setWidget(container)

        back_button = QPushButton("← Back to Welcome Screen")
        back_button.setFixedHeight(44)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        layout.addLayout(header_layout)
        layout.addWidget(scroll, 1)
        layout.addWidget(back_button)

        return screen

    def create_project_type_card(self, project_type, config):
        card = QFrame()
        card.setFixedSize(360, 500)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 90))
        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        # Header do card - apenas gradiente com texto
        header_label = QLabel()
        header_label.setFixedHeight(140)
        header_layout = QVBoxLayout(header_label)
        header_layout.setContentsMargins(16, 12, 16, 12)

        top_layout = QHBoxLayout()
        icon = QLabel(config['icon'])
        title = QLabel(config['name'])
        top_layout.addWidget(icon)
        top_layout.addSpacing(12)
        top_layout.addWidget(title)
        top_layout.addStretch()

        desc = QLabel(config['description'])
        desc.setWordWrap(True)

        header_layout.addLayout(top_layout)
        header_layout.addWidget(desc)

        categories_label = QLabel("Available Specializations:")

        categories_layout = QVBoxLayout()
        categories_layout.setSpacing(10)

        for cat_id, cat_conf in config['categories'].items():
            # Categorias - apenas texto sem frames
            cat_layout = QHBoxLayout()
            cat_icon = QLabel(cat_conf['icon'])
            cat_name = QLabel(cat_conf['name'])

            cat_layout.addWidget(cat_icon)
            cat_layout.addSpacing(10)
            cat_layout.addWidget(cat_name)
            cat_layout.addStretch()

            categories_layout.addLayout(cat_layout)

        select_button = QPushButton(f"Start {config['name']} Analysis")
        select_button.setFixedHeight(48)
        select_button.clicked.connect(lambda _=None, pt=project_type: self.show_category_selection(pt))

        layout.addWidget(header_label)
        layout.addWidget(categories_label)
        layout.addLayout(categories_layout)
        layout.addStretch()
        layout.addWidget(select_button)

        return card

    # ---------------- CATEGORY SCREEN ----------------
    def create_category_screen(self):
        screen = QWidget()
        self.category_layout = QVBoxLayout(screen)
        self.category_layout.setContentsMargins(36, 28, 36, 28)
        self.category_layout.setSpacing(18)
        return screen

    def update_category_screen(self, project_type):
        # Clear previous content completely
        while self.category_layout.count():
            item = self.category_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # Recursively clear nested layouts
                self.clear_layout(item.layout())

        config = self.project_templates[project_type]

        # Header - texto direto
        header_layout = QVBoxLayout()
        title = QLabel(f"Choose {config['name']} Specialization")
        subtitle = QLabel("Select the specific investigation workflow that matches your requirements")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        grid_area = QScrollArea()
        grid_area.setWidgetResizable(True)
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(20)
        grid.setContentsMargins(12, 12, 12, 12)

        row, col = 0, 0
        max_cols = 2
        for cat_id, cat_conf in config['categories'].items():
            card = self.create_category_card(project_type, cat_id, cat_conf)
            grid.addWidget(card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        grid_area.setWidget(grid_widget)

        back_button = QPushButton("← Back to Investigation Types")
        back_button.setFixedHeight(44)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.category_layout.addLayout(header_layout)
        self.category_layout.addWidget(grid_area, 1)
        self.category_layout.addWidget(back_button)

    def clear_layout(self, layout):
        """Helper method to recursively clear a layout"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def create_category_card(self, project_type, category_id, config):
        project_color = self.project_templates[project_type]['color']
        card = QFrame()
        card.setFixedHeight(220)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        top = QHBoxLayout()
        # Ícone - apenas texto com estilo
        icon_label = QLabel(config['icon'])
        icon_label.setFixedSize(46, 46)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        name = QLabel(config['name'])

        top.addWidget(icon_label)
        top.addSpacing(12)
        top.addWidget(name)
        top.addStretch()

        desc = QLabel(config['description'])
        desc.setWordWrap(True)

        start_btn = QPushButton("Begin Analysis")
        start_btn.setFixedHeight(44)
        start_btn.clicked.connect(lambda _=None, pt=project_type, cat=category_id: self.start_project(pt, cat))

        layout.addLayout(top)
        layout.addWidget(desc)
        layout.addStretch()
        layout.addWidget(start_btn)

        return card

    # ---------------- FOOTER ----------------
    def create_footer(self):
        footer = QFrame()
        footer.setFixedHeight(60)

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(36, 12, 36, 12)

        copyright = QLabel("© 2024 BeatRooter - Advanced Digital Investigation Platform")

        layout.addWidget(copyright)
        layout.addStretch()

        return footer

    # ---------------- ANIMATIONS ----------------
    def setup_animations(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(380)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

    # ---------------- HELPERS ----------------
    def lighten_color(self, hex_color, amount=18):
        try:
            r = min(255, int(hex_color[1:3], 16) + amount)
            g = min(255, int(hex_color[3:5], 16) + amount)
            b = min(255, int(hex_color[5:7], 16) + amount)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return hex_color

    def darken_color(self, hex_color, amount=18):
        try:
            r = max(0, int(hex_color[1:3], 16) - amount)
            g = max(0, int(hex_color[3:5], 16) - amount)
            b = max(0, int(hex_color[5:7], 16) - amount)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return hex_color

    # ---------------- NAVIGATION / ACTIONS ----------------
    def show_project_type_selection(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_category_selection(self, project_type):
        self.current_project_type = project_type
        self.update_category_screen(project_type)
        self.stacked_widget.setCurrentIndex(2)

    def start_project(self, project_type, category):
        template_data = {
            'project_type': project_type,
            'category': category,
            'template': f"{project_type}_{category}",
            'metadata': {
                'title': f"{self.project_templates[project_type]['name']} - {self.project_templates[project_type]['categories'][category]['name']}",
                'created': '',
                'template': f"{project_type}_{category}"
            }
        }
        self.project_selected.emit(project_type, category, json.dumps(template_data))
        self.close()

    def import_existing_project(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open Investigation', '',
            'BeatRooter Tree Files (*.brt);;JSON Files (*.json);;All Files (*)'
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    project_data = json.load(f)

                self.project_selected.emit('imported', 'existing', json.dumps({
                    'file_path': filename,
                    'project_data': project_data
                }))
                self.close()

            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Failed to import project: {e}")

    def show_api_development(self):
        QMessageBox.information(self, "API Integration",
                                "API Integration features are currently under development."
                                "This feature will allow you to connect BeatRooter with external threat intelligence feeds, SIEM systems and automation platforms."
                                "Coming in a future update.")