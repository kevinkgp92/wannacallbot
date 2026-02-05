from PIL import Image
import sys

def convert():
    try:
        img = Image.open("icon.png")
        img.save("icon.ico", format='ICO', sizes=[(256, 256)])
        print("Success: icon.ico created")
    except ImportError:
        print("Error: PIL/Pillow not installed")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    convert()
