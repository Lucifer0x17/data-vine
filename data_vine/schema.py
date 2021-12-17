def getType(substr):
    if substr.find('char') != -1:
        return 'string'
    if substr.find('int') == 0:
        return 'int'
    elif substr.find('int') > 0:
        return 'long'
    if substr.find('float') == 0:
        return 'float'
    if substr.find('double') == 0:
        return 'double'
    if substr.find('date') == 0:
        return 'date'


def getAvsc(columnTuple, tableName):
    schemaJson = {
        "namespace": "database",
        "type": "record",
        "name": "",
        "fields": []
    }
    fieldList = []
    schemaJson["name"] = tableName
    for eachColumn in columnTuple:
        # print(eachColumn["Type"])
        dType = getType(eachColumn["Type"])
        if eachColumn["Null"] == "NO":
            fieldList.append({
                "name": eachColumn["Field"], "type": dType})
        else:
            fieldList.append({
                "name": eachColumn["Field"], "type": [dType, "null"]})
    schemaJson["fields"] = fieldList
    return schemaJson
