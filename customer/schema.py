import graphene
from bson import ObjectId
from .db import customers_collection

# Object type
class CustomerType(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    email = graphene.String()

# Query (READ)
class Query(graphene.ObjectType):
    customer = graphene.Field(CustomerType, id=graphene.String(required=True))
    customers = graphene.List(CustomerType)

    def resolve_customers(root, info):
        docs = customers_collection.find()
        return [
            {"id": str(d["_id"]), "name": d["name"], "email": d["email"]}
            for d in docs
        ]

    def resolve_customer(root, info, id):
        c = customers_collection.find_one({"_id": ObjectId(id)})
        if not c:
            return None
        return {"id": str(c["_id"]), "name": c["name"], "email": c["email"]}


# Mutations (CREATE, UPDATE, DELETE)
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    customer = graphene.Field(CustomerType)

    def mutate(root, info, name, email):
        new_doc = {"name": name, "email": email}
        result = customers_collection.insert_one(new_doc)
        new_doc["_id"] = result.inserted_id
        return CreateCustomer(
            customer={"id": str(new_doc["_id"]), "name": name, "email": email}
        )


class UpdateCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String()
        email = graphene.String()

    customer = graphene.Field(CustomerType)

    def mutate(root, info, id, name=None, email=None):
        update_fields = {}
        if name:
            update_fields["name"] = name
        if email:
            update_fields["email"] = email

        customers_collection.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
        updated = customers_collection.find_one({"_id": ObjectId(id)})
        return UpdateCustomer(
            customer={
                "id": str(updated["_id"]),
                "name": updated["name"],
                "email": updated["email"],
            }
        )


class DeleteCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        result = customers_collection.delete_one({"_id": ObjectId(id)})
        return DeleteCustomer(ok=result.deleted_count > 0)


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    update_customer = UpdateCustomer.Field()
    delete_customer = DeleteCustomer.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
