from aiohttp.web import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema, json_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        email = self.data["email"]
        admin = await self.store.admins.get_by_email(email)
        if not admin:
            raise HTTPForbidden

        password = self.data["password"]
        if not admin.is_password_valid(password):
            raise HTTPForbidden

        raw_admin = AdminSchema().dump(admin)

        session = await new_session(self.request)
        session["admin"] = raw_admin

        return json_response(raw_admin)


class AdminCurrentView(AuthRequiredMixin, View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        return json_response(AdminSchema().dump(self.request.admin))
