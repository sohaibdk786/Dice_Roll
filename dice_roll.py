import os
from PIL import Image, ImageTk
import tkinter as tk
import time  # Import the time module

BLACK_DICE_FOLDER = r"C:\Users\Chaudhary\Desktop\Dice Roll\Dices\Black_dice"
GOLD_DICE_FOLDER = r"C:\Users\Chaudhary\Desktop\Dice Roll\Dices\Gold_dice"

# Define the sizes
BLACK_PREVIEW_SIZE = (100, 100)  # Size for the black dice preview
GOLD_PREVIEW_SIZE = (107, 107)   # Slightly larger size for the gold dice preview
OUTPUT_SIZE = (300, 300)         # Size for the final dice images

# Shuffle parameters
SHUFFLE_INTERVAL = 50  # Interval in milliseconds
SHUFFLE_DURATION = 500  # Duration of the shuffle effect in milliseconds

def load_dice_images(dice_folder, size):
    images = {}
    for i in range(1, 7):
        try:
            image_path = os.path.join(dice_folder, f"{i}.png")
            if os.path.exists(image_path):
                with Image.open(image_path) as img:
                    # Resize and pad the image to ensure it fits the specified size
                    img = resize_and_pad(img, size)
                    images[i] = img
            else:
                print(f"File not found: {image_path}")
        except Exception as e:
            print(f"Error loading {i}.png: {e}")
    return images

def resize_and_pad(image, size):
    # Calculate the padding needed to make the image fit the desired size
    original_size = image.size
    ratio = min(size[0] / original_size[0], size[1] / original_size[1])
    new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
    image = image.resize(new_size, Image.LANCZOS)

    # Create a new image with the desired size and a white background
    new_image = Image.new("RGBA", size, (255, 255, 255, 255))
    new_image.paste(image, ((size[0] - new_size[0]) // 2, (size[1] - new_size[1]) // 2))
    return new_image

def roll_dice(dice_images):
    import random
    return random.choice(list(dice_images.keys()))

def shuffle_images(root, dice_images, label, end_time):
    now = time.time()
    if now < end_time:
        roll = roll_dice(dice_images)
        image = dice_images[roll]
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo  # Keep a reference
        root.after(SHUFFLE_INTERVAL, shuffle_images, root, dice_images, label, end_time)
    else:
        # Final roll
        roll = roll_dice(dice_images)
        image = dice_images[roll]
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo  # Keep a reference

def update_dice_image(dice_folder, label):
    dice_images = load_dice_images(dice_folder, OUTPUT_SIZE)
    if not dice_images:
        print(f"No images loaded from {dice_folder}")
        return
    
    end_time = time.time() + SHUFFLE_DURATION / 1000  # Convert milliseconds to seconds
    shuffle_images(root, dice_images, label, end_time)

def update_preview_images():
    # Load preview images for both dice types
    black_dice_images = load_dice_images(BLACK_DICE_FOLDER, BLACK_PREVIEW_SIZE)
    gold_dice_images = load_dice_images(GOLD_DICE_FOLDER, GOLD_PREVIEW_SIZE)
    
    # Use the image for the '1' roll as the preview (or any other roll)
    black_preview_image = black_dice_images.get(1)
    gold_preview_image = gold_dice_images.get(1)
    
    if black_preview_image:
        black_photo = ImageTk.PhotoImage(black_preview_image)
        black_preview_label.config(image=black_photo)
        black_preview_label.image = black_photo  # Keep a reference
    
    if gold_preview_image:
        gold_photo = ImageTk.PhotoImage(gold_preview_image)
        gold_preview_label.config(image=gold_photo)
        gold_preview_label.image = gold_photo  # Keep a reference

def select_dice_type(dice_type):
    global current_dice_folder
    if dice_type == 'Black':
        current_dice_folder = BLACK_DICE_FOLDER
    elif dice_type == 'Gold':
        current_dice_folder = GOLD_DICE_FOLDER
    else:
        print("Invalid dice selection")
        return

def roll_dice_action():
    if current_dice_folder:
        update_dice_image(current_dice_folder, dice_label)

def main():
    global black_preview_label, gold_preview_label, current_dice_folder, dice_label, root
    
    root = tk.Tk()
    root.title("Dice Roll")
    
    # Set the window size of gui
    root.geometry("700x600")

    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Create a frame to hold the dice selection and preview
    dice_frame = tk.Frame(frame)
    dice_frame.pack(side=tk.LEFT, padx=10)
    
    # Preview images for dice
    black_preview_label = tk.Label(dice_frame)
    black_preview_label.grid(row=0, column=0, padx=5)
    gold_preview_label = tk.Label(dice_frame)
    gold_preview_label.grid(row=0, column=1, padx=5)
    
    tk.Label(dice_frame, text="Black Dice").grid(row=1, column=0)
    tk.Label(dice_frame, text="Gold Dice").grid(row=1, column=1)

    # Bind click events to the preview images
    black_preview_label.bind("<Button-1>", lambda e: select_dice_type('Black'))
    gold_preview_label.bind("<Button-1>", lambda e: select_dice_type('Gold'))

    roll_button = tk.Button(root, text="Roll Dice", command=roll_dice_action)
    roll_button.pack(pady=10)

    dice_label = tk.Label(root)
    dice_label.pack(pady=10)

    # Set initial dice folder
    current_dice_folder = BLACK_DICE_FOLDER

    # Update preview images at the start
    update_preview_images()

    root.mainloop()

if __name__ == "__main__":
    main()
