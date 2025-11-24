from pyvips import Image
from numpy.typing import NDArray
from numpy import uint8

def image_compress(image_path: str, **kwargs) -> NDArray[uint8]:
    try:
        # Additional parameters
        params = {
            'Q': kwargs.get('quality', 80),
            'compression': kwargs.get('compression', 4)
        }
        # Load image
        image = Image.new_from_file(image_path)
        # Compress image from buffer
        compress_buffer = image.pngsave_buffer(**params)
        # Load image from buffer
        compressed_image = Image.new_from_buffer(compress_buffer, '')
        # Return NDArray[uint8]
        return compressed_image.numpy()
    except Exception as e:
        print(f"Error: {e}")
        return -1
