# Aeropuerto
Proyecto final de mi curso de programación.
Este proyecto consiste en la creación de una aplicación de consola que simula la gestión de un aeropuerto, permitiendo gestionar vuelos, pasajeros y el estado de los vuelos. La aplicación está diseñada para registrar vuelos programados, gestionar los pasajeros asociados a cada vuelo, y permitir la actualización del estado de los vuelos (por ejemplo, si un vuelo está a tiempo, retrasado o cancelado).

# Objetivos.
Gestión de vuelos: Los vuelos pueden ser registrados con detalles como la aerolínea, la fecha, la hora de salida y la duración.
Gestión de pasajeros: Se puede agregar pasajeros a los vuelos, visualizando detalles como el nombre del pasajero, el vuelo asociado y su estado.
Control de estados de los vuelos: Permite actualizar y consultar el estado de los vuelos (a tiempo, retrasado, cancelado).
Interacción con la consola: La aplicación tiene una interfaz de consola que permite al usuario interactuar con el sistema, ingresando datos y consultando información.

# Funcionalidades principales
Registrar un vuelo: Permite registrar un vuelo con información básica como el número de vuelo, la aerolínea, la fecha y hora de salida, y la duración del vuelo.
Registrar un pasajero: Los pasajeros pueden ser registrados y asociados a un vuelo específico. Cada pasajero tiene información como nombre, número de documento y vuelo asignado.
Actualizar el estado de un vuelo: Permite cambiar el estado de un vuelo (a tiempo, retrasado, cancelado), lo cual es crucial para la correcta gestión y notificación de los vuelos.
Consultar vuelos y pasajeros: El sistema permite consultar todos los vuelos programados y los pasajeros asociados a cada vuelo.
Eliminar vuelos y pasajeros: Permite la eliminación de vuelos y pasajeros del sistema en caso de cancelaciones o cambios en la programación.
Estructura del Proyecto
El proyecto está estructurado en varias clases que permiten gestionar distintos aspectos de la operación del aeropuerto:
Clase Vuelo: Representa un vuelo individual. Contiene detalles como el número de vuelo, la aerolínea, la fecha y hora de salida, la duración y el estado del vuelo.
Clase Pasajero: Representa a un pasajero en particular, con detalles como su nombre, número de documento y el vuelo en el que está registrado.
Clase Aeropuerto: Administra los vuelos y los pasajeros, gestionando las operaciones de registro, actualización de estados y eliminación de vuelos o pasajeros.
