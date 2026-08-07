"""
Captcha Service for verification.
Generates image captchas using Pillow.
"""
import io
import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class CaptchaService:
    @staticmethod
    def generate_captcha(length: int = 5) -> tuple[io.BytesIO, str]:
        """Generates a random captcha image and returns (BytesIO image, code string)."""
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
        width, height = 200, 70

        image = Image.new("RGB", (width, height), color=(47, 49, 54))
        draw = ImageDraw.Draw(image)

        # Draw noise lines
        for _ in range(8):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line([(x1, y1), (x2, y2)], fill=(88, 101, 242), width=2)

        # Draw text characters
        for i, char in enumerate(code):
            x = 25 + (i * 32)
            y = random.randint(15, 25)
            draw.text((x, y), char, fill=(255, 255, 255))

        # Add light blur effect
        image = image.filter(ImageFilter.GaussianBlur(0.4))

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        return buffer, code


captcha_service = CaptchaService()
