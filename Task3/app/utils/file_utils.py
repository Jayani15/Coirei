"""
File utility functions
"""
import hashlib
import os
import aiofiles
from typing import Optional


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return os.path.splitext(filename)[1].lower()


def get_file_name_without_extension(filename: str) -> str:
    """Get filename without extension"""
    return os.path.splitext(filename)[0]


async def calculate_checksum(file_path: str, algorithm: str = "sha256") -> str:
    """Calculate file checksum"""
    hash_obj = hashlib.new(algorithm)
    
    async with aiofiles.open(file_path, 'rb') as f:
        while chunk := await f.read(8192):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def is_valid_filename(filename: str) -> bool:
    """Check if filename is valid (no path traversal, etc.)"""
    # Check for path traversal attempts
    if ".." in filename or "/" in filename or "\\" in filename:
        return False
    
    # Check for hidden files
    if filename.startswith("."):
        return False
    
    # Check for special characters
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
    if any(char in filename for char in invalid_chars):
        return False
    
    return True


async def encrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """Encrypt a file using AES encryption (optional - requires cryptography package)"""
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    import os
    
    # Generate random IV
    iv = os.urandom(16)
    
    # Create cipher
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    async with aiofiles.open(input_path, 'rb') as f_in:
        async with aiofiles.open(output_path, 'wb') as f_out:
            # Write IV to file
            await f_out.write(iv)
            
            # Encrypt and write data
            while chunk := await f_in.read(8192):
                encrypted_chunk = encryptor.update(chunk)
                await f_out.write(encrypted_chunk)
            
            # Finalize encryption
            await f_out.write(encryptor.finalize())


async def decrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """Decrypt a file using AES encryption (optional - requires cryptography package)"""
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    
    async with aiofiles.open(input_path, 'rb') as f_in:
        # Read IV
        iv = await f_in.read(16)
        
        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        async with aiofiles.open(output_path, 'wb') as f_out:
            # Decrypt and write data
            while chunk := await f_in.read(8192):
                decrypted_chunk = decryptor.update(chunk)
                await f_out.write(decrypted_chunk)
            
            # Finalize decryption
            await f_out.write(decryptor.finalize())