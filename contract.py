from boa.interop.System.Runtime import Log
from boa.interop.System.Storage import Put, GetContext, Get, Delete

ctx = GetContext()

def Main(operation, args):
    if operation == 'CreatePreschool':
        name = args[0]
        CreatePreschool(name)
    elif operation == 'DeletePreschool':
        preschoolId = args[0]
        DeletePreschool(preschoolId)
    elif operation == 'GetPreschoolName':
        preschoolId = args[0]
        GetPreschoolName(preschoolId)
    elif operation == 'ShowPreschools':
        return ShowPreschools()
    elif operation == 'AddParentToPreschool':
        preschoolId = args[0]
        parentAddress = args[1]
        AddParentToPreschool(preschoolId, parentAddress)
    elif operation == 'RemoveParentFromPreschool':
        preschoolId = args[0]
        parentAddress = args[1]
        RemoveParentFromPreschool(preschoolId, parentAddress)
    elif operation == 'AddChildminderToPreschool':
        preschoolId = args[0]
        childminderAddress = args[1]
        AddChildminderToPreschool(preschoolId, childminderAddress)
    elif operation == 'RemoveChildminderFromPreschool':
        preschoolId = args[0]
        childminderAddress = args[1]
        RemoveChildminderFromPreschool(preschoolId, childminderAddress)
        
    return False


def GetValueWithDefault(key, default):
    k = Get(ctx, key)
    if k is None:
        return default
    else:
        return Deserialize(k)

def PutValue(key, value):
    s = Serialize(value)
    Put(ctx, key, s)
    return s


def CreatePreschool(name):
    info_list = GetValueWithDefault("Preschools", [])
    id_ = len(info_list) + 1
    info = { 'id': id_, 'name': name, 'budget_per_month': 10}
    info_list.append(info)
    PutValue("Preschools", info_list)
    Notify(id_)

def DeletePreschool(preschoolId):
    Delete(ctx, preschoolId)

def GetPreschoolName(preschoolId):
    info_list = GetValueWithDefault("Preschools", [])
    for info in info_list:
        if info['id'] == preschoolId:
            Notify(info['name'])

def ShowPreschools():
    info_list = GetValueWithDefault("Preschools")
    return info_list

def AddParentToPreschool(preschoolId, parentAddress):
    info_list = GetValueWithDefault("ParentToPreschool", [])
    info = { 'preschool_id': preschoolId, 'parent_address': parentAddress }
    info_list.append(info)
    PutValue(info_list)

def RemoveParentFromPreschool(preschoolId, parentAddress):
    info_list = GetValueWithDefault("ParentToPreschool", [])
    for info in info_list:
        if (info['preschool_id'] == preschoolId) and (info['parent_address'] == parentAddress):
            info_list.remove(info)

def AddChildminderToPreschool(preschoolId, childminderAddress):
    info_list = GetValueWithDefault("ChildminderToPreschool", [])
    info = { 'preschool_id': preschoolId, 'childminder_address': childminderAddress }
    info_list.append(info)
    PutValue(info_list)

def RemoveChildminderFromPreschool(preschoolId, childminderAddress):
    info_list = GetValueWithDefault("ChildminderToPreschool", [])
    for info in info_list:
        if (info['preschool_id'] == preschoolId) and (info['childminder_address'] == childminderAddress):
            info_list.remove(info)

def isParentBelongsToPreschool(preschoolId, parentAddress):
    info_list = GetValueWithDefault("ParentToPreschool", [])
    for info in info_list:
        if (info['preschool_id'] == preschoolId) and (info['parent_address'] == parentAddress):
            return True
    return False

def isChildminderBelongsToPreschool(preschoolId, childminderAddress):
    info_list = GetValueWithDefault("ChildminderToPreschool", [])
    for info in info_list:
        if (info['preschool_id'] == preschoolId) and (info['childminder_address'] == childminderAddress):
            return True
    return False


