# Define the Unicode range for Bengali characters
bengali_range = (int('0980', 16), int('09FF', 16))

# Generate a list of Bengali characters
bengali_characters = [chr(char_code) for char_code in range(bengali_range[0], bengali_range[1] + 1)]

# Join all Bengali characters into a single string
bengali_string = ''.join(bengali_characters)

# Print the string of Bengali characters
print(bengali_string)
