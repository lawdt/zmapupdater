import re
string = "AP170_3b:d4\nsauna\nC8-B5-AD-C8-3B-D4\nChannels: 48, 1\ntest"
print(string)
print("-------------------")
string = re.sub(r'Channels:.*\n','', string)
string = re.sub(r'Channels:.*','', string)
print(string)
