import pytest
import cv2
import tkinter as tk
from unittest.mock import patch

# from send2airgap.frontend import BroadcastWindow
# from send2airgap.receiver import QRDecoder

# import send2airgap.backend as BroadcastWindow


@pytest.mark.skip(reason="just testing skip")
def disable_test_frontend_to_receiver_integration():
    # Set up the Tkinter frontend
    root = tk.Tk()
    broadcast_window = BroadcastWindow(root)

    # Simulate generating a QR code
    data_to_encode = "Test QR Data"
    broadcast_window.backend.generate_qr_code(data_to_encode)

    # Capture the QR code image (mock this for simplicity)
    qr_image = (
        "./test_qr_image.png"  # Save the generated QR to a temporary file
    )
    broadcast_window.backend.image.save(qr_image)

    # Set up the receiver with a mocked camera feed
    decoder = QRDecoder()
    with patch.object(decoder.camera, "read") as mock_read, patch.object(
        decoder.qcd, "detectAndDecode"
    ) as mock_decode:
        # Mock camera feed to use the saved QR image
        mock_read.return_value = (True, cv2.imread(qr_image))
        mock_decode.return_value = (data_to_encode, None, None)

        # Simulate reading and decoding
        frame, detected = decoder.decode_frame()

        # Assert the data was correctly decoded
        assert detected == data_to_encode

    # Clean up
    root.destroy()
