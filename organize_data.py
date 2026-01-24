import os
import shutil
import random
from pathlib import Path

# Configuration
SOURCE_DIR = "/Users/aditya/Desktop/Kaggle/catdog/train"
BASE_TARGET_DIR = "/Users/aditya/Desktop/Kaggle/catdog/prepared_data"
SPLIT_RATIO = 0.9  # 90% training, 10% validation

def organize_dataset():
    # Create target directories
    train_cats_dir = os.path.join(BASE_TARGET_DIR, 'train', 'cats')
    train_dogs_dir = os.path.join(BASE_TARGET_DIR, 'train', 'dogs')
    val_cats_dir = os.path.join(BASE_TARGET_DIR, 'validation', 'cats')
    val_dogs_dir = os.path.join(BASE_TARGET_DIR, 'validation', 'dogs')

    for d in [train_cats_dir, train_dogs_dir, val_cats_dir, val_dogs_dir]:
        os.makedirs(d, exist_ok=True)
        print(f"Created directory: {d}")

    # Get all files
    all_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.jpg')]
    print(f"Found {len(all_files)} total images.")

    # Sort files to ensure deterministic runs if needed (shuffle comes next)
    all_files.sort()
    random.seed(42) # For reproducibility
    random.shuffle(all_files)

    # Metrics
    cat_count = 0
    dog_count = 0
    moved_count = 0

    for filename in all_files:
        if filename.startswith('cat.'):
            category = 'cats'
            cat_count += 1
        elif filename.startswith('dog.'):
            category = 'dogs'
            dog_count += 1
        else:
            print(f"Skipping unknown file: {filename}")
            continue

        # Determine split (simple random split per file)
        # Note: A more balanced way is to split cats and dogs lists separately, 
        # but for large datasets random shuffle over all is usually fine. 
        # Let's do a stricter split to ensure balance if we wanted, but random is fine here.
        
        is_train = random.random() < SPLIT_RATIO
        
        if is_train:
            target_folder = os.path.join(BASE_TARGET_DIR, 'train', category)
        else:
            target_folder = os.path.join(BASE_TARGET_DIR, 'validation', category)
            
        src_path = os.path.join(SOURCE_DIR, filename)
        dst_path = os.path.join(target_folder, filename)
        
        shutil.copy2(src_path, dst_path)
        moved_count += 1
        if moved_count % 1000 == 0:
            print(f"Processed {moved_count} images...")

    print("-" * 30)
    print("Organization Complete!")
    print(f"Total Cats: {cat_count}")
    print(f"Total Dogs: {dog_count}")
    print(f"Images processed: {moved_count}")
    print(f"Data organized in: {BASE_TARGET_DIR}")

if __name__ == "__main__":
    if not os.path.exists(SOURCE_DIR):
        print(f"Error: Source directory not found at {SOURCE_DIR}")
    else:
        organize_dataset()
