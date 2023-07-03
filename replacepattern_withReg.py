import re

file_path = 'regex.txt'  # Replace with the path to your Python file

# Read the content of the file
file = open(file_path, 'r')
content = file.read()
file.close()

# Replace the desired line
pattern = r'PKG_SOURCE_COMMITID = .+'  # Pattern to match "A = " followed by any characters
new_line = 'PKG_SOURCE_COMMITID = 2f4cf9fca3172f56cf96f6efbc0fa146ca08e4f9'  # New line to replace the matched line
modified_content = re.sub(pattern, new_line, content)

# Write the modified content back to the file
file = open(file_path, 'w')
file.write(modified_content)
file.close()
