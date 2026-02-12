from PySide6.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect, QVBoxLayout, QFrame, QHBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QTimer, QUrl, QSize
from PySide6.QtGui import QPixmap, QDesktopServices, QColor
from qfluentwidgets import SubtitleLabel, BodyLabel, StrongBodyLabel, HyperlinkButton, PushButton, FluentIcon as FIF
from ..common.resource import get_resource_path
import math
import random
import os

class LinkSelectionWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(360, 280)
        self.setObjectName("linkSelectionWidget")
        
        # Style
        self.setStyleSheet("""
            LinkSelectionWidget {
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }
        """)
        
        # Shadow
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(20)
        self.shadowEffect.setColor(QColor(0, 0, 0, 60))
        self.shadowEffect.setOffset(0, 5)
        self.setGraphicsEffect(self.shadowEffect)
        
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.setSpacing(15)
        
        self.titleLabel = SubtitleLabel("选择访问的页面", self)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(self.titleLabel)
        
        self.vBoxLayout.addStretch(1)
        
        self.btn1 = PushButton("昔涟.cn", self)
        self.btn1.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://昔涟.cn")))
        self.vBoxLayout.addWidget(self.btn1)
        
        self.btn2 = PushButton("uwuo.cn", self)
        self.btn2.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://uwuo.cn")))
        self.vBoxLayout.addWidget(self.btn2)
        
        self.btn3 = PushButton("cyrene.cq.com", self)
        self.btn3.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://cyrene.cq.com")))
        self.vBoxLayout.addWidget(self.btn3)
        
        self.vBoxLayout.addStretch(1)
        
        self.closeLayout = QHBoxLayout()
        self.closeLayout.addStretch(1)
        self.closeBtn = PushButton("关闭", self)
        self.closeBtn.setFixedWidth(120)
        self.closeBtn.clicked.connect(self.hide)
        self.closeLayout.addWidget(self.closeBtn)
        
        self.vBoxLayout.addLayout(self.closeLayout)

class AboutInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("aboutInterface")
        
        # Gallery parameters
        self.imageCount = 6
        self.cycleLen = 4.5
        self.baseRadius = 550
        self.scrollStep = 0.05
        self.cameraZ = 0.0
        
        # Store gallery items: list of dict
        self.galleryItems = []
        
        # Directions (Vector2 equivalent)
        self.directions = [
            (-1, 0), (-0.7, -0.7), (0, -1), (0.7, -0.7),
            (1, 0), (0.7, 0.7), (0, 1), (-0.7, 0.7)
        ]
        
        self.initUI()
        self.initGallery()

    def initUI(self):
        # Container for text info to manage Z-order easily
        self.infoContainer = QWidget(self)
        self.infoContainer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False) # Allow interaction
        
        self.infoLayout = QVBoxLayout(self.infoContainer)
        self.infoLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.infoLayout.setContentsMargins(0, 0, 0, 0)
        self.infoLayout.setSpacing(10)
        
        # Avatar
        self.avatarLabel = QLabel(self)
        self.avatarLabel.setFixedSize(96, 96)
        avatarPath = get_resource_path("app/resource/images/Cyrene.png")
        if os.path.exists(avatarPath):
            self.avatarLabel.setPixmap(QPixmap(avatarPath).scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.avatarLabel.setStyleSheet("border-radius: 48px; border: 2px solid white;") 
        self.infoLayout.addWidget(self.avatarLabel)
        
        # Add some spacing
        self.infoLayout.addSpacing(10)
        
        # Title
        self.titleLabel = SubtitleLabel(self.tr('Cyrene UI'), self)
        self.infoLayout.addWidget(self.titleLabel)
        
        # Version
        self.versionLabel = BodyLabel(self.tr('Version 0.1.0'), self)
        self.infoLayout.addWidget(self.versionLabel)
        
        self.infoLayout.addSpacing(10)
        
        # Developer Info
        self.devLabel = StrongBodyLabel(self.tr('Developer: StarCyrene'), self)
        self.infoLayout.addWidget(self.devLabel)
        
        # GitHub
        self.githubBtn = HyperlinkButton(
            url='https://github.com/Cyrene2008', 
            text=self.tr('GitHub: @Cyrene2008'), 
            parent=self
        )
        # Make it bold and add shadow
        self.githubBtn.setStyleSheet("HyperlinkButton { font-weight: bold; color: #FF69B4; }") # HotPink
        githubShadow = QGraphicsDropShadowEffect(self.githubBtn)
        githubShadow.setBlurRadius(5)
        githubShadow.setColor(QColor(0, 0, 0, 50))
        githubShadow.setOffset(1, 1)
        self.githubBtn.setGraphicsEffect(githubShadow)
        self.infoLayout.addWidget(self.githubBtn)
        
        # Website Link Trigger
        self.websiteBtn = PushButton(self.tr('访问我的网站 / Visit Website'), self)
        self.websiteBtn.setFixedWidth(200)
        # Pink style
        self.websiteBtn.setStyleSheet("""
            PushButton {
                background-color: #FFB7C5;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            PushButton:hover {
                background-color: #FF9EAA;
            }
            PushButton:pressed {
                background-color: #FF8496;
            }
        """)
        self.websiteBtn.clicked.connect(self.showLinkPopup)
        self.infoLayout.addWidget(self.websiteBtn)
        
        self.infoLayout.addSpacing(20)
        
        # Copyright
        self.artLabel = BodyLabel(self.tr('Art: (C) miHoYo'), self)
        self.infoLayout.addWidget(self.artLabel)
        
        self.copyLabel = BodyLabel(self.tr('Copyright (C) 2026 StarCyrene'), self)
        self.infoLayout.addWidget(self.copyLabel)

        self.infoContainer.adjustSize()
        self.infoContainer.move(50, 50)
        
        # Link Popup Window
        self.linkPopup = LinkSelectionWidget(self)
        self.linkPopup.hide()

    def showLinkPopup(self):
        # Center the popup
        x = (self.width() - self.linkPopup.width()) // 2
        y = (self.height() - self.linkPopup.height()) // 2
        self.linkPopup.move(x, y)
        self.linkPopup.show()
        self.linkPopup.raise_()

    def initGallery(self):
        # Clear existing
        for item in self.galleryItems:
            item['widget'].deleteLater()
        self.galleryItems = []
        
        # Radial directions for Rank 1-6
        # Rank 1: Top-Left
        # Rank 2: Top
        # Rank 3: Top-Right
        # Rank 4: Bottom-Right
        # Rank 5: Bottom
        # Rank 6: Bottom-Left
        self.itemDirections = {
            1: (-0.8, -0.6), # Top-Left
            2: (0.0, -0.9),  # Top
            3: (0.8, -0.6),  # Top-Right
            4: (0.8, 0.6),   # Bottom-Right
            5: (0.0, 0.9),   # Bottom
            6: (-0.8, 0.6)   # Bottom-Left
        }
        
        # Max concurrent visible: 4
        # Total items: 6
        # To have 4 visible, visibleDuration should be > 3 * (1/6) = 0.5
        # Let's use 0.65 to ensure 4 items overlap
        self.visibleDuration = 0.65
        
        for i in range(1, self.imageCount + 1):
            # Create image label
            imgLabel = QLabel(self)
            imgLabel.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            
            # Load image
            # Reverse order: Load Rank 6 for ID 1, Rank 5 for ID 2, etc.
            # User wants Rank 6 -> 1 order (or similar reverse)
            # Map index i (1..6) to reversed rank
            rank_id = self.imageCount - i + 1 # 1->6, 2->5, ..., 6->1
            
            # Try WebP first, fallback to PNG if not found
            imgPath = get_resource_path(f"app/resource/images/1415_Rank_{rank_id}.webp")
            if not os.path.exists(imgPath):
                imgPath = get_resource_path(f"app/resource/images/1415_Rank_{rank_id}.png")
            
            if os.path.exists(imgPath):
                pixmap = QPixmap(imgPath)
                imgLabel.setPixmap(pixmap)
                imgLabel.setScaledContents(True)
            
            # Init opacity effect
            opacityEffect = QGraphicsOpacityEffect(imgLabel)
            imgLabel.setGraphicsEffect(opacityEffect)
            
            # Offset: 0, 1/6, 2/6, ...
            offset = (i - 1) * (1.0 / 6.0)
            
            # Store item
            self.galleryItems.append({
                'widget': imgLabel,
                'id': i, # Logic ID (order of appearance)
                'rank': rank_id, # Visual Rank ID
                'offset': offset,
                'effect': opacityEffect,
                'original_size': (250, 250),
                'direction': self.itemDirections.get(i, (0, 0)) # Direction based on appearance order
            })
            
            imgLabel.resize(250, 250)
            # Start hidden, updateGalleryPositions will show if needed
            imgLabel.hide()
            
        self.updateGalleryPositions()
        
        # Start auto-scroll timer
        self.galleryTimer = QTimer(self)
        self.galleryTimer.timeout.connect(self.onGalleryTimer)
        self.galleryTimer.start(16) # ~60 FPS

    def onGalleryTimer(self):
        # Auto scroll
        self.cameraZ += 0.002 # Adjust speed
        self.updateGalleryPositions()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.updateGalleryPositions()
        
        # Keep popup centered if visible
        if self.linkPopup.isVisible():
            x = (self.width() - self.linkPopup.width()) // 2
            y = (self.height() - self.linkPopup.height()) // 2
            self.linkPopup.move(x, y)

    def updateGalleryPositions(self):
        w = self.width()
        h = self.height()
        
        if w == 0 or h == 0:
            return

        cx = w / 2
        cy = h / 2
        
        # Max travel distance (approx from center to corner)
        max_dist = math.sqrt(w*w + h*h) / 2 * 0.9 # 90% to corner

        for item in self.galleryItems:
            widget = item['widget']
            offset = item['offset']
            effect = item['effect']
            base_w, base_h = item['original_size']
            direction = item['direction'] # (dx, dy) normalized-ish
            
            # Current global time position
            # We want each item to have a "life cycle" within [0, 1]
            # It is active if (global_time + offset) % 1.0 < visibleDuration
            
            loop_pos = (self.cameraZ + offset) % 1.0
            
            if loop_pos < self.visibleDuration:
                # Active
                if not widget.isVisible():
                    widget.show()
                
                # Normalized progress within the visible window [0, 1]
                t = loop_pos / self.visibleDuration
                
                # Position calculation
                # Start at Center -> Move outward along direction
                # Add some randomness or sine wave? User asked for "Sequential radial move"
                
                # Radial move
                # Distance from center
                # Start: 0
                # End: max_dist (or until fade out)
                
                # Let's scale dist by t
                current_dist = max_dist * t
                
                # Apply direction (adjust for aspect ratio if needed, but simple vector is fine)
                # direction is (dx, dy).
                # To fill screen better, let's scale dx by w/2 and dy by h/2 roughly
                # But simple vector * max_dist is more "radial"
                
                target_x = cx + direction[0] * current_dist
                target_y = cy + direction[1] * current_dist
                
                # Scale: Far (Center) -> Near (Edge)
                # User: "Appear from center (small/far?), move to edge (big/near?)"
                # Normal items: 0.5 -> 2.0 (1.5 * t)
                # Special items (Rank 2 and 5): 0.5 -> 2.5 (2.0 * t)
                
                # Check rank from item dict
                rank = item.get('rank', 0)
                if rank == 2 or rank == 5:
                    scale = 0.5 + 2.0 * t # Ends at 2.5
                else:
                    scale = 0.5 + 1.5 * t # Ends at 2.0
                
                # Opacity: Fade In (Start) -> Visible -> Fade Out (End)
                # Fade in quickly at start (center)
                # Fade out slowly at end (edge)
                
                if t < 0.2:
                    opacity = t / 0.2
                elif t > 0.7:
                    opacity = (1.0 - t) / 0.3
                else:
                    opacity = 1.0
                    
                # Apply changes
                current_w = int(base_w * scale)
                current_h = int(base_h * scale)
                widget.resize(current_w, current_h)
                
                widget.move(int(target_x - current_w / 2), int(target_y - current_h / 2))
                effect.setOpacity(opacity)
                
                # Z-Order: Smaller (further) should be behind?
                # Actually, usually "later" items are on top.
                # But here, items emerging from center (far) might be behind items near edge (near)?
                # If "Far to Near", implies Center is Far (Back), Edge is Near (Front).
                # So items with larger 't' (closer to edge) should be on top.
                # We can handle z-order by simply raising the one with largest t?
                # But we have multiple items.
                # Let's set z-order based on 't'.
                
                # We can't easily set arbitrary Z-index in Qt without restacking.
                # But since we iterate all, we can collect visible items and sort.
                
            else:
                # Inactive
                if widget.isVisible():
                    widget.hide()
                    
        # Sort visible widgets by 'scale' (or t) to ensure correct layering
        # Larger scale = Closer = On Top
        visible_items = [i for i in self.galleryItems if i['widget'].isVisible()]
        visible_items.sort(key=lambda i: i['widget'].width()) # width is proportional to scale
        
        for item in visible_items:
            item['widget'].raise_()
            
        # Ensure Info UI is on TOP of gallery
        if hasattr(self, 'infoContainer'):
            self.infoContainer.raise_()
            
        # Ensure Popup is on TOP of everything
        if hasattr(self, 'linkPopup') and self.linkPopup.isVisible():
            self.linkPopup.raise_()
