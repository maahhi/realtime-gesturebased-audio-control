import json
X_true = []

with open('01-armraise-39samples.json', 'r') as file:
    data = json.load(file)
    print(len(data))
    for i in range(len(data)):
        RwristX = data[i]["Rwrist"]["x"]
        RwristY = data[i]["Rwrist"]["y"]
        RwristZ = data[i]["Rwrist"]["z"]
        Rwrist = [RwristX, RwristY, RwristZ]
        print(len(Rwrist[0]))

        RelbowX = data[i]["Relbow"]["x"]
        RelbowY = data[i]["Relbow"]["y"]
        RelbowZ = data[i]["Relbow"]["z"]
        Relbow = [RelbowX, RelbowY, RelbowZ]

        RshoulderX = data[i]["Rshoulder"]["x"]
        RshoulderY = data[i]["Rshoulder"]["y"]
        RshoulderZ = data[i]["Rshoulder"]["z"]
        Rshoulder = [RshoulderX, RshoulderY, RshoulderZ]

        X_true.append([Rwrist, Relbow, Rshoulder])


with open('02-armrais-45samples.json', 'r') as file:
    data = json.load(file)
    print(len(data))
    for i in range(len(data)):
        RwristX = data[i]["Rwrist"]["x"]
        RwristY = data[i]["Rwrist"]["y"]
        RwristZ = data[i]["Rwrist"]["z"]
        Rwrist = [RwristX, RwristY, RwristZ]
        print(len(Rwrist[0]))

        RelbowX = data[i]["Relbow"]["x"]
        RelbowY = data[i]["Relbow"]["y"]
        RelbowZ = data[i]["Relbow"]["z"]
        Relbow = [RelbowX, RelbowY, RelbowZ]

        RshoulderX = data[i]["Rshoulder"]["x"]
        RshoulderY = data[i]["Rshoulder"]["y"]
        RshoulderZ = data[i]["Rshoulder"]["z"]
        Rshoulder = [RshoulderX, RshoulderY, RshoulderZ]

        X_true.append([Rwrist, Relbow, Rshoulder])

X_false = []
with open('01-nonarmrais-34samples.json', 'r') as file:
    data = json.load(file)
    print(len(data))
    for i in range(len(data)):
        RwristX = data[i]["Rwrist"]["x"]
        RwristY = data[i]["Rwrist"]["y"]
        RwristZ = data[i]["Rwrist"]["z"]
        Rwrist = [RwristX, RwristY, RwristZ]
        print(len(Rwrist[0]))

        RelbowX = data[i]["Relbow"]["x"]
        RelbowY = data[i]["Relbow"]["y"]
        RelbowZ = data[i]["Relbow"]["z"]
        Relbow = [RelbowX, RelbowY, RelbowZ]

        RshoulderX = data[i]["Rshoulder"]["x"]
        RshoulderY = data[i]["Rshoulder"]["y"]
        RshoulderZ = data[i]["Rshoulder"]["z"]
        Rshoulder = [RshoulderX, RshoulderY, RshoulderZ]

        X_false.append([Rwrist, Relbow, Rshoulder])

with open('02-nonarmrais-50samples.json', 'r') as file:
    data = json.load(file)
    print(len(data))
    for i in range(len(data)):
        RwristX = data[i]["Rwrist"]["x"]
        RwristY = data[i]["Rwrist"]["y"]
        RwristZ = data[i]["Rwrist"]["z"]
        Rwrist = [RwristX, RwristY, RwristZ]
        print(len(Rwrist[0]))

        RelbowX = data[i]["Relbow"]["x"]
        RelbowY = data[i]["Relbow"]["y"]
        RelbowZ = data[i]["Relbow"]["z"]
        Relbow = [RelbowX, RelbowY, RelbowZ]

        RshoulderX = data[i]["Rshoulder"]["x"]
        RshoulderY = data[i]["Rshoulder"]["y"]
        RshoulderZ = data[i]["Rshoulder"]["z"]
        Rshoulder = [RshoulderX, RshoulderY, RshoulderZ]

        X_false.append([Rwrist, Relbow, Rshoulder])

print(len(X_true))
print(len(X_false))

"""
with open('X_true.json', 'w') as file:
    json.dump(X_true, file)

with open('X_false.json', 'w') as file:
    json.dump(X_false, file)
"""



