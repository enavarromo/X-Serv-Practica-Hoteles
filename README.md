# X-Serv-Practica-Hoteles
Repositorio para la práctica final de SARO/SAT. Curso 2015-2016 



Nombre: Eloy Navarro Morales

Titulación: Sistemas de Telecomunicación

Nombre de Usuario en GitHub: enavarromo

Peculiaridades:
    1) Inicialmente desconocía que la base de datos del portal de Madrid no se
    actualizaba practicamente nunca, por tanto no implementé un boton que dirigiese
    a la actualización de las bases de datos, sino que diseñé la aplicación para que
    en cada llamada a home ("Get /") descargase el .xml y contrastase contra un .xml
    en disco. En caso de existir diferencias entre ambos (o sencillamente no
    existir un .xml propio) la aplicación borra lo existente en las bases de datos
    y realiza en parseo y almacenamiento de nuevo. Sabiendo que no se actualizan,
    esta funcionalidad es practicamete inutil, incluso molesta al obligar la
    descarga del .xml en cada llamada a home, pero aun así la dejo, ya que es la
    encargada del parse y del almacenamiento inicial en sql.

Funcionalidades Opcionales: Ninguna

URL del vídeo de funcionalidad básica: [URL_a_Funcionalidad_Básica](https://www.youtube.com/watch?v=2XMKPqCFe3Y)


