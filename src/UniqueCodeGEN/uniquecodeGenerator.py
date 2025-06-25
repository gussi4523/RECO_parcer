import shortuuid 

def generateUniquecode(lenght):
    code = shortuuid.ShortUUID().random(length=lenght)
    return code