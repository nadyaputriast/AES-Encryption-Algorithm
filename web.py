import streamlit as st
from Padding import pad_data, aes_encrypt_with_padding, aes_encrypt_without_padding
from PredefinedKey import key

def display_matrix(matrix):
    """Helper function to display a 4x4 matrix in Streamlit."""
    st.write("State Matrix:")
    for row in matrix:
        st.write(" | ".join(f"{byte:02X}" for byte in row))

def main():
    st.markdown("# AES Encryption")

    # Form untuk input pengguna
    with st.form(key="encryption_form"):
        plaintext = st.text_input("Masukkan plaintext:", key="plaintext")

        key_option = st.radio(
            "Pilih metode kunci:", 
            ("Gunakan kunci sendiri", "Gunakan kunci bawaan"),
            key="key_option"
        )

        predefined_key = key.decode('utf-8')

        if key_option == "Gunakan kunci sendiri":
            user_key = st.text_input("Masukkan kunci:", key="user_key", type="password")
        else:
            user_key = predefined_key
            show_predefined_key = st.checkbox("Tampilkan kunci bawaan")
            if show_predefined_key:
                st.write(f"Predefined Key: `{user_key}`")
            else:
                st.write("Predefined Key: `********`")
        
        # Tambahkan opsi padding             
        use_padding = st.checkbox("Gunakan Padding", value=True, help="Jika dicentang, plaintext akan dipadding hingga kelipatan 16 bytes")
        
        # Tombol submit
        submit_button = st.form_submit_button(label="Enkripsi")

    # Tampilkan hasil enkripsi jika tombol telah ditekan
    if submit_button:
        # Lakukan proses enkripsi dan tampilkan hasilnya
        if not plaintext:
            st.error("Plaintext tidak boleh kosong!")
            return
            
        if not user_key:
            st.error("Kunci tidak boleh kosong!")
            return
            
        key_len = len(user_key.encode('utf-8'))  # Ensure we use byte length

        if key_len not in [16, 24, 32]:
            st.error(f"Panjang kunci saat ini: {key_len} byte. Masukkan kunci yang panjangnya 16, 24, atau 32 byte.")
            return
            
        st.write(f"Key Size: {key_len * 8} bits")

        # Menentukan jumlah round berdasarkan panjang kunci
        if key_len == 16:
            num_rounds = 10
        elif key_len == 24:
            num_rounds = 12
        else:
            num_rounds = 14

        # Check if plaintext is valid
        encoded_plaintext = plaintext.encode('utf-8')
        
        # Check if plaintext length is valid when not using padding
        if not use_padding and len(encoded_plaintext) % 16 != 0:
            st.error(f"Panjang plaintext ({len(encoded_plaintext)} bytes) harus kelipatan 16 bytes jika tidak menggunakan padding.")
            return
        
        # Display plaintext info
        st.write("Plaintext (Hex):")
        st.code(encoded_plaintext.hex().upper(), language="plaintext")
        
        # Apply padding if selected
        if use_padding:
            padded_plaintext = pad_data(encoded_plaintext, 16)
            st.write("Padded Plaintext (Hex):")
            st.code(padded_plaintext.hex().upper(), language="plaintext")
        else:
            padded_plaintext = encoded_plaintext
            st.write("Plaintext tidak dipadding.")

        # Calculate number of blocks
        num_blocks = len(padded_plaintext) // 16
        st.write(f"Jumlah Blok: {num_blocks}")

        # Step 2: Tampilkan initial key
        key_bytes = user_key.encode('utf-8')
        st.write("Initial Key (Hex):")
        st.code(key_bytes.hex().upper(), language="plaintext")

        # Step 3: Encryption process (debug mode aktif)
        try:
            if use_padding:
                ciphertext, all_steps = aes_encrypt_with_padding(plaintext, user_key, key_len, debug=True)
            else:
                ciphertext, all_steps = aes_encrypt_without_padding(plaintext, user_key, key_len, debug=True)
        except Exception as e:
            st.error(f"Error dalam proses enkripsi: {str(e)}")
            return
            
        # Organize steps by block
        steps_by_block = {}
        for step in all_steps:
            block_num = step.get("block", 0)
            if block_num not in steps_by_block:
                steps_by_block[block_num] = []
            steps_by_block[block_num].append(step)
        
        # Display steps for each block
        for block_num in range(num_blocks):
            with st.expander(f"### Block {block_num + 1}"):
                if block_num in steps_by_block:
                    block_steps = steps_by_block[block_num]
                    step_index = 0
                    
                    # Display initial block state
                    block_start = block_num * 16
                    block_data = padded_plaintext[block_start:block_start+16]
                    initial_matrix = [[0 for _ in range(4)] for _ in range(4)]
                    for i in range(4):
                        for j in range(4):
                            initial_matrix[j][i] = block_data[i * 4 + j]
                    
                    st.write("**1. Konversi Plaintext Blok ke Matrix**")
                    st.write("**Deskripsi:** Konversi plaintext ke representasi matriks (sebelum XOR key)")
                    display_matrix(initial_matrix)
                    
                    # Initial AddRoundKey
                    if step_index < len(block_steps):
                        st.write("**2. Initial AddRoundKey**")
                        st.write("**Deskripsi:** XOR dengan kunci awal")
                        step_data = block_steps[step_index]['state']
                        state_matrix = [[0 for _ in range(4)] for _ in range(4)]
                        for i in range(4):
                            for j in range(4):
                                state_matrix[j][i] = step_data[i * 4 + j]
                        display_matrix(state_matrix)
                        step_index += 1
                    
                    # Main rounds
                    for round_num in range(1, num_rounds):
                        if step_index + 3 < len(block_steps):  # pastikan 4 langkah tersedia
                            st.write(f"**{round_num + 2}. Round {round_num}**")
                            step_labels = ["SubBytes", "ShiftRows", "MixColumns", "AddRoundKey"]
                            for label in step_labels:
                                if step_index < len(block_steps):
                                    st.write(f"**Langkah:** {label}")
                                    step_data = block_steps[step_index]['state']
                                    state_matrix = [[0 for _ in range(4)] for _ in range(4)]
                                    for i in range(4):
                                        for j in range(4):
                                            state_matrix[j][i] = step_data[i * 4 + j]
                                    display_matrix(state_matrix)
                                    step_index += 1
                    
                    # Final Round
                    if step_index + 2 < len(block_steps):
                        st.write(f"**{num_rounds + 2}. Final Round**")
                        final_labels = ["SubBytes", "ShiftRows", "AddRoundKey"]
                        for label in final_labels:
                            if step_index < len(block_steps):
                                st.write(f"**Langkah:** {label}")
                                step_data = block_steps[step_index]['state']
                                state_matrix = [[0 for _ in range(4)] for _ in range(4)]
                                for i in range(4):
                                    for j in range(4):
                                        state_matrix[j][i] = step_data[i * 4 + j]
                                display_matrix(state_matrix)
                                step_index += 1
        
        # Final ciphertext
        st.write("### Final Ciphertext")
        ciphertext_hex = ciphertext.hex().upper()
        st.success("Enkripsi berhasil dilakukan!")
        st.write("Ciphertext (Hex):")
        st.code(ciphertext_hex, language="plaintext")
        
        # Show block-by-block ciphertext
        st.write("Ciphertext by Block:")
        for i in range(0, len(ciphertext), 16):
            block_hex = ciphertext[i:i+16].hex().upper()
            st.write(f"Block {i//16 + 1}: `{block_hex}`")

if __name__ == "__main__":
    main()