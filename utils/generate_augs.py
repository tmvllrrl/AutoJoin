'''
    Perturbation code adapted from Yu Shen's GitHub: Multi_Perturbation_Robustness
'''

from __future__ import print_function
 
import cv2 # Import the OpenCV library
import numpy as np # Import Numpy library
import matplotlib.pyplot as plt # Import matplotlib functionality
import random

RGB_MAX = 255
HSV_H_MAX = 180
HSV_SV_MAX = 255
YUV_MAX = 255

# level values
BLUR_LVL = [7, 17, 37, 67, 107]
NOISE_LVL = [20, 50, 100, 150, 200]
DIST_LVL = [1, 10, 50, 200, 500]
RGB_LVL = [0.02, 0.2, 0.5, 0.65]

IMG_WIDTH = 200
IMG_HEIGHT = 66

KSIZE_MIN = 0.1
KSIZE_MAX = 3.8
NOISE_MIN = 0.1
NOISE_MAX = 4.6
DISTORT_MIN = -2.30258509299
DISTORT_MAX = 5.3
COLOR_SCALE = 0.25

def add_noise(image, sigma):
    row,col,ch= image.shape
    mean = 0
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    noisy = image + gauss
    noisy = np.float32(noisy)
    return noisy

def generate_noise_image(image, noise_level=20):

    image = add_noise(image, noise_level)
    image = np.moveaxis(image, -1, 0)

    return image

def perturb_noise(image, dist_ratio):
    noise_level = int(dist_ratio * (200 - 20) + 20)
    return generate_noise_image(image, noise_level)

def generate_blur_image(image, blur_level=7):
    
    image = cv2.GaussianBlur(image, (blur_level, blur_level), 0)
    image = np.moveaxis(image, -1, 0)

    return image

def perturb_blur(image, dist_ratio):
    blur_level = int(dist_ratio * (107 - 7) + 7)
    if blur_level % 2 == 0: # blur has to be an odd number
        blur_level += 1
    
    return generate_blur_image(image, blur_level)

def generate_distort_image(image, distort_level=1):
     
    K = np.eye(3)*1000
    K[0,2] = image.shape[1]/2
    K[1,2] = image.shape[0]/2
    K[2,2] = 1

    image = cv2.undistort(image, K, np.array([distort_level,distort_level,0,0]))
    # image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    image = np.moveaxis(image, -1, 0)

    return image

def perturb_distort(image, dist_ratio):
    distort_level = int(dist_ratio * (500 - 1) + 1)
    return generate_distort_image(image, distort_level)


def generate_RGB_image(image, channel, direction, dist_ratio=0.25):

    color_str_dic = {
        0: "R",
        1: "G", 
        2: "B"
    }
                   
    if direction == 4: # lower the channel value
        image[:, :, channel] = (image[:, :, channel] * (1-dist_ratio)) + (0 * dist_ratio)
    else: # raise the channel value
        image[:, :, channel] = (image[:, :, channel] * (1-dist_ratio)) + (RGB_MAX * dist_ratio)

    # added nov 10
    # image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    image = np.moveaxis(image, -1, 0)

    return image

def perturb_r(image, dist_ratio):
    return generate_RGB_image(image, 0, 4 if random.random() < 0.5 else 5, dist_ratio)

def perturb_r_low(image, dist_ratio):
    return generate_RGB_image(image, 0, 4, dist_ratio)

def perturb_r_high(image, dist_ratio):
    return generate_RGB_image(image, 0, 5, dist_ratio)

def perturb_g(image, dist_ratio):
    return generate_RGB_image(image, 1, 4 if random.random() < 0.5 else 5, dist_ratio)

def perturb_g_low(image, dist_ratio):
    return generate_RGB_image(image, 1, 4, dist_ratio)

def perturb_g_high(image, dist_ratio):
    return generate_RGB_image(image, 1, 5, dist_ratio)

def perturb_b(image, dist_ratio):
    return generate_RGB_image(image, 2, 4 if random.random() < 0.5 else 5, dist_ratio)

def perturb_b_low(image, dist_ratio):
    return generate_RGB_image(image, 2, 4, dist_ratio)

def perturb_b_high(image, dist_ratio):
    return generate_RGB_image(image, 2, 5, dist_ratio)


def generate_HSV_image(image, channel, direction, dist_ratio=0.25):
    
    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    color_str_dic = {
        0: "H",
        1: "S", 
        2: "V"
    }           

    max_val = HSV_SV_MAX
    if channel == 0:
        max_val = HSV_H_MAX

    if direction == 4:
        image[:, :, channel] = (image[:, :, channel] * (1-dist_ratio))
    if direction == 5:
        image[:, :, channel] = (image[:, :, channel] * (1-dist_ratio)) + (max_val * dist_ratio)


    image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    # image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    image = np.moveaxis(image, -1, 0)

    return image

def perturb_h(image, dist_ratio):
    return generate_HSV_image(image, 0, 4 if random.random() < 0.5 else 5, dist_ratio)

def perturb_h_low(image, dist_ratio):
    return generate_HSV_image(image, 0, 4, dist_ratio)

