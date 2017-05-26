import sqlite3
from custom_object import Table, ToDo

class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]

class DBHelper(object):
    """Database helper"""
    def __init__(self, db):
        self.db = db
        self.__init_database()

    def __init_database(self):
        conn = sqlite3.connect(self.db)
        conn.execute('''create table if not exists ''' + Table.to_do + '''(
            ''' + ToDo.id + '''  INTEGER PRIMARY KEY,
            ''' + ToDo.priority + '''  TEXT NOT NULL,
            ''' + ToDo.email + '''  TEXT NOT NULL,
            ''' + ToDo.task + '''  TEXT NOT NULL)''')
        conn.commit()
        conn.close()

    def delete_todo(self, id):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()

        c.execute(\
            'DELETE FROM {} where {} {} ?'.format(Table.to_do, ToDo.id, '>' if id == 0 else '='),\
            (str(id)))
        conn.commit()
        conn.close()

    def insert_todo(self, email, priority, task):
        if priority is not None and email is not None and task is not None:
            conn = sqlite3.connect(self.db)
            c = conn.cursor()
            c.execute(\
                'INSERT INTO {} ({}, {}, {}) VALUES (?, ?, ?)'\
                .format(Table.to_do, ToDo.email, ToDo.priority, ToDo.task),\
                (email, priority, task))
            conn.commit()
            conn.close()

    def update_todo(self, id, email, priority, task):
        if id is not None and priority is not None and email is not None and task is not None:
            conn = sqlite3.connect(self.db)
            c = conn.cursor()
            c.execute(\
                'UPDATE {} set {} = ?, {} = ?, {} = ? where id = ?'\
                .format(Table.to_do, ToDo.email, ToDo.priority, ToDo.task),\
                (email, priority, task, id))
            conn.commit()
            conn.close()

    def select_todos(self):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute('SELECT * FROM {}'.format(Table.to_do))
        res = c.fetchall()
        conn.close()
        return list(map(lambda x: ToDo(x), res))

    def select_todo(self, id):
        if id is not None:
            conn = sqlite3.connect(self.db)
            c = conn.cursor()
            c.execute('SELECT * FROM {} where {} = ?'.format(Table.to_do, ToDo.id), (str(id)))
            res = c.fetchone()
            conn.close()
            return ToDo(res) if res is not None else None


