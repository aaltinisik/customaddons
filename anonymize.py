#!/usr/bin/env python
#-*- encoding: utf8 -*-

import os
import sys
import argparse
import psycopg2
from psycopg2.psycopg1 import cursor as psycopg1cursor
import datetime
from itertools import groupby
from operator import itemgetter
import pickle
import random

__version__ = '0.1'

PRINT_INCREMENT = 1000

EXIT_FILE_NOT_FOUND = 2
EXIT_DB_NOT_FOUND = 3
EXIT_ABORTED_BY_USER = 4
EXIT_UNSTABLE_STATE = 5
EXIT_INVALID_FIELD_TYPE = 7
EXIT_FILE_ALREADY_EXISTS = 8


class LoggingCursor(psycopg1cursor):
    def execute(self, query, vars=None):
        def pack_whitespace(str):
            new_str = str.replace('  ', ' ')
            if new_str == str:
                return new_str
            else:
                return pack_whitespace(new_str)
        # END pack_whitespace.

        if not isinstance(query, (basestring)):
            raise Exception("execute: first argument should be string or unicode, you supplied a %s instead" % (type(query)))

        if vars is None:
            q = pack_whitespace(self.mogrify(query).strip().replace('\n', ' '))
        else:
            q = pack_whitespace(self.mogrify(query, vars).strip().replace('\n', ' '))

        sys.stdout.write(q+'\n')

        try:
            res = super(LoggingCursor, self).execute(query, vars)
        except:
            raise
        return res


