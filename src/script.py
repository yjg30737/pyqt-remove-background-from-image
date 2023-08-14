import os, sys

import cv2
import torch
from PIL import Image
import numpy as np
from torchvision import transforms
from torchvision.models.segmentation import deeplabv3_resnet101, DeepLabV3_ResNet101_Weights


def open_directory(path):
    if sys.platform.startswith('darwin'):  # macOS
        os.system('open "{}"'.format(path))
    elif sys.platform.startswith('win'):  # Windows
        os.system('start "" "{}"'.format(path))
    elif sys.platform.startswith('linux'):  # Linux
        os.system('xdg-open "{}"'.format(path))
    else:
        print("Unsupported operating system.")


def remove_background_from_image(filename):
    try:
        # 1. make mask
        # resnet 101
        def make_deeplab(device):
            deeplab = deeplabv3_resnet101(weights=DeepLabV3_ResNet101_Weights.DEFAULT).to(device)
            deeplab.eval()
            return deeplab

        # DeepLabV3_ResNet50_Weights
        # DeepLabV3_ResNet101_Weights
        # DeepLabV3_MobileNet_V3_Large_Weights

        device = torch.device("cuda")
        deeplab = make_deeplab(device)

        img_orig = cv2.imread(filename, 1)

        k = min(1.0, 1024/max(img_orig.shape[0], img_orig.shape[1]))
        img = cv2.resize(img_orig, None, fx=k, fy=k, interpolation=cv2.INTER_LANCZOS4)

        deeplab_preprocess = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        def apply_deeplab(deeplab, img, device):
            input_tensor = deeplab_preprocess(img)
            input_batch = input_tensor.unsqueeze(0)
            with torch.no_grad():
                output = deeplab(input_batch.to(device))['out'][0]
            output_predictions = output.argmax(0).cpu().numpy()
            return (output_predictions == 15)

        mask = apply_deeplab(deeplab, img, device)

        mask_filename = 'mask_result.png'

        # save temporarily
        Image.fromarray(mask).save(mask_filename)

        # Load the mask and remove it immediately
        mask = cv2.imread(mask_filename, cv2.IMREAD_GRAYSCALE)

        os.remove(mask_filename)

        # 3. make border more smooth
        mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=5, sigmaY=5)

        # Resize the mask to match the image dimensions
        mask = cv2.resize(mask, (img_orig.shape[1], img_orig.shape[0]))

        # Create a new image with an alpha channel (4 channels: BGR + Alpha)
        output_image = np.zeros((img_orig.shape[0], img_orig.shape[1], 4), dtype=np.uint8)

        # Copy the original image to the output image (channels 0-2)
        output_image[:, :, :3] = img_orig

        # Set the alpha channel based on the binary mask (channel 3)
        output_image[:, :, 3] = mask

        # Save the final image with a transparent background
        cv2.imwrite(filename, output_image)

        # 2.1. make the border smoothly
        # # Convert the binary mask to a three-channel format
        # binary_mask_rgb = cv2.merge([mask, mask, mask])
        #
        # # Apply Gaussian blur to the mask
        # blurred_mask = cv2.GaussianBlur(binary_mask_rgb, (0, 0), sigmaX=10, sigmaY=10)
        #
        # # Convert the mask to a float type in the range [0, 1]
        # blurred_mask = blurred_mask.astype(np.float32) / 255.0
        #
        # # Combine the original image and the blurred mask
        # output_image = image * blurred_mask
        #
        # # Convert the output to uint8 and save it
        # output_image = np.clip(output_image, 0, 255).astype(np.uint8)
        # cv2.imwrite('output_image.jpg', output_image)
    except Exception as e:
        print(filename)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)