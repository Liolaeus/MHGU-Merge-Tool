# MGHU save file merge/transfer tool.
# Transfer save data from src save file, src slot, to dst save file, dst slot.
# Can transfer any slot from src file to dst file (there are only 3 possible slots in each save)

# Credits:
# https://github.com/mineminemine/MHXXSaveEditor/wiki/MHXX-'system'-file-structure
# https://github.com/Dawnshifter/MHXXSwitchSaveEditor

SRC_FILE = "save1"
DST_FILE = "save2"
SRC_SLOT = 1
DST_SLOT = 2

# Size of switch save file header
HEADER_OFFSET = 36
# offsets to offsets of starting bytes of each character slot
CHAR_OFFSETS = [0x10, 0x14, 0x18]
# offsets to "character slot used" flags
CHAR_USED = [0x4, 0x5, 0x6]

EXPECTED_FILE_SIZE = 5159100
CHARACTER_SIZE = 1177796


def print_bytes(byte_array, start, end):
    for i in range(start, end+1):
        print(f'{byte_array[i]:02x}', end=' ')
    print()

# convert little-endian character offsets to integer
def bytes_to_int(byte_array, start, end):
    return int.from_bytes(byte_array[start:end+1], byteorder='little')

def load_save(file_path):
    with open(file_path, 'rb') as f:
        save_bytes = f.read()
        print(f"{file_path}: file size: {len(save_bytes)} bytes")

        if len(save_bytes) != EXPECTED_FILE_SIZE:
            raise ValueError(f"File {file_path} is {len(save_bytes)} bytes, expected {EXPECTED_FILE_SIZE} bytes")

        return save_bytes

def get_slot_offset(byte_array, slot_number):
    if slot_number < 1 or slot_number > 3:
        raise ValueError("Slot number must be 1, 2, or 3")

    offset = CHAR_OFFSETS[slot_number - 1]
    return bytes_to_int(byte_array, HEADER_OFFSET + offset, HEADER_OFFSET + offset + 3)

def transfer_slot(src_file_path, dst_file_path, src_slot, dst_slot):
    src_bytes = load_save(src_file_path)
    dst_bytes = load_save(dst_file_path)

    # offsets to starting bytes of each character slot
    src_offset = get_slot_offset(src_bytes, src_slot)
    dst_offset = get_slot_offset(dst_bytes, dst_slot)

    src_data = src_bytes[src_offset:src_offset + CHARACTER_SIZE]

    slot_used_offset = CHAR_USED[dst_slot - 1]  + HEADER_OFFSET

    # insert src char data into dst save
    output_bytes = (
        dst_bytes[:slot_used_offset] +
        bytes([1]) +  # Mark dst slot as used
        dst_bytes[slot_used_offset + 1:dst_offset] +
        src_data +
        dst_bytes[dst_offset + CHARACTER_SIZE:]
    )

    if len(output_bytes) != EXPECTED_FILE_SIZE:
        raise ValueError(f"Output file is {len(output_bytes)} bytes, expected {EXPECTED_FILE_SIZE} bytes")

    return output_bytes

if __name__ == "__main__":
    output_bytes = transfer_slot(SRC_FILE, DST_FILE, SRC_SLOT, DST_SLOT)

    with open('merged_save', 'wb') as f:
        f.write(output_bytes)
        f.close()

    print("Transfer complete, merged save file written to 'merged_save'")
