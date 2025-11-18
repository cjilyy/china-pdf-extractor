import argparse
import os
import pdfplumber
import cv2
import numpy as np
from PIL import Image

def remove_watermark(image, threshold=200):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    mask = cv2.bitwise_not(mask)
    image[mask == 0] = [255, 255, 255]
    return image

def generate_clean_pdf(input_path, output_path, resolution=200, threshold=200):
    with pdfplumber.open(input_path) as pdf:
        pages = []
        for page in pdf.pages:
            img = page.to_image(resolution=resolution).original
            img_np = np.array(img)
            clean_img = remove_watermark(img_np, threshold=threshold)
            pages.append(Image.fromarray(clean_img))
        if not pages:
            raise RuntimeError("no pages")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        pages[0].save(output_path, save_all=True, append_images=pages[1:])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="test_files/report.pdf")
    parser.add_argument("--output", default="test_files/clean.pdf")
    parser.add_argument("--resolution", type=int, default=200)
    parser.add_argument("--threshold", type=int, default=200)
    args = parser.parse_args()
    try:
        if not os.path.exists(args.input):
            raise FileNotFoundError(args.input)
        generate_clean_pdf(args.input, args.output, args.resolution, args.threshold)
        print(args.output)
    except Exception as e:
        print(f"error: {e}")
        raise

if __name__ == "__main__":
    main()