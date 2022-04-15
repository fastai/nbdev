#!/bin/bash

set -e

LATEST_VER=`curl -s https://api.github.com/repos/quarto-dev/quarto-cli/releases/latest | grep tag_name | cut -d v -f 2 | tr -d \",`
CURRENT_VER=`quarto -V || true`

if [[ $CURRENT_VER == *"not found"*  ]]; then
	echo "Quarto is not installed."
	INSTALL_QUARTO=1;
elif [[ "$LATEST_VER" > "$CURRENT_VER" ]]; then
    echo "You have Quarto version ${CURRENT_VER}. The latest available version is ${LATEST_VER}."
	INSTALL_QUARTO=1;
elif [[ "$LATEST_VER" == "$CURRENT_VER" ]]; then
    echo "Your version of Quarto ${CURRENT_VER} is the latest version."
	INSTALL_QUARTO=0;
fi

install_linux() {
		echo "...installing Quarto"
		wget -nv https://www.quarto.org/download/latest/quarto-linux-amd64.deb
		sudo dpkg -i *64.deb
		rm *64.deb
}

install_mac() {
		echo "...opening installer for Quarto"
		wget -nv https://www.quarto.org/download/latest/quarto-macos.pkg
		open quarto-macos.pkg
}

if [[ "$INSTALL_QUARTO" -eq 1 ]]; then
	case "$OSTYPE" in
	linux*)   install_linux ;;
	darwin*)  install_mac ;;
	*)        echo "make sure you install the latest version of quarto: https://quarto.org/docs/get-started/" ;;
	esac
fi
