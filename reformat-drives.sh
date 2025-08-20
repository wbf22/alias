
# get the drive name with this (assuming named sdb below)
lsblk


# wipe completely if needed
sudo dd if=/dev/zero of=/dev/sdb bs=4M status=progress

# reformat
sudo parted /dev/sdb mklabel msdos
sudo parted -a optimal /dev/sdb mkpart primary 0% 100%
sudo partprobe /dev/sdb
sudo mkfs.ntfs -f /dev/sdb1 -L MyUSB


# mounting unmounting
sudo mkdir -p /mnt/usb
sudo mount -t ntfs /dev/sdb1 /mnt/usb
sudo umount /mnt/usb
