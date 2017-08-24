import pymysql

from smsurvey.core.model.data_type import DataType
from smsurvey.core.model.query.where import Where


class Model:

    repository = None
    dao = None

    @classmethod
    def from_database(cls, _dao):
        cls.dao = _dao

        show_table_sql = "SHOW TABLES;"
        describe_table_sql = "DESCRIBE "

        connection = cls.dao.get_connection()

        try:
            models = {}

            with connection.cursor() as cursor:
                cursor.execute(show_table_sql)
                tables = cursor.fetchall()

                for table in tables:
                    table_name = table[0]

                    cursor.execute(describe_table_sql + table_name)
                    table_description = cursor.fetchall()
                    models[table_name + "s"] = cls._Model.from_description(table_description, table_name)

        finally:
            connection.close()

        cls.repository = cls.__ModelRepository(models)

    class __ModelRepository:

        def __init__(self, models_dictionary):
            self.__dict__ = models_dictionary

    class _Model:

        def __init__(self, table_name, columns):
            columns_copy = dict(columns)
            self.__dict__ = columns
            self.columns = columns_copy
            self.table_name = table_name

        @classmethod
        def from_description(cls, description, table_name):
            columns = {}

            for column_description in description:
                column_name = column_description[0]
                columns[column_name] = cls.__Column.from_tuple(column_description)

            return cls(table_name, columns)

        def select(self, inner_join=None, where=None):
            sql = "SELECT * FROM " + self.table_name
            connection = Model.dao.get_connection()

            try:
                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    if inner_join is not None:
                        sql += " INNER JOIN " + inner_join.build()

                    if where is not None:
                        sql += " WHERE " + where.build()

                    cursor.execute(sql)

                    results = cursor.fetchall()

                    if len(results) == 1:
                        return self.__ModelInstance.from_dict(self, results[0])
                    elif len(results) > 1:
                        instances = []

                        for result in results:
                            instances.append(self.__ModelInstance.from_dict(self, result))

                        return instances

                    return None
            finally:
                connection.close()

        def delete(self, where):
            sql = "DELETE FROM "
            connection = Model.dao.get_connection()

            try:
                with connection.cursor() as cursor:
                    if where is None:
                        cursor.execute(sql + self.table_name)
                    else:
                        cursor.execute(sql + self.table_name + " WHERE " + where.build())

                    connection.commit()
            finally:
                connection.close()

        def validate_column(self, column_name, value):
            column = self.columns[column_name]
            data_type = column.data_type
            try:
                data_type.validate(value)
            except ValueError as e:
                raise ValueError(column_name + ": " + str(e))

        def create(self):
            cs = {}

            for key in self.columns:
                    cs[key] = self.columns[key].default

            return self.__ModelInstance.from_create(self, cs)

        class __ModelInstance:

            def __init__(self, model, columns_dict):
                self.__dict__ = columns_dict
                self.__columns_dict = columns_dict
                self.model = model
                self.__new = True

            @classmethod
            def from_dict(cls, model, result_dict):
                mi = cls(model, result_dict)
                mi.__new = False
                return mi

            @classmethod
            def from_create(cls, model, columns_dict):
                mi = cls(model, columns_dict)
                mi.__new = True
                return mi

            def save(self):
                for key in self.model.columns:
                    self.model.validate_column(key, self.__dict__[key])

                if self.__new:
                    return self.save_new()
                else:
                    return self.save_update()

            def save_new(self):
                columns, values = self.get_column_tuples()
                sql = "INSERT INTO " + self.model.table_name + " " + columns + " VALUES %s"

                connection = Model.dao.get_connection()

                try:
                    with connection.cursor() as cursor:
                        cursor.execute(sql, [values])

                        connection.commit()
                        new_row_id = cursor.lastrowid
                finally:
                    connection.close()

                return self.model.select(Where(self.model.id, Where.EQUAL, new_row_id))

            def save_update(self):

                instr = ''
                for key in self.model.columns:
                    instr += key + " = " + self.parse_value(self.__dict__[key]) + ', '

                instr = instr[:-2]

                sql = "UPDATE " + self.model.table_name + " SET " + instr + " WHERE id = %s"

                connection = Model.dao.get_connection()

                try:
                    with connection.cursor() as cursor:
                        cursor.execute(sql, self.__dict__['id'])
                        connection.commit()
                        updated_row_id = cursor.lastrowid
                finally:
                    connection.close()

                return self.model.select(Where(self.model.id, Where.EQUAL, updated_row_id))



            @staticmethod
            def parse_value(value):
                if isinstance(value, str):
                    return "'" + value + "'"

                if isinstance(value, list) or isinstance(value, set) or isinstance(value, tuple):
                    s = '('

                    for i in value:
                        s += Where.format_second_clause(i) + ', '

                    return s[:-2] + ')'

                return str(value)

            def get_column_tuples(self):
                columns, values = [], []
                for key in self.model.columns:
                        columns.append(key)
                        values.append(self.__dict__[key])

                column_string = "("
                for column in columns:
                    column_string += column + ', '

                column_string = column_string[:-2] + ')'
                return column_string, values

        class __Column:

            def __init__(self, column_name, data_type, unique, default):
                self.column_name = column_name
                self.data_type = data_type
                self.unique = unique
                self.default = default

            @classmethod
            def from_tuple(cls, column_tuple):
                column_name = column_tuple[0]
                required = column_tuple[2] == 'NO' and column_tuple[5].find('auto_increment') == -1
                data_type = DataType.from_db(column_tuple[1], required)

                if column_tuple[3] == 'UNI' or column_tuple[3] == 'PRI':
                    unique = True
                else:
                    unique = False

                default = column_tuple[4]

                return cls(column_name, data_type, unique, default)