file_ = open('requirements.txt', 'r')

line = file_.readline()
packages = []
while line:
    print(line)
    
    line = file_.readline()
print(packages)
