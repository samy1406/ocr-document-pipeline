import cv2
from deskew import determine_skew

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    return image
    
def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
    return cv2.medianBlur(image, 3) 

def fix_contrast(image):  
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # Apply it to a grayscale image
    return clahe.apply(image)

def fix_skew(image):
    # finding the angle of skew
    angle = determine_skew(image)
    
    if angle is None:
        return image

    # get the image dimension and center for rotation
    (h,w) = image.shape[:2]
    center = (w // 2, h // 2)

    # create rotation matrix and rotate
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed = cv2.warpAffine(image, M, (w, h), 
                          flags=cv2.INTER_CUBIC, 
                          borderMode=cv2.BORDER_REPLICATE)
    
    return deskewed


def preprocess_image(image_path):
    image = load_image(image_path)

    gray_img = to_grayscale(image)

    img = remove_noise(gray_img)

    img = fix_contrast(img)

    return fix_skew(img)