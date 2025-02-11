import os
import random
from PIL import Image, ImageOps
from tqdm import tqdm  # For progress bar

# Paths to your dataset
dataset_path = r"D:\Occupant Classification system\occupant_classification_system\SVIRO\train"
folders_to_augment = ["adult_child", "child_infant"]  # Folders to augment
target_count = 100  # Target number of images per folder

# Define augmentation functions
def augment_image(image):
    """
    Apply random augmentations to an image.
    """
    augmentations = [
        lambda x: x,  # No change
        ImageOps.mirror,  # Horizontal flip
        ImageOps.flip,  # Vertical flip
        lambda x: x.rotate(15),  # Rotate 15 degrees
        lambda x: x.rotate(-15),  # Rotate -15 degrees
        lambda x: x.crop((10, 10, x.width - 10, x.height - 10)).resize(x.size),  # Crop and resize
    ]
    augmentation = random.choice(augmentations)
    return augmentation(image)

# Augment images in each folder
for folder in folders_to_augment:
    folder_path = os.path.join(dataset_path, folder)
    if not os.path.exists(folder_path):
        print(f"Folder '{folder}' does not exist. Skipping...")
        continue

    images = [f for f in os.listdir(folder_path) if f.endswith(".png") or f.endswith(".jpg")]
    current_count = len(images)

    if current_count >= target_count:
        print(f"Folder '{folder}' already has {current_count} images. No augmentation needed.")
        continue

    print(f"Augmenting folder '{folder}' ({current_count} -> {target_count})...")

    # Generate augmented images until target count is reached
    for i in tqdm(range(target_count - current_count)):
        # Choose a random image to augment
        image_name = random.choice(images)
        image_path = os.path.join(folder_path, image_name)

        # Open the image and apply augmentation
        with Image.open(image_path) as img:
            augmented_image = augment_image(img)

            # Save the augmented image with a new name
            new_image_name = f"{os.path.splitext(image_name)[0]}_aug_{i}.png"
            new_image_path = os.path.join(folder_path, new_image_name)
            augmented_image.save(new_image_path)

print("Data augmentation complete!")