def perturb_h_high(image, dist_ratio):
    return generate_HSV_image(image, 0, 5, dist_ratio)

def perturb_s(image, dist_ratio):
    return generate_HSV_image(image, 1, 4 if random.random() < 0.5 else 5, dist_ratio)

def perturb_s_low(image, dist_ratio):
    return generate_HSV_image(image, 1, 4, dist_ratio)

def perturb_s_high(image, dist_ratio):
    return generate_HSV_image(image, 1, 5, dist_ratio)

def perturb_v(image, dist_ratio):
    return generate_HSV_image(image, 2, 4 if random.random() < 0.5 else 5, dist_ratio)

def perturb_v_low(image, dist_ratio):
    return generate_HSV_image(image, 2, 4, dist_ratio)

def perturb_v_high(image, dist_ratio):
    return generate_HSV_image(image, 2, 5, dist_ratio)

def clean(image, dist_ratio):
    return np.moveaxis(image, -1, 0)

def combine(img, dist_ratio):
    dist_ratio = dist_ratio / 2

    methods = [perturb_r_low, perturb_r_high, perturb_b_low, perturb_b_high, perturb_g_low, perturb_g_high, 
                perturb_h_low, perturb_h_high, perturb_s_low, perturb_s_high, perturb_v_low, perturb_v_high,
                perturb_blur, perturb_noise, perturb_distort]

    img_clean = img.copy()
    
    for i in range(3):
        aug_img = methods[np.random.randint(0, high=len(methods))](img_clean.copy(), dist_ratio)
        aug_img = np.moveaxis(aug_img, 0, -1)
        img = np.uint8(np.mean([img, aug_img], axis=0))

    img = np.moveaxis(img, -1,0)

    return img

def generate_random_image(img, curriculum_max):

    # Original set of perturbations
    methods = [perturb_r_low, perturb_r_high, perturb_b_low, perturb_b_high, perturb_g_low, perturb_g_high, 
                perturb_h_low, perturb_h_high, perturb_s_low, perturb_s_high, perturb_v_low, perturb_v_high,
                perturb_blur, perturb_noise, perturb_distort]

    intensity = np.random.uniform(low=0.0, high=curriculum_max) # random intensity
    aug_img = np.uint8(methods[np.random.randint(0, high=len(methods))](img.copy(), intensity)) # choosing a random perturbation

    return aug_img


def generate_augmentations_batch(image_batch, curriculum_max):
    aug_imgs = []

    '''
        The following comment blocks should be commented and uncommented based on the test
        you are performing. Even though these affects what single perturbations are seen
        by the model during training, ALL of the single perturbations are still present
        during testing.

        However, b/c of the fact that not all single perturbations are seen during training,
        performance of the different below cases should be compared using the performance of
        Clean, Combined, and Unseen.
    '''

    # Original set of perturbations
    methods = [perturb_r_low, perturb_r_high, perturb_b_low, perturb_b_high, perturb_g_low, perturb_g_high, 
                perturb_h_low, perturb_h_high, perturb_s_low, perturb_s_high, perturb_v_low, perturb_v_high,
                perturb_blur, perturb_noise, perturb_distort]

    # Only 9 perturbations where the direction of the single channel perturbations is chosen randomly
    # methods = [perturb_r, perturb_b, perturb_g, perturb_h, perturb_s, perturb_v,
    #             perturb_blur, perturb_noise, perturb_distort]
    
    # Remove HSV perturbations
    # methods = [perturb_r_low, perturb_r_high, perturb_b_low, perturb_b_high, perturb_g_low, 
    #             perturb_g_high, perturb_blur, perturb_noise, perturb_distort]
    
    # Remove RGB perturbations
    # methods = [perturb_h_low, perturb_h_high, perturb_s_low, perturb_s_high, perturb_v_low, 
    #             perturb_v_high, perturb_blur, perturb_noise, perturb_distort]

    # Remove Blue, Noise, Distort
    # methods = [perturb_r_low, perturb_r_high, perturb_b_low, perturb_b_high, perturb_g_low, 
    #             perturb_g_high, perturb_h_low, perturb_h_high, perturb_s_low, perturb_s_high, 
    #             perturb_v_low, perturb_v_high]

    # Remove Blur and Distort perturbations
    # methods = [perturb_r_low, perturb_r_high, perturb_b_low, perturb_b_high, perturb_g_low, 
    #             perturb_g_high, perturb_h_low, perturb_h_high, perturb_s_low, perturb_s_high, 
    #             perturb_v_low, perturb_v_high, perturb_noise ]

    # Only RGB and Noise
    # methods = [perturb_r_low, perturb_r_high, perturb_b_low, perturb_b_high, perturb_g_low, perturb_g_high, 
    #             perturb_noise ]

    # Only HSV and Noise
    # methods = [perturb_h_low, perturb_h_high, perturb_s_low, perturb_s_high, perturb_v_low, perturb_v_high,
    #             perturb_noise]

    # Only RGB
    # methods = [perturb_r_low, perturb_r_high, perturb_b_low, perturb_b_high, perturb_g_low, perturb_g_high]

    # Only HSV 
    # methods = [perturb_h_low, perturb_h_high, perturb_s_low, perturb_s_high, perturb_v_low, perturb_v_high]
    
    # Augmenting the images with single perturbations
    for i in range(len(image_batch)):
        image = image_batch[i]
        intensity = np.random.uniform(low=0.0, high=curriculum_max)
        
        # Static Intensities 
        # intensity = random.choice([0.02, 0.2, 0.5, 0.65, 1.0])

        if i % len(methods) == 0:
            random.shuffle(methods)
    
        aug_imgs.append(np.uint8(methods[i%len(methods)](image.copy(), intensity)))
    
    aug_imgs = np.asarray(aug_imgs)

    # Augmenting a random sampling of the batch with combined perturbations through averaging other images
    # combined_imgs_index = np.random.choice(len(aug_imgs), int((len(image_batch)/10)), replace=False)
    # # print(f"combined imgs index: {combined_imgs_index}")
    # for j in range(len(combined_imgs_index)):
    #     selected_imgs_index = np.random.randint(0, len(aug_imgs), size=2)
    #     # print(f"selected imgs index: {selected_imgs_index}")

    #     aug_imgs[combined_imgs_index[j]] = np.uint8(np.mean(np.array([aug_imgs[combined_imgs_index[j]], aug_imgs[selected_imgs_index[0]], aug_imgs[selected_imgs_index[1]]]), axis=0))        

    return aug_imgs

