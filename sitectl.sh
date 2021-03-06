#!/usr/bin/env bash
set -o errexit

SCRIPT_DIR=$(dirname $0)
SCRIPT_NAME=$(basename $0)
PYTHON_VENV_DIR=${SCRIPT_DIR}/.venv

if [[ $# -eq 0 ]]; then
  echo "Usage: ${SCRIPT_NAME} {init|upgrade|run|upload}"
  echo "       ${SCRIPT_NAME} <command in Python venv>"
  echo "PYTHON_VENV_DIR: ${PYTHON_VENV_DIR}"
  exit
fi

case "$1" in
  init)
    rm -rf ${PYTHON_VENV_DIR}
    python3 -m venv ${PYTHON_VENV_DIR}
    rm -rf ${SCRIPT_DIR}/custom_extensions/__pycache__
    ;;

  upgrade)
    source ${PYTHON_VENV_DIR}/bin/activate
    pip3 install --upgrade pip
    pip3 install --upgrade setuptools
    pip3 install --upgrade mkdocs
    pip3 install --upgrade mkdocs-material    # theme: https://squidfunk.github.io/mkdocs-material/
    pip3 install --upgrade mkdocs-awesome-pages-plugin    # plugin: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin
    # Install custom Python-Markdown extensions and their dependencies
    pip3 install --upgrade bs4    # custom_extensions.arithmatex_generic 的 dependency
    PYTHON_VENV_SITEPACKAGES_DIR=$(python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')
    if [[ ! -e ${PYTHON_VENV_SITEPACKAGES_DIR}/custom_extensions ]]; then
      ln -s $(realpath --relative-to="${PYTHON_VENV_SITEPACKAGES_DIR}" ${SCRIPT_DIR}/custom_extensions) ${PYTHON_VENV_SITEPACKAGES_DIR}
    fi
    ;;

  run)
    source ${PYTHON_VENV_DIR}/bin/activate
    mkdocs serve
    ;;

  upload)
    source ${PYTHON_VENV_DIR}/bin/activate
    echo "=============== Pushing website to GitHub Pages ====================="
    mkdocs gh-deploy --site-dir /tmp/jisa0224.github.io-mkdocs-site --force --remote-name https://github.com/jisa0224/jisa0224.github.io --remote-branch master
    echo ""
    echo "=============== Pushing website source code to GitHub ==============="
    git checkout dev
    git add --all
    git commit -m "update website"
    git push --force https://github.com/jisa0224/jisa0224.github.io dev:dev
    ;;

  *)
    source ${PYTHON_VENV_DIR}/bin/activate
    $@
    ;;
esac

# 不需要 deactivate，因為 source 的作用範圍只有這個 shell script
