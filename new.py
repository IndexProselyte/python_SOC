sda = 9
sa = f"niggae: {sda}"

rem = len(sa) - 77
if rem != 0:
    sa = f"niggae: {sda}" + f" " * (rem*-1)


with open("nwww.txt", "rb") as file:
    line1 = file.read(64)
    print(line1)
    print(len(line1), end="")