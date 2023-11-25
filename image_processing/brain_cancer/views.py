from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render
import cv2
import numpy as np
from PIL import Image
import imghdr
import os
from django.http import HttpResponseBadRequest


def is_valid_image(file):
    image_type = imghdr.what(file)
    return image_type in ['jpeg', 'png', 'gif'] if image_type else False


allowed_filters = [
    'blur_averaging', 'blur_gaussian', 'blur_median', 'blur_bilateral',
    'blur_custom', 'edge', 'enhance', 'sharpen', 'sobel', 'threshold'
]


def apply_blur_averaging(img):
    return cv2.blur(img, (11, 11))


def apply_blur_gaussian(img):
    return cv2.GaussianBlur(img, (7, 7), 2)


def apply_blur_median(img):
    return cv2.medianBlur(img, 5)


def apply_blur_bilateral(img):
    return cv2.bilateralFilter(img, 9, 75, 75)


def custom_blur_function(image):
    kernel = np.ones((5, 5), np.float32) / 25
    return cv2.filter2D(image, -1, kernel)


def apply_edge_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, 100, 200)


def apply_image_enhancement(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.equalizeHist(v)
    final_hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)


def apply_sharpening(img):
    sharp_filter = np.array([[-1, -1, -1],
                             [-1, 9, -1],
                             [-1, -1, -1]])
    return cv2.filter2D(img, -1, sharp_filter)


def apply_sobel(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel_combined = cv2.addWeighted(cv2.convertScaleAbs(
        sobelx), 0.5, cv2.convertScaleAbs(sobely), 0.5, 0)
    return sobel_combined


def apply_threshold(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY)
    return thresh


def apply_filter(image, filter_type):
    if filter_type not in allowed_filters:
        return None

    img_array = np.frombuffer(image.read(), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)

    if filter_type == 'blur_averaging':
        return apply_blur_averaging(img)
    elif filter_type == 'blur_gaussian':
        return apply_blur_gaussian(img)
    elif filter_type == 'blur_median':
        return apply_blur_median(img)
    elif filter_type == 'blur_bilateral':
        return apply_blur_bilateral(img)
    elif filter_type == 'blur_custom':
        return custom_blur_function(img)
    elif filter_type == 'edge':
        return apply_edge_detection(img)
    elif filter_type == 'enhance':
        return apply_image_enhancement(img)
    elif filter_type == 'sharpen':
        return apply_sharpening(img)
    elif filter_type == 'sobel':
        return apply_sobel(img)
    elif filter_type == 'threshold':
        return apply_threshold(img)
    else:
        return None


def process_image(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image = request.FILES['image']

            if not is_valid_image(image):
                return render(request, 'home.html', {'error': 'Invalid or unsupported image format.'})

            filter_choice = request.POST.get('filter_choice')

            filtered_image = apply_filter(image, filter_choice)

            if filtered_image is None:
                return render(request, 'home.html', {'error': 'Invalid filter choice or filter application failed.'})

            _, filename = os.path.split(image.name)
            filtered_filename = 'filtered_' + filename

            # تحويل الصورة المُعالَجة إلى بيانات قابلة للتخزين بتنسيق JPEG
            success, encoded_image = cv2.imencode(".jpg", filtered_image)

            if not success:
                return render(request, 'home.html', {'error': 'Failed to encode the image.'})

            # حفظ الصورة المعالجة في وسيلة التخزين الافتراضية
            with default_storage.open(filtered_filename, 'wb') as f:
                f.write(encoded_image.tobytes())

            file_url = default_storage.url(filtered_filename)

            return render(request, 'home.html', {
                'uploaded_file_url': file_url
            })

    return HttpResponseBadRequest('Invalid request')
