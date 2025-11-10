from django.http import JsonResponse
from graphene import Schema
from .schema import schema
from django.views.decorators.csrf import csrf_exempt


def run_query(query, variables=None):
    result = schema.execute(query, variable_values=variables)
    if result.errors:
        return {"errors": [str(e) for e in result.errors]}
    return result.data


# POST /customer
@csrf_exempt
def create_customer(request):
    if request.method == "POST":
        import json

        body = json.loads(request.body)
        query = """
        mutation($name: String!, $email: String!) {
            createCustomer(name: $name, email: $email) {
                customer { id name email }
            }
        }
        """
        data = run_query(query, {"name": body["name"], "email": body["email"]})
        return JsonResponse(data)


# GET /customer/<id>/read
@csrf_exempt
def read_customer(request, customerId):
    query = """
    query($id: String!) {
        customer(id: $id) { id name email }
    }
    """
    data = run_query(query, {"id": customerId})
    return JsonResponse(data)


# PUT /customer/<id>/update
@csrf_exempt
def update_customer(request, customerId):
    if request.method == "PUT":
        import json

        body = json.loads(request.body)
        query = """
        mutation($id: String!, $name: String, $email: String) {
            updateCustomer(id: $id, name: $name, email: $email) {
                customer { id name email }
            }
        }
        """
        data = run_query(query, {"id": customerId, **body})
        return JsonResponse(data)


# DELETE /customer/<id>/delete
@csrf_exempt
def delete_customer(request, customerId):
    if request.method == "DELETE":
        query = """
        mutation($id: String!) {
            deleteCustomer(id: $id) { ok }
        }
        """
        data = run_query(query, {"id": customerId})
        return JsonResponse(data)
