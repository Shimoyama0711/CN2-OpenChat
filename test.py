from room import Room

rooms = {}

room_number = "1325"

print("####################")
print(f"rooms = {rooms}")
print("####################")

room_test = Room(room_number, 3, 60, 2, 1, 0)
print("####################")
print(f"room_test = {room_test}")
print("####################")


rooms[room_number] = room_test
print("####################")
print(f"rooms = {rooms}")
print("####################")
