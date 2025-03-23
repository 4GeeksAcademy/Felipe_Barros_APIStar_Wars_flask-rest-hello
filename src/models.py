from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Integer, Float, ForeignKey, Boolean, Enum, Text
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)   
    is_active = Column(Boolean, default=True, nullable=False)     
    
    #Relación con Favorites
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    #
    #Apuntes cascade="all, delete-orphan"
    #Indicamos qué debe pasar con los objetos relacionados cuando se elimina un objeto padre.
    #all = Atajo que agrupa varios tipos de cascada a la vez
    #       cascade="
    #           save-update[Si el objeto padre se guarda o actualiza, sus hijos también lo harán], 
    #           merge[Permite que los hijos sean fusionados cuando el padre lo sea], 
    #           expunge[Si el padre es eliminado de la sesion de SQLAlchemy, los hijos se eliminan automáticamente], 
    #           delete[Si el padre es eliminado, los hijos se eliminan automáticamente], 
    #           delete-orphan[Si un objeto hijo pierde su referencia al objeto padre, será eliminado automáticamente]**, 
    #           refresh-expire[Si el padre se recarga desde la BBDD, también se recargan los hijos]";
    #


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "is_active": self.is_active,
        }
    
class Favorite(db.Model):
    __tablename__ = "favorite"  
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicle.id"), nullable=True) 
    character_id = Column(Integer, ForeignKey("character.id"), nullable=True) 
    specie_id = Column(Integer, ForeignKey("specie.id"), nullable=True)
    planet_id = Column(Integer, ForeignKey("planet.id"), nullable=True)

    #Creación de restricciones de unicidad compuesta (UniqueConstraint):
    #Esto genera que un usuario no tenga duplicados en sus favoritos
    __table_args__ = (
        db.UniqueConstraint('user_id', 'vehicle_id', name='unique_user_vehicle'),
        db.UniqueConstraint('user_id', 'character_id', name='unique_user_character'),
        db.UniqueConstraint('user_id', 'specie_id', name='unique_user_specie'),
        db.UniqueConstraint('user_id', 'planet_id', name='unique_user_planet'),
        db.CheckConstraint(
            #Aseguramos que al menos una columna tenga un valor
            "(COALESCE(vehicle_id, character_id, specie_id, planet_id) IS NOT NULL)",
            name="check_at_least_one_favorite"
        )
    )
#      Apuntes COALESCE***
#       Función de SQL que retorna el primer valor no NULL de una lista de valores. Si todos los valores son NULL, retorna NULL.
#
    #Relación inversa con User
    user = relationship("User", back_populates="favorites")

    #Relación inversa con Planet
    planet = relationship("Planet", back_populates="favorites")

    #Relación inversa con Character
    character = relationship("Character", back_populates="favorites")

    #Relación inversa con Vehicle
    vehicle = relationship("Vehicle", back_populates="favorites")

    #Relación inversa con Specie
    specie = relationship("Specie", back_populates="favorites")


          


    def serialize(self):
        return {   
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id,
            "character_id": self.character_id,
            "specie_id": self.specie_id,
            "planet_id": self.planet_id,
            }
    
class Planet(db.Model):
    __tablename__ = "planet" 
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    diameter = Column(Float, nullable=False)
    gravity = Column(Float, nullable=False)
    population = Column(Integer, nullable=False)
    climate = Column(String(100), nullable=False)
    terrain = Column(String(100), nullable=False)

    #Relación con Favorites
    favorites = relationship("Favorite", back_populates="planet", cascade="all, delete-orphan")

    def serialize(self):
        return {    
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            }
    
class Character(db.Model):
    __tablename__ = "character" 
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    birth_year = Column(String(100), nullable=False)
    gender = Column(Enum('male', 'female', 'unknown', 'n/a', name='gender_types'), nullable=False)
    hair_color = Column(String(100), nullable=False)
    height = Column(Float, nullable=False)
    mass = Column(Float, nullable=False)
    skin_color = Column(String(100), nullable=False)
    homeworld = Column(String(100), nullable=False) 

    #Relación con Favorites
    favorites = relationship("Favorite", back_populates="character", cascade="all, delete-orphan")

    def serialize(self):
        return {   
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "homeworld": self.homeworld,
            }
    
class Vehicle(db.Model):
    __tablename__ = "vehicle" 
    id = Column(Integer, primary_key=True, autoincrement=True)  
    name = Column(Text, nullable=False)
    model = Column(Text, nullable=False)
    vehicle_class = Column(String(100), nullable=False)
    manufacturer = Column(String(100), nullable=False)
    crew = Column(Integer, nullable=False)
    passengers = Column(Integer, nullable=False)
    max_atmosphering_speed = Column(Float, nullable=False)
    cargo_capacity = Column(Integer, nullable=False)
    consumables = Column(String(100), nullable=False)

    #Relación con Favorites
    favorites = relationship("Favorite", back_populates="vehicle", cascade="all, delete-orphan")

    def serialize(self):
        return {   
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            }
        
class Specie(db.Model):
    __tablename__ = "specie"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(Text, nullable=False) 
    classification = Column(String(100), nullable=False)
    designation = Column(Text, nullable=False)
    skin_colors = Column(String(100), nullable=False)
    language = Column(String(100), nullable=False)
    homeworld = Column(String(100), nullable=False)

    #Relación con Favorites
    favorites = relationship("Favorite", back_populates="specie", cascade="all, delete-orphan")

    def serialize(self):
        return {     
            "id": self.id,
            "name": self.name,
            "classification": self.classification,
            "designation": self.designation,
            "skin_colors": self.skin_colors,
            "language": self.language,
            "homeworld": self.homeworld,
            }
    


#   **          Objeto padre: Es el objeto que contiene una lista de objetos hijos.
#                Objeto hijo: Es un objeto que pertenece a un padre mediante una relación relationship().
#       Perder la referencia: Un hijo "pierde" a su padre cuando ya no está en la lista de hijos del padre 
#                             o cuando la clave foránea (ForeignKey) que lo relaciona con el padre se vuelve NULL.
#                   Ejemplos:
#                       a) {Eliminación del padre} Si se borra un User, sus Favorite también serán eliminados
#                       b) {Se elimina referencia en la relación} Si se quita manualmente un Favorite de la lista de favorites del User,
#                                                                 el Favorite se eliminará automáticamente de la BBDD
#                       c) {Se pierde la referencia de la Foreingkey} Si cambiamos la user_id de Favorite a None, también se elimina el registro.
#
#
#   *** Sintaxis:
#           COALESCE(valor1, valor2, valor3, ..., valorN)
#               - Recorre los valor de izquierda a derecha
#               - Devuelve el primer valor no NULL
#           Por lo tanto, cuando:
#               "(COALESCE(vehicle_id, character_id, specie_id, planet_id) IS NOT NULL)",
#                name="check_at_least_one_favorite"
#           Nos estamos asegurando de que por lo menos una columna tenga un valor y que si todos los datos son NULL
#           la BBDD rechazará la inserción ya que no tendría sentido guardar un favorito sin relación cun un vehicle_id,
#           character_id, specie_id o planet_id
#