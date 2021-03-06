from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Proyecto:
    # home:
    url(r'^$', 'alojamientos.views.homeTemp'),
    url(r'^default.css$', 'alojamientos.views.StyleV'),
    url(r'^fonts.css/$', 'alojamientos.views.StylefontV'),
    url(r'^images/(.*\.jpg)$', 'django.views.static.serve',\
       {'document_root': 'templates/images/'}),
    # about:
    url(r'^about$', 'alojamientos.views.about'),
    # loggin/loggout:
    url(r'^login$','alojamientos.views.loginV'),
    url(r'^logout$','alojamientos.views.logoutV'),
    # favicon:
    url(r'^favicon.ico/$', 'alojamientos.views.faviconV'),
    # alojamientosV:
    url(r'^alojamientos/$', 'alojamientos.views.alojamientosTempV'),
    # alojamientoIdV:
    url(r'^alojamientos/(.*)/(.*)', 'alojamientos.views.alojamientoIdLengTempV'),
    url(r'^alojamientos/(.*)', 'alojamientos.views.alojamientoIdTempV'),
    # admin:
    url(r'^admin/', include(admin.site.urls)),
    # xmlV:
    url(r'^xml/(.*)', 'alojamientos.views.xmlV'),
    # seleccion:
    url(r'^sel/(.*)/(.*)', 'alojamientos.views.seleccion'),
    # usuariosV:
    url(r'^(.*)/(.*)', 'alojamientos.views.usuariosTempV'),  # User Vs Default404
)
