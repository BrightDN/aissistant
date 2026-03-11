from functions.get_file_content import get_file_content

print("Result for lorem.txt:")
print(get_file_content("calculator", "lorem.txt"))


print("Result for 'main.py' calculator:")
print(get_file_content("calculator", "main.py"))

print("Result for 'pkg' calculator:")
print(get_file_content("calculator", "pkg/calculator.py"))

print("Result for '/bin/cat' directory:")
print(get_file_content("calculator", "/bin/cat"))

print("Result for non existing file:")
print(get_file_content("calculator", "pkg/does_not_exist.py"))