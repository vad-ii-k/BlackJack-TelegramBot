from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminAuthRequestSchema, AdminResponseSchema
from app.auth.decorators import auth_required
from app.web.app import View
from app.web.utils import json_response


class AdminLoginView(View):
    @docs(tags=["admin"], summary="Admin login")
    @request_schema(AdminAuthRequestSchema)
    @response_schema(AdminResponseSchema, 200)
    async def post(self):
        email, password = self.data["email"], self.data["password"]
        admin_db = await self.store.admins.get_by_email(email)
        if not (admin_db and admin_db.is_password_valid(password)):
            raise HTTPForbidden

        session = await new_session(request=self.request)
        response_data = AdminResponseSchema().dump(admin_db)
        session["admin_data"] = response_data
        return json_response(data=response_data)


class AdminCurrentView(View):
    @auth_required
    @docs(tags=["admin"], summary="Get info about current admin")
    @response_schema(AdminResponseSchema, 200)
    async def get(self):
        admin = self.request.admin
        return json_response(data=AdminResponseSchema().dump(admin))
