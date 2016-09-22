# -*- coding: utf-8 -*-
"""
    flask_jsonschema
    ~~~~~~~~~~~~~~~~

    flask_jsonschema
"""

import os
import warnings

from functools import wraps

from flask import current_app, request, json
from jsonschema import ValidationError, validate as _validate


class _JsonSchema(object):
    def __init__(self, schemas):
        self._schemas = schemas

    def get_schema(self, path):
        rv = self._schemas[path[0]]
        for p in path[1:]:
            rv = rv[p]
        return rv


class JsonSchema(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self._state = self.init_app(app)

    def init_app(self, app):
        default_dir = os.path.join(app.root_path, 'jsonschema')
        schema_dir = app.config.get('JSONSCHEMA_DIR', default_dir)
        schemas = {}
        for fn in os.listdir(schema_dir):
            key = fn.split('.')[0]
            fn = os.path.join(schema_dir, fn)
            if os.path.isdir(fn) or not fn.endswith('.json'):
                continue
            with open(fn) as f:
                schemas[key] = json.load(f)
        state = _JsonSchema(schemas)
        app.extensions['jsonschema'] = state
        return state

    def validate(self, *path):
        warnings.warn('the `JsonSchemea.validate` function is deprecated. Please use the '
                      'module level `flask_jsonschema.validate` function instead.',
                      PendingDeprecationWarning)

        def wrapper(fn):
            @wraps(fn)
            def decorated(*args, **kwargs):
                jschema = current_app.extensions.get('jsonschema', None)
                if jschema is None:
                    raise RuntimeError('Flask-JsonSchema was not properly initialized for the '
                                       'current application: %s' % current_app)
                _validate(request.json, jschema.get_schema(path))
                return fn(*args, **kwargs)
            return decorated
        return wrapper

    def __getattr__(self, name):
        return getattr(self._state, name, None)


def validate(*path):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            jschema = current_app.extensions.get('jsonschema', None)
            if jschema is None:
                raise RuntimeError('Flask-JsonSchema was not properly initialized for the '
                                   'current application: %s' % current_app)
            _validate(request.json, jschema.get_schema(path))
            return fn(*args, **kwargs)
        return decorated
    return wrapper


