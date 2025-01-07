import os
import cv2

def draw_labels_on_images(images_dir, labels_dir, output_dir):
    # Tạo thư mục lưu kết quả nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)

    # Lọc và chỉ lấy các file có cùng tên giữa ảnh và label
    image_files = {os.path.splitext(f)[0]: f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))}
    label_files = {os.path.splitext(f)[0]: f for f in os.listdir(labels_dir) if f.lower().endswith('.txt')}

    # Chỉ xử lý các file có cả ảnh và label tương ứng
    common_files = image_files.keys() & label_files.keys()

    for base_name in common_files:
        image_name = image_files[base_name]
        label_name = label_files[base_name]

        # Đường dẫn đến hình ảnh và file label tương ứng
        image_path = os.path.join(images_dir, image_name)
        label_path = os.path.join(labels_dir, label_name)

        # Đọc hình ảnh
        image = cv2.imread(image_path)
        if image is None:
            print(f"[Error] Failed to read image: {image_name}")
            continue

        height, width, _ = image.shape
        labels_found = False

        # Đọc file label
        with open(label_path, 'r') as file:
            for line_num, line in enumerate(file, start=1):
                parts = line.strip().split()
                if len(parts) != 5:
                    print(f"[Warning] Invalid label format at line {line_num} in file: {label_path}")
                    continue

                try:
                    class_id, x_center, y_center, bbox_width, bbox_height = map(float, parts)
                except ValueError:
                    print(f"[Error] Non-numeric values at line {line_num} in file: {label_path}")
                    continue

                # Chuyển đổi tọa độ từ hệ quy chiếu tương đối sang pixel
                x_center *= width
                y_center *= height
                bbox_width *= width
                bbox_height *= height

                x1 = int(x_center - bbox_width / 2)
                y1 = int(y_center - bbox_height / 2)
                x2 = int(x_center + bbox_width / 2)
                y2 = int(y_center + bbox_height / 2)

                # Kiểm tra tọa độ bounding box có hợp lệ không
                if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
                    print(f"[Warning] Bounding box out of bounds at line {line_num} in file: {label_path}")
                    continue

                # Vẽ bounding box và class_id lên hình ảnh
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, str(int(class_id)), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                labels_found = True

        if not labels_found:
            print(f"[Info] No valid labels found for image: {image_name}")
            continue

        # Lưu hình ảnh đã được vẽ bounding box vào thư mục result
        output_path = os.path.join(output_dir, image_name)
        cv2.imwrite(output_path, image)
        print(f"[Success] Processed and saved: {output_path}")

# Example usage
images_dir = "images"
labels_dir = "labels"
output_dir = "result"

draw_labels_on_images(images_dir, labels_dir, output_dir)
