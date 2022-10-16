import hashlib
import mmap
import re
import os
import sys
import argparse
from kaitaistruct import KaitaiStream, BytesIO
from java_class import JavaClass

JAVA_SIG = b'\xCA\xFE\xBA\xBE'
BLOCK_SIZE = 1024 * 1024
INTERFACE_FLAG = 0x200

def class_dump(payload,name, out_dir):
    name=name+".class"
    file_name = os.path.join(out_dir, name)
    fd = open(file_name,"wb")
    fd.write(payload)
    fd.close()

def get_md5_hash(payload):
    mymd5 = hashlib.md5(payload)
    return mymd5.hexdigest()

def get_java_offsets(file_name):
    offsets = []
    fd = open(file_name,"rb")
    searcher = mmap.mmap(fd.fileno(), 0, access=mmap.ACCESS_READ)
    javare = re.compile(JAVA_SIG)
    for result in javare.finditer(searcher):
        offsets.append(result.start())
    return offsets

def read_block(file_name, offset, size):
    fd = open(file_name, "rb")
    fd.seek(offset)
    block = fd.read(size)
    fd.close()
    return block

def get_class_full_name(myjclass):
    name_index = myjclass.constant_pool[myjclass.this_class-1].cp_info.name_index - 1
    class_name = myjclass.constant_pool[name_index].cp_info.value
    return class_name

def not_j_class(myjclass):
    try:
        class_name = get_class_full_name(myjclass)
    except:
        return True

    if "$" not in class_name and not (myjclass.access_flags & INTERFACE_FLAG):
        return False
    else:
        return True

def get_class_short_name(myjclass):
    class_name = get_class_full_name(myjclass)
    short_class_name = class_name.split('/')
    short_class_name = short_class_name[len(short_class_name) - 1]
    return short_class_name

def main(file_name, out_dir):
    print("\nAuthor: Mohammed Almodawah\n")
    print("Look4Shell V 1.0\n")
    sys.stdout.write("Locating Java Headers...")
    sys.stdout.flush()
    java_offsets = get_java_offsets(file_name)
    sys.stdout.write("\rDumping Java Classes...\n")
    sys.stdout.flush()

    classes_hashes = []
    for i, java_offset in enumerate(java_offsets):
        payload = read_block(file_name, java_offset, BLOCK_SIZE)
        try:
            myjclass = JavaClass(KaitaiStream(BytesIO(payload)))
        except:
            continue

        class_hash = get_md5_hash(payload[0 : myjclass.file_size])
        if class_hash in classes_hashes:
            continue
        
        if not_j_class(myjclass):
            continue

        classes_hashes.append(class_hash)
        short_class_name = get_class_short_name(myjclass)
        print("")
        print("Class name: " + short_class_name)
        print("Class size: " + str(myjclass.file_size) + " bytes")
        print("MD5 hash: " + class_hash)
        class_dump(payload[0 : myjclass.file_size],short_class_name + "_" + class_hash, out_dir)
    
    print("")
    print("Total classes found: " + str(len(classes_hashes)))

parser = argparse.ArgumentParser(description = "Look4Shell V 1.0. Author: Mohammed Almodawah. This tool allows you to dump java classes from memory dumps.")
parser.add_argument("File", help="Path to your memory dump file")
parser.add_argument("Directory", help="Path of where you want to dump the extracted java classes")
args = parser.parse_args()

main(args.File, args.Directory)
