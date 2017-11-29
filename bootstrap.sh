#!/bin/bash
VENV_NAME=${1:-"env"}
WORKSPACE=${WORKSPACE:-$PWD}
VENV_PATH=$WORKSPACE/${VENV_NAME}
PROJECT_NAME=`find . -not -path '*/\.*' -iname settings.py | cut -d \/ -f 2`
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal

create_venv() {
    if [ ! -d "${VENV_PATH}" ]; then
        echo "Creating a new virtual environment..."
        virtualenv -p python3.6 ${VENV_NAME}
    fi
    # The virtualenv has been created with success?
    if [ $? != 0 ]; then
        echo "Somethings went wrong! Try again!"
        rm ${VENV_PATH} -rf
        return -1
    fi
}

validate_venv() {
    # Sanity check
    if [[ (! -f ${VENV_PATH}/bin/python) || (! -f ${VENV_PATH}/bin/activate) ]]; then
        echo "The virtualenv has been corrupted. Try again!"
        rm ${VENV_PATH} -rf
        return -1
    fi
}

install_deps() {
    source ${VENV_PATH}/bin/activate && {
        pip install -r development.txt
    }
}

create_dotenv() {
    if [ ! -d ".env" ]; then
        echo DEBUG=True > .env
    fi
}

create_venv && {
    validate_venv && {
        install_deps
        create_dotenv
    }
}
