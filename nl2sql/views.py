from django.shortcuts import render
from .gemini_nl2sql import nl2sql_query
from .utils_gemini_prompt import get_schema_with_departments
from django.db import connection

def nl2sql_query_view(request):
    result = None
    sql_query = None
    if request.method == 'POST':
        nl_query = request.POST.get('nl_query')
        schema = get_schema_with_departments()
        sql_query = nl2sql_query(nl_query, schema)
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
    return render(request, 'nl2sql_query.html', {'result': result, 'sql_query': sql_query})