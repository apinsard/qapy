# -*- coding: utf-8 -*-
"""Watch SASS and CoffeeScript on runserver.
Patch runserver to run the sass and coffeescript compilers automatically.
Credits to https://gist.github.com/EmilStenstrom/4761479
"""

import atexit
import subprocess

from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import \
    Command as RunserverCommand


class Command(RunserverCommand):
    active_processes = []

    def _run_shell_cmd(self, cmd):
        self.stdout.write("Running command: {}".format(cmd))
        proc = subprocess.Popen([cmd], shell=True, stdin=subprocess.PIPE,
                                stdout=self.stdout, stderr=self.stderr)
        self.active_processes.append(proc)

    def inner_run(self, *args, **options):
        dirname = settings.BASE_DIR.child('ui', 'static', 'ui')
        self._run_shell_cmd(
            "sass --watch {0}/sass:{0}/css".format(dirname))
        self._run_shell_cmd(("coffee --watch "
                             "--output {0}/js/ "
                             "--compile {0}/coffee/").format(dirname))
        super().inner_run(*args, **options)

    def exit(self):
        for proc in self.active_processes:
            proc.terminate()

    def __init__(self, *args, **kwargs):
        atexit.register(self.exit)
        return super().__init__(*args, **kwargs)
