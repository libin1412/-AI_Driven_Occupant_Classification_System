import os
import shutil

# Define paths
dataset_path = r"C:\Users\libin\Downloads\x5_grayscale_wholeImage\x5\test_with_labels\grayscale_wholeImage"
output_path = r"D:\Occupant Classification system\occupant_classification_system\SVIRO\test"

# Create output directory
os.makedirs(output_path, exist_ok=True)

# Mapping of classes to categories
class_to_category = {
    "0": "empty",
    "1": "infant",
    "2": "child",
    "3": "adult",
    "4": "object",
    "5": "empty",      # Group empty infant seat with empty
    "6": "empty"       # Group empty child seat with empty
}

# Define folder mapping based on combinations
def get_folder_name(categories):
    if "adult" in categories and "child" in categories:
        return "adult_child"
    elif "adult" in categories and "infant" in categories:
        return "adult_infant"
    elif "adult" in categories and ("empty" in categories or "object" in categories):
        return "adult_empty"
    elif "child" in categories and "infant" in categories:
        return "child_infant"
    elif "child" in categories and ("empty" in categories or "object" in categories):
        return "child_empty"
    elif "infant" in categories and ("empty" in categories or "object" in categories):
        return "infant_empty"
    elif len(categories) == 1 and "empty" in categories:
        return "empty_only"
    else:
        return None  # For unmatched cases

# Process files
for filename in os.listdir(dataset_path):
    if filename.endswith(".png"):
        # Extract seat classifications from filename
        parts = filename.split("_")
        seats = parts[-3:]  # Last three parts are seat classifications
        
        # Get unique categories present in the image
        categories = sorted(set(class_to_category[seat] for seat in seats if seat in class_to_category))
        
        # Map to a specific folder name
        folder_name = get_folder_name(categories)
        
        if folder_name:
            # Create folder if it doesn't exist
            folder_path = os.path.join(output_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            
            # Copy file to corresponding folder
            src = os.path.join(dataset_path, filename)
            dst = os.path.join(folder_path, filename)
            shutil.copy(src, dst)

print("Categorization complete!")

# Count images in each category
from collections import defaultdict

category_counts = defaultdict(int)
for root, dirs, files in os.walk(output_path):
    for dir in dirs:
        category_counts[dir] = len(os.listdir(os.path.join(root, dir)))

print("\nImage counts per category:")
for category, count in sorted(category_counts.items()):
    print(f"{category}: {count}")