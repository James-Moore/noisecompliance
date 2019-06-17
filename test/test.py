import uuid

val = uuid.uuid4()
print(val)
valstr = str(val)
print(valstr)
val2 = uuid.UUID(valstr)
print(val2)
print(str(val2))