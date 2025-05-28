import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog


class PosItApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pos-It — Automated Product Poster")
        self.setGeometry(200, 200, 400, 300)

        self.label = QLabel("📸 Upload a product image to begin")
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)

        self.output_label = QLabel("\nWaiting for image...")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.output_label)

        self.setLayout(layout)

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.jpeg)")
        from services.image_search import reverse_image_search
        from services.chatgpt_client import ChatGPTClient

        context = reverse_image_search(file_name)
        chatgpt = ChatGPTClient()
        try:
            result_json = chatgpt.generate_listing_info(context)
            self.output_label.setText(
                f"\n📄 Generated Listing Info:\n\n{result_json}")
        except Exception as e:
            self.output_label.setText(f"❌ GPT error: {str(e)}")
            # TODO: Display generated title/price/description


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PosItApp()
    window.show()
    sys.exit(app.exec_())
