import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtWidgets import QTextEdit


class PosItApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pos-It — Automated Product Poster")
        self.setGeometry(200, 200, 400, 300)

        self.label = QLabel("📸 Upload a product image to begin")
        self.output_label = QTextEdit("\nWaiting for image...")
        self.output_label.setReadOnly(True)
        self.upload_button.clicked.connect(self.upload_image)

        self.post_button = QPushButton("Post")
        self.post_button.clicked.connect(self.post_listing)
        self.post_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.post_button)

        self.setLayout(layout)

        from services.listing_agent import process_image_and_generate_listing
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.jpeg)")
        if file_name:
            self.image_path = file_name
            try:
                self.listing_data = process_image_and_generate_listing(
                    self.image_path)
                display = "\n".join(
                    [f"{k}: {v}" for k, v in self.listing_data.items()])
                self.output_label.setText(
                    f"\n📄 Generated Listing Info:\n\n{display}")
                self.post_button.setEnabled(True)
            except Exception as e:
                self.output_label.setText(f"❌ Error: {str(e)}")
                self.post_button.setEnabled(False)

    def post_listing(self):
        from services.listing_agent import post_listing_to_all
        try:
            results = post_listing_to_all(self.listing_data, [self.image_path])
            status = "\n\n✅ Post Results:\n" + \
                "\n".join([f"{k}: {v}" for k, v in results.items()])
            self.output_label.append(status)
        except Exception as e:
            self.output_label.append(f"\n❌ Posting failed: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PosItApp()
    window.show()
    sys.exit(app.exec_())
