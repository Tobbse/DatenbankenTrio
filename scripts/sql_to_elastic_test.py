# Tried to send SQL statements directly to Elastic using normal JSON contain the SQL statements.
# This is somehow possible using the SQL Elastics Beta feature but doesn't work yet.



from elasticsearch import Elasticsearch as Elastic

es = Elastic([{'host': 'localhost', 'port': 9200}])
print("Elastic running: " + str(es.ping()))


def handle_statement(statement):
    transformed_statement = "POST /_datenbanken_test1/test1\n{\n   \"query\": " + indent_statement(statement) + "\n}"
    return transformed_statement


def indent_statement(statement):
    lines = statement.split("\n")
    indented_lines = []
    is_first = True
    for line in lines:
        if is_first:
            indented_lines.append(line + "\n")
            is_first = False
        else:
            indented_lines.append(' ' * 9 + line + "\n")
    return ''.join(indented_lines)


with open("createKursRel.txt") as sql_file:
    raw_sql_statements = sql_file.read().split(';')

es_statements = []
for raw_line in raw_sql_statements:
    sql_statement = raw_line.strip()
    transformed_statement = handle_statement(sql_statement)
    es_statements.append(transformed_statement)
    print(transformed_statement)
    print("____________________________________________________________________________________________")

for es_statement in es_statements:
    es.index(es_statement)
