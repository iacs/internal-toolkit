#!/usr/bin/env python3
# coding: utf-8
#
#  __     ______     ______     __  __     ______
# /\ \   /\  __ \   /\  ___\   /\ \/\ \   /\  ___\
# \ \ \  \ \  __ \  \ \ \____  \ \ \_\ \  \ \___  \
#  \ \_\  \ \_\ \_\  \ \_____\  \ \_____\  \/\_____\
#   \/_/   \/_/\/_/   \/_____/   \/_____/   \/_____/
#
# Librarian 3.1.1
# SN: 151008
#
# Iago Mosquera
# Script para automatizar tareas de mantenimiento
# * Clasificación de archivos
# * Limpieza de archivos temporales
#
# Versión python.
# Configurado para WSL
#

import os
import subprocess
import json
import logging
import logging.handlers

__author__ = 'Iago Mosquera'

FILE_SETTINGS = "settings.json"
FILE_LOG = "librarian.log"
ENCODING = "utf-8"

settings = {}
log = ""


def main():
    global settings
    global log

    settings = _loadData(FILE_SETTINGS)
    log = _setupLogger(FILE_LOG)

    _createBoxroomDirs()
    _moveVaultToBoxroom()
    _sortBoxroom()
    _deleteTmp()

    log.info("Librarian - ejecucion finalizada")
    print("Finalizado")


def _loadData(filepath):
    location = os.path.dirname(os.path.realpath(__file__))
    abspath = os.path.join(location, filepath)
    data = {}
    with open(abspath, 'r', encoding='utf-8') as datafile:
        data = json.load(datafile)
    return data


def _moverArchivos(lista, destino):
    if len(lista) >= 1:
        for line in lista:
            subprocess.call(['mv', '-n', line, destino])
            log.info("Moviendo archivo: {0}".format(line))
        print("movidos {} archivos a {}".format(len(lista), destino))


def _clasificarPorRegex(regex):
    trastero = settings['dir_boxroom']
    result = subprocess.check_output([
        'find',
        trastero,
        '-maxdepth', '1',
        '-type', 'f',
        '-regextype', 'posix-awk',
        '-iregex', regex
    ])

    return result.decode(ENCODING).split('\n')


def _getBoxPath(boxname):
    trastero = settings['dir_boxroom']

    return os.path.join(trastero, boxname)


def _setupLogger(logFileName):
    dir_logs = settings['dir_logs']

    if not (os.path.exists(dir_logs)):
        os.makedirs(dir_logs)

    log = logging.getLogger('librarian')
    formatter = logging.Formatter(
        fmt='{asctime} [{levelname}] - {message}', style='{')
    fileHandler = logging.handlers.RotatingFileHandler(os.path.join(dir_logs, logFileName),
                                                       'a', 1048576, 10)

    fileHandler.setFormatter(formatter)
    log.setLevel(logging.INFO)
    log.addHandler(fileHandler)

    return log


def _createBoxroomDirs():
    dir_boxroom = settings['dir_boxroom']

    for box in settings['boxroom']:
        path = os.path.join(dir_boxroom, box['name'])
        if not os.path.exists(path):
            os.makedirs(path)
            log.info("Creando directorio: {0}".format(path))


def _moveVaultToBoxroom():
    vault = settings['dir_vault']
    trastero = settings['dir_boxroom']
    white_dirs = settings['white_dirs']
    dir_descargas = settings['dir_dls']

    dias_antig = "+" + str(settings['days_old'])

    if os.listdir(vault):
        result = subprocess.check_output(['find', vault, '-maxdepth', '1'])
        mover = result.decode(ENCODING).split('\n')
        if "" in mover:
            mover.remove("")
        if vault in mover:
            mover.remove(vault)
        _moverArchivos(mover, trastero)
    else:
        log.info("Baul vacío. Nada que mover")

    # Mover descargas antiguas
    result = subprocess.check_output([
        'find',
        dir_descargas,
        '-maxdepth', '1',
        '-type', 'f',
        '-mtime', dias_antig,
    ])

    if result:
        mover = result.decode(ENCODING).split('\n')
        if "" in mover:
            mover.remove("")
        _moverArchivos(mover, vault)

    # Mover directorios
    result = subprocess.check_output([
        'find',
        dir_descargas,
        '-maxdepth', '1',
        '-type', 'd',
        '-mtime', dias_antig,
    ])

    if result:
        mover = result.decode(ENCODING).split('\n')
        if "" in mover:
            mover.remove("")
        if dir_descargas in mover:
            mover.remove(dir_descargas)
        for d in white_dirs:
            if os.path.join(dir_descargas, d) in mover:
                mover.remove(os.path.join(dir_descargas, d))
        _moverArchivos(mover, vault)


def _sortBoxroom():
    boxroom = settings['boxroom']
    trastero = settings['dir_boxroom']
    white_dirs = settings['white_dirs']

    for set in boxroom:
        box = _getBoxPath(set['name'])
        regex = ".*\.("
        for ext in set['filetypes'][:-1]:
            regex = regex + ext + "|"
        regex = regex + set['filetypes'][-1] + ")"
        log.debug("Using regex: {0}".format(regex))
        fileList = _clasificarPorRegex(regex)
        if fileList:
            if "" in fileList:
                fileList.remove("")
            _moverArchivos(fileList, box)

    box = _getBoxPath(settings['box_misc'])
    result = subprocess.check_output([
        'find',
        trastero,
        '-maxdepth', '1',
        '-type', 'f',
    ])
    if result:
        mover = result.decode(ENCODING).split('\n')
        if "" in mover:
            mover.remove("")
        _moverArchivos(mover, box)

    result = subprocess.check_output([
        'find',
        trastero,
        '-maxdepth', '1',
        '-type', 'd',
    ])

    if result:
        mover = result.decode(ENCODING).split('\n')
        if "" in mover:
            mover.remove("")
        if trastero in mover:
            mover.remove(trastero)
        for d in white_dirs:
            if os.path.join(trastero, d) in mover:
                mover.remove(os.path.join(trastero, d))
        _moverArchivos(mover, box)


def _deleteTmp():
    dir_tmp = settings['dir_tmp']
    subprocess.call(['rm', '-rf', dir_tmp])
    print("Directorio temporal eliminado")


if __name__ == '__main__':
    main()
