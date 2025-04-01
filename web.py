import streamlit as st
from Padding import aes_encrypt_with_padding
from PredefinedKey import key

def main():
    st.markdown("# AES Encryption")

    plaintext = st.text_input("Masukkan plaintext:", key="plaintext")

    key_option = st.radio(
        "Pilih metode kunci:", 
        ("Gunakan kunci sendiri", "Gunakan kunci bawaan"),
        key="key_option"
    )

    predefined_key = key.decode('utf-8')

    if key_option == "Gunakan kunci sendiri":
        user_key = st.text_input(
            "Masukkan kunci:", 
            key="user_key", 
            type="password"
        )
    else:
        user_key = predefined_key
        show_predefined_key = st.checkbox("Tampilkan kunci bawaan")
        if show_predefined_key:
            st.write(f"Predefined Key: `{user_key}`")
        else:
            st.write("Predefined Key: `********`")
                 
    key_len = len(user_key)

    if key_len not in [16, 24, 32]:
        st.warning("Masukkan kunci yang panjangnya 16, 24, atau 32 karakter.")
    else:
        st.write(f"Key Size: {key_len * 8} bits")

        ciphertext = aes_encrypt_with_padding(plaintext, user_key, key_len)
        ciphertext_hex = bytes(ciphertext).hex().upper()
        
        st.write("Ciphertext: ")
        st.code(ciphertext_hex, language="plaintext")

if __name__ == "__main__":
    main()