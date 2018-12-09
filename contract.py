from boa.interop.System.Runtime import Log
from boa.interop.System.Storage import Put, GetContext, Get, Delete
from boa.interop.Ontology.Native import Invoke
from boa.builtins import ToScriptHash, state, concat

ctx = GetContext()

OntContract = ToScriptHash("AFmseVrdL9f9oyCzZefL9tG6UbvhUMqNMV")

TRANSACTIONS_KEYS = ["sender_address", "receiver_address", "amount", "message"]

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
        ShowPreschools()
    elif operation == 'ShowPreschoolIds':
        ShowPreschoolIds();
    elif operation == 'ShowPreschoolNames':
        ShowPreschoolNames()
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
    elif operation == 'ShowChildmindersByPreschoolId':
        preschoolId = args[0]
        ShowChildmindersByPreschoolId(preschoolId)
    elif operation == 'IsParentBelongsToPreschool':
        preschoolId = args[0]
        parentAddress = args[1]
        IsParentBelongsToPreschool(preschoolId, parentAddress)
    elif operation == 'IsChildminderBelongsToPreschool':
        preschoolId = args[0]
        childminderAddress = args[1]
        IsChildminderBelongsToPreschool(preschoolId, childminderAddress)
    elif operation == 'SendTokenAndMessage':
        senderAddress = args[0]
        receiverAddress = args[1]
        amount = args[2]
        message = args[3]
        SendTokenAndMessage(senderAddress, receiverAddress, amount, message)
    elif operation == 'ShowTransactions':
        childminderAddress = args[0]
        ShowTransactions(childminderAddress)

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
    info = { 'id': id_, 'name': name, 'budget_per_month': 10 }
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
    info_list = GetValueWithDefault("Preschools", [])
    Notify(Serialize(info_list))

def ShowPreschoolIds():
    info_list = GetValueWithDefault("Preschools", [])
    id_list = []
    for info in info_list:
        id_list.append(info['id'])
    Notify(id_list)

def ShowPreschoolNames():
    info_list = GetValueWithDefault("Preschools", [])
    name_list = []
    for info in info_list:
        name_list.append(info['name'])
    Notify(name_list)

def AddParentToPreschool(preschoolId, parentAddress):
    info_list = GetValueWithDefault("ParentToPreschool", [])
    info = { 'preschool_id': preschoolId, 'parent_address': parentAddress }
    info_list.append(info)
    PutValue("ParentToPreschool", info_list)
    Notify(info_list)

def RemoveParentFromPreschool(preschoolId, parentAddress):
    info_list = GetValueWithDefault("ParentToPreschool", [])
    for info in info_list:
        if (info['preschool_id'] == preschoolId) and (info['parent_address'] == parentAddress):
            info_list.remove(info)
    PutValue("ParentToPreschool", info_list)

def AddChildminderToPreschool(preschoolId, childminderAddress):
    info_list = GetValueWithDefault("ChildminderToPreschool", [])
    info = { 'preschool_id': preschoolId, 'childminder_address': childminderAddress }
    info_list.append(info)
    PutValue("ChildminderToPreschool", info_list)
    Notify(Serialize(info_list))

def RemoveChildminderFromPreschool(preschoolId, childminderAddress):
    info_list = GetValueWithDefault("ChildminderToPreschool", [])
    for info in info_list:
        if (info['preschool_id'] == preschoolId) and (info['childminder_address'] == childminderAddress):
            info_list.remove(info)
    PutValue("ChildminderToPreschool", info_list)

def ShowChildmindersByPreschoolId(preschoolId):
    info_list = GetValueWithDefault("ChildminderToPreschool", [])
    Notify(Serialize(info_list))
    id_list = []
    for info in info_list:
        if info['preschool_id'] == preschoolId:
            id_list.append(info['childminder_address'])
    Notify(id_list)

def IsParentBelongsToPreschool(preschoolId, parentAddress):
    info_list = GetValueWithDefault("ParentToPreschool", [])
    for info in info_list:
        if (info['preschool_id'] == preschoolId) and (info['parent_address'] == parentAddress):
            Notify("True")
            return
    Notify("False")

def IsChildminderBelongsToPreschool(preschoolId, childminderAddress):
    info_list = GetValueWithDefault("ChildminderToPreschool", [])
    for info in info_list:
        if (info['preschool_id'] == preschoolId) and (info['childminder_address'] == childminderAddress):
            Notify("True")
            return
    Notify("False")

def SendTokenAndMessage(senderAddress, receiverAddress, amount, message):
    param = state(senderAddress, receiverAddress, amount)
    res = Invoke(1, OntContract, 'transfer', [param])
    if res and res == b'\x01':
        info_list = GetValueWithDefault("Transactions", [TRANSACTIONS_KEYS])
        info = [senderAddress, receiverAddress, amount, message]
        info_list.append(info)
        PutValue("Transactions", info_list)

        Notify('True')
        return True
    else:
        Notify('False')
        return False

def ShowTransactions(childminderAddress):
    info_list = GetValueWithDefault("Transactions", [TRANSACTIONS_KEYS])
    Notify(info_list)
    return True
