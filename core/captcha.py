import base64
import time
import requests
import re
try:
    import ddddocr
except ImportError:
    ddddocr = None

class LocalCaptchaSolver:
    """A helper to solve simple image-to-text captchas using local logic or external API."""
    def __init__(self, api_key=None):
        self.api_key = api_key # For 2Captcha/CapMonster fallback
        self.ocr = None
        if ddddocr:
            try:
                self.ocr = ddddocr.DdddOcr(show_ad=False)
            except Exception as e:
                print(f"⚠️ Error al inicializar ddddocr: {e}")

    def solve_image(self, screenshot_base64):
        """
        Solves image-to-text captchas using ddddocr.
        Accepts base64 encoded image string or bytes.
        """
        if not self.ocr:
            print("WARN: OCR no disponible. Usando valor de prueba.")
            return "1234"

        try:
            if isinstance(screenshot_base64, str):
                # Remove header if present (data:image/png;base64,...)
                if "," in screenshot_base64:
                    screenshot_base64 = screenshot_base64.split(",")[1]
                image_bytes = base64.b64decode(screenshot_base64)
            else:
                image_bytes = screenshot_base64

            result = self.ocr.classification(image_bytes)
            print(f"ℹ️ Captcha resuelto: {result}")
            return result
        except Exception as e:
            print(f"❌ Error en OCR: {e}")
            return "1234"

    def solve_math(self, text):
        """
        Attempts to solve simple math captchas (e.g. '5 + 3 = ?')
        """
        try:
            # Clean text
            clean_text = text.replace("=", "").replace("?", "").strip()
            # Simple regex to find numbers and operators
            match = re.search(r'(\d+)\s*([\+\-\*\/])\s*(\d+)', clean_text)
            if match:
                a, op, b = match.groups()
                result = eval(f"{a} {op} {b}")
                print(f"ℹ️ Captcha matemático resuelto: {a} {op} {b} = {result}")
                return str(int(result))
        except:
            pass
        return text

    def solve_recaptcha(self, sitekey, url):
        """Solves ReCaptcha via API if key is provided."""
        if not self.api_key:
            return None
        # Logic for 2Captcha/CapMonster would go here
        return "mock_token"
