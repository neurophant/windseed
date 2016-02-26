from windseed.apps.admin.urls import routes as admin_routes
from windseed.apps.web.urls import routes as web_routes


routes = admin_routes + web_routes
