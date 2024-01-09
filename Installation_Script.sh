#!/bin/bash

# Gets the absolute path to the script directory
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# The relative path of the source file
source_files_dir="$script_dir/resources/driver"

# Source files and target paths
source_file_dtb="$source_files_dir/tegra234-p3701-0000-p3737-0000.dtb"
target_path_dtb="/boot/dtb/kernel_tegra234-p3701-0000-p3737-0000.dtb"
source_file_max96712="$source_files_dir/max96712.ko"
source_file_nv_ar0234="$source_files_dir/nv_ar0234.ko"
source_file_bmi088="$source_files_dir/bmi088.ko"
source_file_camera_overrides="$source_files_dir/camera_overrides.isp"
target_path_media_i2c="/lib/modules/5.10.104-tegra/kernel/drivers/media/i2c/"
target_path_ko="/lib/modules/5.10.104-tegra/kernel/drivers/iio/imu/bmi088/"
target_path_camera_overrides="/var/nvidia/nvcam/settings/"

# Copy the file to the destination path
sudo cp "$source_file_dtb" "$target_path_dtb" && echo "dtb file copied successfully!"
sudo cp "$source_file_max96712" "$target_path_media_i2c" && echo "max96712.ko file copied successfully!"
sudo cp "$source_file_nv_ar0234" "$target_path_media_i2c" && echo "nv_ar0234.ko file copied successfully!"
sudo cp "$source_file_bmi088" "$target_path_ko" && echo "bmi088.ko file copied successfully!"
sudo cp "$source_file_camera_overrides" "$target_path_camera_overrides" && echo "camera_overrides.isp file copied successfully!"
