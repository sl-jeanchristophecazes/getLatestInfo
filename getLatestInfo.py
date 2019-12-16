"""Permet de générer une requête SQL correspondant aux dernières mises à jour des annonces entre deux dates 
"""

# Helper function
def makeCustomQueryLines(tableName,dateStart,dateEnd,ListCol):
    """Fonction support pour la fonction principale makeCustomQuery.
    
    Arguments:
        tableName {str} -- Nom de la table sur laquelle on fait la requête
        dateStart {str} -- Date de départ au format YYYY/MM/DD
        dateEnd {str} -- Date limite au format YYYY/MM/DD
        ListCol {list[str]} -- Liste contenant les noms des colonnes sélectionnées. Le premier élément de la liste 
        est la colonne sur laquelle la jointure est faite.
    """    
    
    A_table = "a_{}".format(tableName)
    B_table = "b_{}".format(tableName)

    selectTableAColLine = ''
    selectOriginalTable = ''
    
    for col in ListCol:
        atoAppend = A_table + '.' + col 
        originaltoAppend = tableName + '.' + col 
        selectTableAColLine = selectTableAColLine + ', ' + atoAppend
        selectOriginalTable = selectOriginalTable + ', ' + originaltoAppend

    selectTableAColLine = selectTableAColLine[2:]
    selectOriginalTable = selectOriginalTable[2:]
    innerJoinCol = ListCol[0]

    joinOnLine = "{0}.{2} = {1}.{2} AND {0}.datemaj = {1}.datemaj".format(A_table,B_table,innerJoinCol)
    
    return(selectTableAColLine,selectOriginalTable,joinOnLine,innerJoinCol,A_table,B_table)



def makeCustomQuery(DBName,tableName,dateStart,dateEnd,ListCol):
    """A partir des arguments, renvoie un str correspondant à la requête à effectuer
    
    Arguments:
        DBName {str} -- Nom de la base de données sur laquelle on fait la requête
        tableName {str} -- Nom de la table sur laquelle on fait la requête
        dateStart {str} -- Date de départ au format YYYY/MM/DD
        dateEnd {str} -- Date limite au format YYYY/MM/DD
        ListCol {list[str]} -- Liste contenant les noms des colonnes sélectionnées. Le premier élément de la liste 
        est la colonne sur laquelle la jointure est faite.
    """    
    customLines = makeCustomQueryLines(tableName,dateStart,dateEnd,ListCol)
    selectTableAColLine = customLines[0]
    selectOriginalTable = customLines[1]
    joinOnLine = customLines[2]
    innerJoinCol = customLines[3]
    A_table = customLines[4]
    B_table = customLines[5]

    with open('sqlSnippetTemplate','r') as file:
        query = file.read()

    query = query.format(selectTableAColLine,selectOriginalTable,joinOnLine,\
                            innerJoinCol,tableName,dateStart,dateEnd,A_table,B_table,DBName)

    return(query)

if __name__ == "__main__":
    print("Voici un exemple \n")
    print("makeCustomQuery('annonce_revision','2019-10-15','2019-11-01',['idannonce','cp','adresse']) renvoie: ")

    query = makeCustomQuery('annonce_revision','2019-10-15','2019-11-01',['idannonce','cp','adresse'])
    print(query)

    with open('testQuery','w') as file:
        file.write(query)