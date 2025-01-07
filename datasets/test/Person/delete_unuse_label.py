import os

def remove_unmatched_labels(images_dir, labels_dir):

    image_files = {os.path.splitext(file)[0] for file in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, file))}
    

    for label_file in os.listdir(labels_dir):
        label_name, _ = os.path.splitext(label_file)
        label_path = os.path.join(labels_dir, label_file)
        

        if label_name not in image_files:
            print(f"Deleting unmatched label file: {label_file}")
            os.remove(label_path)


images_directory = "./images" 
labels_directory = "./labels"  

remove_unmatched_labels(images_directory, labels_directory)