class AnonymizationManager(object):
    def __init__(self, args):
        self.args = args
        self.cr = self._get_cursor()

    def _get_cursor(self):
        try:
            connect_string = " ".join(["%s=%s" % (arg, getattr(self.args, arg)) for arg in ['dbname', 'user', 'password', 'host', 'port'] if getattr(self.args, arg)])
            conn = psycopg2.connect(connect_string)
        except psycopg2.OperationalError, e:
            msg = "Error: {0}\n".format(e)
            sys.stderr.write(msg)
            sys.exit(EXIT_DB_NOT_FOUND)
        if self.args.verbose:
            return conn.cursor(cursor_factory=LoggingCursor)
        else:
            return conn.cursor(cursor_factory=psycopg1cursor)

    def group(self, lst, cols):
        if isinstance(cols, basestring):
            cols = [cols]
        return dict((k, [v for v in itr]) for k, itr in groupby(sorted(lst, key=itemgetter(*cols)), itemgetter(*cols)))

    def column_exists(self, table, column):
        self.cr.execute("SELECT count(1)"
            " FROM pg_class c, pg_attribute a"
            " WHERE c.relname=%s"
            " AND c.oid=a.attrelid"
            " AND a.attname=%s", [table, column])
        return self.cr.fetchone()[0]

    def run(self):
        try:
            self.cr.execute('BEGIN')
            self._run()
        except:
            sys.stderr.write('Error -> rollbacking\n')
            self.cr.execute('ROLLBACK')
            raise
        else:
            if self.args.dry_run:
                sys.stderr.write('Dry run mode -> rollbacking\n')
                self.cr.execute('ROLLBACK')
            else:
                self.cr.execute('COMMIT')

    def _run(self):
        if self.args.action in ('a', 'anonymize'):
            self.anonymize_database()
        else:
            self.reverse_anonymize_database()

    def anonymize_database(self):
        # create a new history record:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        vals = [
            now,
            now,
            'started',
            'clear -> anonymized',
        ]
        sql_insert_history = "insert into ir_model_fields_anonymization_history (create_uid, create_date, date, state, direction) values (1, %s, %s, %s, %s) returning id"
        self.cr.execute(sql_insert_history, vals)

        history_id, = self.cr.fetchone()

        # check that all the defined fields are in the 'clear' state
        self.cr.execute("select field_name from ir_model_fields_anonymization where state = 'anonymized'")
        invalid = self.cr.fetchall()
        if invalid:
            fields = ', '.join([r[0] for r in invalid])
            msg = "All existing anonymisation fields should be in the 'clear' state. These fields are in the 'anonymized' state: {0}\n".format(fields)
            sys.stderr.write(msg)
            sys.exit(EXIT_UNSTABLE_STATE)

        # do the anonymization:
        dirpath = os.environ.get('HOME') or os.getcwd()
        rel_filepath = 'field_anonymization_{0}_{1}.pickle'.format(self.args.dbname, history_id)
        abs_filepath = os.path.abspath(os.path.join(dirpath, rel_filepath))
        if os.path.exists(abs_filepath):
            msg = "Anonymization file {0} already exists\n"
            sys.stderr.write(msg)
            sys.exit(EXIT_FILE_ALREADY_EXISTS)

        self.cr.execute("select * from ir_model_fields_anonymization where state <> 'not_existing'")
        fields = self.cr.dictfetchall()

        if not fields:
            msg = "No fields to anonymize.\n"
            self.stdout.write(msg)

        data = []

        self.cr.execute("select id, model from ir_model")
        model_names_by_id = dict([(r[0], r[1]) for r in self.cr.fetchall()])
        self.cr.execute("select * from ir_model_fields")
        fields_by_id = dict([(r['id'], r) for r in self.cr.dictfetchall()])

        len_fields = len(fields)
        i1 = 0
        for anon_field in fields:
            i1+=1
            model_name = model_names_by_id.get(anon_field['model_id'])
            field = fields_by_id.get(anon_field['field_id'])
            field_name = field['name']
            field_type = field['ttype']
            table_name = model_name.replace('.', '_')

            # get the current value
            if not self.column_exists(table_name, field_name):
                msg = "field {0} in table {1} does not exist, setting it as 'not existing'\n".format(field_name, table_name)
                sys.stderr.write(msg)
                self.cr.execute("update ir_model_fields_anonymization set state = 'not_existing' where id = %s", [anon_field['field_id']])
                continue

            sql = "select id, %s from %s" % (field_name, table_name)
            self.cr.execute(sql)
            records = self.cr.dictfetchall()
            len_records = len(records)
            i2 = 0
            for record in records:
                i2+=1
                if not i2 % PRINT_INCREMENT or i2 == len_records:
                    m = "{table}.{field}: f: {i1}/{len_fields}), r: {i2}/{len_records}\n".format(table=table_name, field=field_name, i1=i1, i2=i2, len_fields=len_fields, len_records=len_records)
                    sys.stderr.write(m)

                data.append({"model_id": model_name, "field_id": field_name, "id": record['id'], "value": record[field_name]})

                # anonymize the value:
                anonymized_value = None

                sid = str(record['id'])
                if field_type == 'char':
                    anonymized_value = 'xxx'+sid
                elif field_type == 'selection':
                    anonymized_value = 'xxx'+sid
                elif field_type == 'text':
                    anonymized_value = 'xxx'+sid
                elif field_type == 'boolean':
                    anonymized_value = random.choice([True, False])
                elif field_type == 'date':
                    anonymized_value = '2011-11-11'
                elif field_type == 'datetime':
                    anonymized_value = '2011-11-11 11:11:11'
                elif field_type == 'float':
                    anonymized_value = 0.0
                elif field_type == 'integer':
                    anonymized_value = 0
                elif field_type in ['binary', 'many2many', 'many2one', 'one2many', 'reference']: # cannot anonymize these kind of fields
                    msg = "Cannot anonymize fields of these types: binary, many2many, many2one, one2many, reference.\n"
                    sys.stderr.write(msg)
                    sys.exit(EXIT_INVALID_FIELD_TYPE)

                sql = "update %(table)s set %(field)s = %%(anonymized_value)s where id = %%(id)s" % {
                    'table': table_name,
                    'field': field_name,
                }
                self.cr.execute(sql, {
                    'anonymized_value': anonymized_value,
                    'id': record['id']
                })

        # save pickle:
        fn = open(abs_filepath, 'w')
        pickle.dump(data, fn, pickle.HIGHEST_PROTOCOL)

        anonfilename = os.path.expanduser(self.args.anonfilename)
        if os.path.exists(anonfilename):
            get_anonfilename = lambda base, i, ext: '{base}_{i}{ext}'.format(base=base, i=i, ext=ext)
            i = 1
            base, ext = os.path.splitext(anonfilename)
            anonfilename = get_anonfilename(base=base, i=i, ext=ext)
            while os.path.exists(anonfilename):
                print anonfilename
                i += 1
                anonfilename = get_anonfilename(base=base, i=i, ext=ext)
            msg = "Error: file {} already exist. Renaming it to {}\n".format(self.args.anonfilename, anonfilename)
            sys.stderr.write(msg)

        fn = open(anonfilename, 'w')
        pickle.dump(data, fn, pickle.HIGHEST_PROTOCOL)

        # update the anonymization fields:
        self.cr.execute("update ir_model_fields_anonymization set state = 'anonymized' where state = 'clear'")

        # add a result message in the wizard:
        msgs = ["Anonymization successful.",
               "",
               "Do not forget to save the resulting file to a safe place because you will not be able to revert the anonymization without this file.",
               "",
               "This file is also stored in the {0} directory. The absolute file path is: {1}.",
               "",
              ]
        msg = '\n'.join(msgs).format(dirpath, abs_filepath)
        sys.stdout.write(msg)

        # update the history record:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg = "Successfully reversed the anonymization.\n"
        vals = {
            'write_date': now,
            'date': now,
            'id': history_id,
            'msg': msg,
        }
        sql_update_history = """update ir_model_fields_anonymization_history set
                                  write_uid = 1,
                                  write_date = %(write_date)s,
                                  date = %(date)s,
                                  filepath = NULL,
                                  msg = %(msg)s,
                                  state = 'done'
                                where id = %(id)s"""
        self.cr.execute(sql_update_history, vals)

    def reverse_anonymize_database(self):
        # create a new history record:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        vals = [
            now,
            now,
            'started',
            'anonymized -> clear',
        ]
        sql_insert_history = "insert into ir_model_fields_anonymization_history (create_uid, create_date, date, state, direction) values (1, %s, %s, %s, %s) returning id"
        self.cr.execute(sql_insert_history, vals)

        history_id, = self.cr.fetchone()

        # check that all the defined fields are in the 'anonymized' state
        self.cr.execute("select field_name from ir_model_fields_anonymization where state = 'clear'")
        invalid = self.cr.fetchall()
        if invalid:
            fields = ', '.join([r[0] for r in invalid])
            msg = "All existing anonymisation fields should be in the 'anonymized' state. These fields are in the 'clear' state: {0}\n".format(fields)
            sys.stderr.write(msg)
            sys.exit(EXIT_UNSTABLE_STATE)

        anonfilename = os.path.expanduser(self.args.anonfilename)
        if not os.path.isfile(anonfilename):
            msg = "Could not find file: {0}".format(anonfilename)
            sys.stderr.write(msg)
            sys.exit(EXIT_FILE_NOT_FOUND)

        data = pickle.load(open(anonfilename))

        sql_get_custom_fixes = """select * from ir_model_fields_anonymization_migration_fix where target_version = %s"""
        self.cr.execute(sql_get_custom_fixes, [self.args.target])
        fixes = self.cr.dictfetchall()
        fixes = self.group(fixes, ('model_name', 'field_name'))

        len_data = len(data)
        i = 0
        for line in data:
            i+=1
            queries = []
            table_name = line['model_id'].replace('.', '_') if line['model_id'] else None

            if not i % PRINT_INCREMENT or i == len_data:
                t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                m = "{0} - l: {1}/{2}, t: {3}\n".format(t, i, len_data, table_name)
                sys.stderr.write(m)

            # check if custom sql exists:
            key = (line['model_id'], line['field_id'])
            custom_updates = fixes.get(key)
            if custom_updates:
                custom_updates.sort(key=itemgetter('sequence'))
                queries = [(record['query'], record['query_type']) for record in custom_updates if record['query_type']]
            elif table_name:
                queries = [("update %(table)s set %(field)s = %%(value)s where id = %%(id)s" % {
                    'table': table_name,
                    'field': line['field_id'],
                }, 'sql')]

            for query in queries:
                try:
                    if query[1] == 'sql':
                        sql = query[0]
                        print ":::::::::::::::::::", query, line['value'], line['id']
                        self.cr.execute(sql, {
                            'value': line['value'],
                            'id': line['id']
                        })
                    elif query[1] == 'python':
                        raw_code = query[0]
                        code = raw_code % line
                        eval(code)
                    else:
                        raise Exception("Unknown query type '{0}'. Valid types are: sql, python.".format(query['query_type']))
                except Exception as exc:
                    print "Error when processing line: {!r}".format(line)
                    raise exc

        # update the anonymization fields:
        self.cr.execute("update ir_model_fields_anonymization set state = 'clear' where state <> 'not_existing'")

        # update the history record:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg = "Successfully reversed the anonymization.\n"
        vals = {
            'write_date': now,
            'date': now,
            'id': history_id,
            'msg': msg,
        }
        sql_update_history = """update ir_model_fields_anonymization_history set
                                  write_uid = 1,
                                  write_date = %(write_date)s,
                                  date = %(date)s,
                                  filepath = NULL,
                                  msg = %(msg)s,
                                  state = 'done'
                                where id = %(id)s"""
        self.cr.execute(sql_update_history, vals)

        sys.stdout.write(msg)


