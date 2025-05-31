import sys
from log.logger import log_event, log_error
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit


class PosItApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pos-It — Automated Product Poster")
        self.setGeometry(200, 200, 400, 400)

        self.label = QLabel("📸 Upload a product image to begin")
        self.output_label = QTextEdit("\nWaiting for image...")
        self.output_label.setReadOnly(True)

        self.image_preview = QLabel("[ No Image Loaded ]")
        self.image_preview.setFixedHeight(150)
        self.image_preview.setScaledContents(True)

        self.thumb_layout = QHBoxLayout()
        self.upload_button = QPushButton("Upload Images")
        self.upload_button.clicked.connect(self.upload_image)

        self.post_button = QPushButton("Post")
        self.post_button.clicked.connect(self.post_listing)
        self.post_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_button)
        layout.addLayout(self.thumb_layout)
        layout.addWidget(self.image_preview)
        layout.addWidget(self.output_label)
        layout.addWidget(self.post_button)
        self.setLayout(layout)

    def upload_image(self):
        from services.listing_agent import process_image_and_generate_listing
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "", "Images (*.png *.xpm *.jpg *.jpeg)")
        if files:
            self.image_paths = files
            log_event(f"Uploaded {len(files)} images")
            self.load_thumbnails()
            self.update_image_preview(files[0])
            try:
                self.listing_data = process_image_and_generate_listing(
                    files[0])
                log_event("Listing generated from main image")
                display = "\n".join([
                    f"{k}: {v}" for k, v in self.listing_data.items()])
                self.output_label.setText(
                    f"\n📄 Generated Listing Info:\n\n{display}")
                self.post_button.setEnabled(True)
            except Exception as e:
                self.output_label.setText(f"❌ Error: {str(e)}")
                log_error(f"Listing generation failed: {str(e)}")
                self.post_button.setEnabled(False)

    def load_thumbnails(self):
        while self.thumb_layout.count():
            item = self.thumb_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        for idx, path in enumerate(self.image_paths):
            thumb_container = QVBoxLayout()

            label = QLabel()
            label.setPixmap(QPixmap(path).scaled(75, 75))
            thumb_container.addWidget(label)

            up_button = QPushButton("↑")
            up_button.clicked.connect(lambda _, i=idx: self.move_image(i, -1))
            thumb_container.addWidget(up_button)

            down_button = QPushButton("↓")
            down_button.clicked.connect(lambda _, i=idx: self.move_image(i, 1))
            thumb_container.addWidget(down_button)

            wrapper = QWidget()
            wrapper.setLayout(thumb_container)
            self.thumb_layout.addWidget(wrapper)

        self.update_image_preview(self.image_paths[0])
        self.process_main_image()

    def move_image(self, index, direction):
        new_index = index + direction
        if 0 <= new_index < len(self.image_paths):
            self.image_paths[index], self.image_paths[new_index] = self.image_paths[new_index], self.image_paths[index]
            self.load_thumbnails()

    def process_main_image(self):
        from services.listing_agent import process_image_and_generate_listing
        try:
            self.listing_data = process_image_and_generate_listing(
                self.image_paths[0])
            log_event("Listing regenerated after image reorder")
            display = "\n".join([
                f"{k}: {v}" for k, v in self.listing_data.items()])
            self.output_label.setText(
                f"\n📄 Generated Listing Info:\n\n{display}")
            self.post_button.setEnabled(True)
        except Exception as e:
            self.output_label.setText(f"❌ Error: {str(e)}")
            log_error(f"Listing regeneration failed: {str(e)}")
            self.post_button.setEnabled(False)

    def post_listing(self):
        from services.listing_agent import post_listing_to_all
        try:
            results = post_listing_to_all(self.listing_data, self.image_paths)
            log_event("Posted listing to all platforms")
            status = "\n\n✅ Post Results:\n" + "\n".join([
                f"{k}: {v}" for k, v in results.items()])
            self.output_label.append(status)
        except Exception as e:
            self.output_label.append(f"\n❌ Posting failed: {str(e)}")
            log_error(f"Posting failed: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PosItApp()
    window.show()
    sys.exit(app.exec_())
