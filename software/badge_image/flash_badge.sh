#!/usr/bin/env bash
# Mount Pico and copy firmware file

FIRMWARE=./supercon_image.uf2

# Function to execute on new device
new_device ()
{
	# First save the device to variable
	DEVICE=$(echo $1 | cut -d'/' -f3)

	# Notify user
	#echo "Found Device: $DEVICE"	

	# Create mount point if it doesn't exist
	mkdir -p /mnt/$DEVICE

	# Mount device
	mount /dev/$DEVICE /mnt/$DEVICE

	# Copy firmware
	cp $FIRMWARE /mnt/$DEVICE/
	
	# Attempt unmount to force write
	echo -n "Copying firmware to $DEVICE ..."
	umount /mnt/$DEVICE
	echo "Done"

	# Delete device node so we don't try to do it again
	rm /dev/$DEVICE 
}

# Must have root permission
if [ "$EUID" -ne 0 ]
  then echo "Must run as root or via sudo"
  exit
fi

# Start here
systemctl daemon-reload

echo "Looking for new devices..."
echo "Hold BOOTSEL for 5 seconds while plugging in."

# Loop through, looking for device files
while true
 do
   for I in `ls /dev/sd*1 2>/dev/null`
    do new_device $I
   done
 sleep 5
done

# EOF