def _get_args(required):
    def _add_required_args(required):
        # required args:
        g1 = parser.add_argument_group("required arguments")
        g1.add_argument('+a', '+action', metavar="ACTION", required=required, choices=['a', 'anonymize', 'r', 'reverse_anonymize'],
                        help="Action (anonymize or a, reverse_anonymize or r)", dest='action',
                       )
        g1.add_argument('+d', '+db', metavar="DBNAME", required=required,
                        help="Database name", dest='dbname',
                       )
        g1.add_argument('+f', '+file', metavar="ANONYMIZATION_FILE", required=required,
                        help="Anonymization file", dest='anonfilename',
                       )
        g1.add_argument('+t', '+target', metavar="ODOO_VERSION", required=required,
                        help="Version of Odoo", dest='target', choices=['7.0', '8.0', '9.0']
                       )
    # END _add_required_args

    parser = argparse.ArgumentParser(prefix_chars='-+', add_help=False)

    _add_required_args(required)

    # options:
    g2 = parser.add_argument_group("optional arguments")
    g2.add_argument('--dry-run', default=False,
                    help="Dry run mode, do not commit anything in db.", dest="dry_run",
                    action='store_true')
    g2.add_argument('-v', '--verbose',
                    help="Displays executed SQL queries.", dest="verbose",
                    action='store_true')
    g2.add_argument('-V', '--version',
                    help="Show this program version and exit.", dest="vers",
                    action='store_true')
    g2.add_argument('-h', '--help',
                    help="Show this help message and exit.", dest="help",
                    action='store_true')

    g3 = parser.add_argument_group("database connection options")
    g3.add_argument('--user', help="Database User", action='store', metavar='USER')
    g3.add_argument('--password', help="Database password", action='store', metavar='PASSWORD')
    g3.add_argument('--host', help="Host (server address)", action='store', metavar='HOST')
    g3.add_argument('--port', help="Database port", action='store', metavar='PORT')

    args = parser.parse_args()
    return args, parser


def _main():
    args, parser = _get_args(required=False)

    if args.help:
        parser.print_help()
    elif args.vers:
        sys.stdout.write(parser.prog+' '+__version__+'\n')
        sys.stdout.flush()
    else:
        args, parser = _get_args(required=True)
        app = AnonymizationManager(args)
        try:
            app.run()
        except KeyboardInterrupt:
            msg = "\nAborted by user.\n"
            sys.stderr.write(msg)
            sys.exit(EXIT_ABORTED_BY_USER)


if __name__ == '__main__':
    _main()

