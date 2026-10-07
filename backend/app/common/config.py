class Config:
    # Ajusta tu usuario, contraseña y nombre de base de datos
    USER = 'root'
    PASSWORD = ''
    HOST = 'localhost'
    DATABASE = 'gestor_contrasena'

    # URL de conexión para SQLAlchemy usando PyMySQL
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False