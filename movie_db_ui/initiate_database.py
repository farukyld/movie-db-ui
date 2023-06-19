from movieDB.databaseManagement.serverInteractors.startUp import createTables, insertInitialRecords

if __name__ == '__main__':
    s1, names1 =createTables()
    s2, names2 =insertInitialRecords()
    if s1: 
        print("tables created reading: {}".format(names1))
    else: print("tables coudlnt created")
    if s2:
        print("initial records inserted reading: {}".format(names1))
    else: print("initial records coulnt created")