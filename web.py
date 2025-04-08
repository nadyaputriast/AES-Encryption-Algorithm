import streamlit as st
from Padding import aes_encrypt_with_padding, pad_data
from PredefinedKey import key
from Encrypt import aes_encrypt

def display_matrix(matrix):
    """Helper function to display a 4x4 matrix in Streamlit."""
    st.write("State Matrix:")
    for row in matrix:
        st.write(" | ".join(f"{byte:02X}" for byte in row))

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

        # Step 1: Padding plaintext
        padded_plaintext = pad_data(plaintext, key_len)
        st.write("Padded Plaintext (Hex):")
        padded_plaintext = pad_data(plaintext, 16)
        st.code(padded_plaintext.hex().upper(), language="plaintext")

        # Step 2: Initial key addition
        st.write("Initial Key (Hex):")
        st.code(user_key.encode('utf-8').hex().upper(), language="plaintext")

        # Step 3: Encryption process
        st.write("Encryption Steps:")
        ciphertext, steps = aes_encrypt_with_padding(plaintext, user_key, key_len, debug=True)
                
        # Menentukan jumlah round berdasarkan panjang kunci
        if key_len == 16:
            num_rounds = 10
        elif key_len == 24:
            num_rounds = 12
        else:
            num_rounds = 14
            
        step_index = 0
        
        # 1. Konversi plaintext ke hex dan matrix
        if step_index < len(steps):
            with st.expander("1. Konversi Plaintext ke Hex dan Matrix"):
                st.write("**Deskripsi:** Konversi Plantext ke hex dan matrix")
                state_matrix = [
                    steps[step_index]['state'][j:j+4] for j in range(0, len(steps[step_index]['state']), 4)
                ]
                display_matrix(state_matrix)
                step_index += 1
        
        # 2. Penambahan Initial Round Key
        if step_index < len(steps):
            with st.expander("2. Penambahan Initial Round Key"):
                st.write("**Deskripsi:** XOR dengan kunci awal")
                state_matrix = [
                    steps[step_index]['state'][j:j+4] for j in range(0, len(steps[step_index]['state']), 4)
                ]
                display_matrix(state_matrix)
                step_index += 1

        # 3. Iterasi round 1 sampai (n-1)
        for round_num in range(1, num_rounds):
            if step_index + 3 < len(steps):  # pastikan 4 langkah tersedia
                with st.expander(f"{round_num + 2}. Round {round_num} (SubBytes, ShiftRows, MixColumns, AddRoundKey)"):
                    step_labels = ["SubBytes", "ShiftRows", "MixColumns", "AddRoundKey"]
                    for label in step_labels:
                        if step_index < len(steps):
                            st.write(f"**Langkah:** {label}")
                            state_matrix = [
                                steps[step_index]['state'][j:j+4] for j in range(0, len(steps[step_index]['state']), 4)
                            ]
                            display_matrix(state_matrix)
                            step_index += 1
        
        # 4. Final Round
        if step_index + 3 <= len(steps):
            with st.expander(f"{num_rounds + 2}. Final Round (SubBytes, ShiftRows, AddRoundKey)"):
                final_labels = ["SubBytes", "ShiftRows", "AddRoundKey"]
                for label in final_labels:
                    if step_index < len(steps):
                        st.write(f"**Langkah:** {label}")
                        state_matrix = [
                            steps[step_index]['state'][j:j+4] for j in range(0, len(steps[step_index]['state']), 4)
                        ]
                        display_matrix(state_matrix)
                        step_index += 1

        # Final ciphertext
        ciphertext_hex = bytes(ciphertext).hex().upper()
        st.write("Final Ciphertext (Hex):")
        st.code(ciphertext_hex, language="plaintext")
        
if __name__ == "__main__":
    main()