from cryptography.fernet import Fernet
import os

def generate_key():
    """Generate a key and save it into a file"""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("New key generated and saved to 'secret.key'.")

def load_key():
    """Load the key from Env Var or file"""
    # 1. Try Environment Variable (Best for CI/CD)
    env_key = os.environ.get("SECRET_KEY")
    if env_key:
        # User might store it as string in GitHub Secrets, ensure bytes
        return env_key.encode() if isinstance(env_key, str) else env_key

    # 2. Try Local File (Best for Local Dev)
    if os.path.exists("secret.key"):
        return open("secret.key", "rb").read()

    # If no key found, generate a temporary one for this session (for testing only)
    # or return None to let the caller handle it.
    # For now, we will warn and generate a temp key to prevent crash,
    # but actual decryption of existing data will fail.
    print("Warning: SECRET_KEY not found in ENV or file. Using a temporary key (decryption will fail).")
    return Fernet.generate_key()

def encrypt_message(message):
    """Encrypts a message"""
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message):
    """Decrypts an encrypted message"""
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()

if __name__ == "__main__":
    # If run directly, generate a key for setup
    if not os.path.exists("secret.key"):
        generate_key()
    else:
        print("Key file 'secret.key' already exists.")