def generate_augmentations_test(image, aug_method, aug_level):
    
    image_copy = image.copy()

    rgb_dark_light = {
        0: [2, 4],
        1: [2, 5],
        2: [1, 4],
        3: [1, 5],
        4: [0, 4],
        5: [0, 5]
    }

    dark_light = {
        0: [0, 4],
        1: [0, 5],
        2: [1, 4],
        3: [1, 5],
        4: [2, 4],
        5: [2, 5]
    }

    rgb_hsv_levels = {
        "1": 0.02,
        "2": 0.2,
        "3": 0.5,
        "4": 0.65,
        "5": 1.0
    }

    if aug_method == "R lighter":
        values = rgb_dark_light[5]
        noise_image = generate_RGB_image(image_copy, values[0], values[1], dist_ratio=rgb_hsv_levels[aug_level])
 
    if aug_method == "R darker":
        values = rgb_dark_light[4]
        noise_image = generate_RGB_image(image_copy, values[0], values[1], dist_ratio=rgb_hsv_levels[aug_level])

    if aug_method == "G lighter":
        values = rgb_dark_light[3]
        noise_image = generate_RGB_image(image_copy, values[0], values[1], dist_ratio=rgb_hsv_levels[aug_level])

    if aug_method == "G darker":
        values = rgb_dark_light[2]
        noise_image = generate_RGB_image(image_copy, values[0], values[1], dist_ratio=rgb_hsv_levels[aug_level])

    if aug_method == "B lighter":
        values = rgb_dark_light[1]
        noise_image = generate_RGB_image(image_copy, values[0], values[1], dist_ratio=rgb_hsv_levels[aug_level])

    if aug_method == "B darker":
        values = rgb_dark_light[0]
        noise_image = generate_RGB_image(image_copy, values[0], values[1], dist_ratio=rgb_hsv_levels[aug_level])

    if aug_method == "H darker":
        values = dark_light[0]
        noise_image = generate_HSV_image(image_copy, values[0], values[1], dist_ratio=rgb_hsv_levels[aug_level])
    
    if aug_method == "H lighter":
        values = dark_light[1]
        noise_image = generate_HSV_image(image_copy, values[0], values[1], dist_ratio=rgb_hsv_levels[aug_level])
    
    if aug_method == "S darker":
        values = dark_light[2]
        noise_image = generate_HSV_image(image_copy, values[0], values[1], dist_ratio=rgb_hsv_levels[aug_level])
    
    if aug_method == "S lighter":
        values = dark_light[3]
        noise_image = generate_HSV_image(image_copy, values[0], values[1], dist_ratio=rgb_hsv_levels[aug_level])

    if aug_method == "V darker":
        values = dark_light[4]
        noise_image = generate_HSV_image(image_copy, values[0], values[1], dist_ratio=rgb_hsv_levels[aug_level])

    if aug_method == "V lighter":
        values = dark_light[5]
        noise_image = generate_HSV_image(image_copy, values[0], values[1], dist_ratio=rgb_hsv_levels[aug_level])

    blur_levels = {
        "1": 7,
        "2": 17,
        "3": 37,
        "4": 67,
        "5": 107
    }

    noise_levels = {
        "1": 20,
        "2": 50,
        "3": 100,
        "4": 150,
        "5": 200 
    }

    distort_levels = {
        "1": 1,
        "2": 10,
        "3": 50,
        "4": 200,
        "5": 500
    }

    if aug_method == "blur":
        noise_image = generate_blur_image(image_copy, blur_levels[aug_level])

    if aug_method == "noise":
        noise_image = generate_noise_image(image_copy, noise_levels[aug_level])
    
    if aug_method == "distort":
        noise_image = generate_distort_image(image_copy, distort_levels[aug_level])

    return noise_image
