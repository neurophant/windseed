from windseed.apps.admin import handlers


login = r'/admin/login/'
logout = r'/admin/logout/'
dashboard = r'/admin/'
records = r'/admin/records/'

routes = [
    (login+'?', handlers.LoginHandler),
    (logout+'?', handlers.LogoutHandler),
    (dashboard+'?', handlers.DashboardHandler),
    (records+'?', handlers.RecordsHandler), ]
