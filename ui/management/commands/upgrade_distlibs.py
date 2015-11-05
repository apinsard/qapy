# -*- coding: utf-8 -*-
from io import BytesIO
import json
from urllib.request import urlopen
from zipfile import ZipFile

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Install or upgrade static css/js libs"

    def _unpack_raw(self, conf):
        """Fetch files from direct URL and save them to the tmp directory."""
        if 'include' in conf:
            files = [
                (conf['source'].format(V=conf['version'], F=f), f)
                for f in conf['include']
            ]
        else:
            files = [(conf['source'].format(V=conf['version']), None)]
        for url, output in files:
            if output is not None:
                filename = self._tmp_dir.child(*output.split('/'))
            else:
                filename = self._tmp_dir.child(url.split('/')[-1])
            filename.parent.mkdir(True)
            with urlopen(url) as f:
                filename.write_file(f.read().decode('utf-8'))

    def _unpack_zip(self, conf):
        """Fetch an archive and extract it to the tmp directory."""
        source = conf['source'].format(V=conf['version'])
        with urlopen(source) as f:
            ar = ZipFile(BytesIO(f.read()))
        ar.extractall(self._tmp_dir)

    def _get_files(self, conf):
        """Return a list of couples (temporary file, destination file)."""
        if type(conf['include']) is dict:
            files = []
            for d, subfiles in conf['include'].items():
                d = d.format(V=conf['version'])
                for f in subfiles:
                    files.append(('{}/{}'.format(d, f), f))
        elif type(conf['include']) is list:
            files = [(f, f) for f in conf['include']]
        return files

    def _move_to(self, output_dir, conf):
        """Move temporary files to `output_dir`."""
        output_dir.mkdir(True)
        if 'include' in conf:
            files = self._get_files(conf)
            for tmp_file, lib_file in files:
                self._tmp_dir.child(*tmp_file.split('/')).rename(
                    output_dir.child(*lib_file.split('/')), True)
        else:
            for f in self._tmp_dir.listdir():
                f.move(output_dir)

    def handle(self, *args, **options):
        lib_dir = settings.BASE_DIR.child('ui', 'static', 'lib')
        filename = settings.BASE_DIR.child('ui', 'data', 'distlibs.json')
        with open(filename) as f:
            distlibs = json.loads(f.read())

        lib_dir.rmtree()
        for name, conf in distlibs.items():
            self._tmp_dir = settings.BASE_DIR.child('tmp', name)
            self._tmp_dir.mkdir(True)
            if conf['type'] == 'raw':
                self._unpack_raw(conf)
            elif conf['type'] == 'zip':
                self._unpack_zip(conf)
            self._move_to(lib_dir.child(name), conf)
            if 'rename' in conf:
                for src, dst in conf['rename'].items():
                    lib_dir.child(
                        name, *src.format(V=conf['version']).split('/')
                    ).rename(
                        lib_dir.child(name, *dst.split('/')), True)
