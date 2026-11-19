from sqlalchemy import create_engine, event, text


def make_engine(url):
    if not url.startswith('mysql+pymysql://'):
        raise RuntimeError('This project requires the configured XAMPP/MariaDB database.')
    engine = create_engine(url, isolation_level='READ COMMITTED', hide_parameters=True, pool_pre_ping=True, pool_recycle=300, pool_size=10,
                           connect_args={'connect_timeout': 5,'read_timeout':5,'write_timeout':5}, echo=False)
    @event.listens_for(engine, 'connect')
    def utc_connection(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        cursor.execute("SET time_zone = '+00:00'")
        cursor.close()
    return engine


def one(connection, sql, **parameters):
    return connection.execute(text(sql), parameters).mappings().first()


def all_rows(connection, sql, **parameters):
    return connection.execute(text(sql), parameters).mappings().all()


def execute(connection, sql, **parameters):
    return connection.execute(text(sql), parameters)
