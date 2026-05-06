Servidor de Simulación Evolutiva
================================

.. toctree::
   :maxdepth: 2
   :caption: Contenidos:

   README
   GEMINI

Arquitectura
============
El proyecto utiliza una arquitectura hexagonal dividida en:

* **Dominio**: Entidades y lógica pura.
* **Aplicación**: Casos de uso y servicios.
* **Infraestructura**: Adaptadores para base de datos y API web.

Módulos
=======

.. automodule:: application.use_cases.simulation_service
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: domain.entities.models
   :members:
   :undoc-members:
   :show-inheritance:
