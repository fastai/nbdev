#!/bin/bash
set -e
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

case "$OSTYPE" in
linux*)   install_linux ;;
darwin*)  install_mac ;;
*)        echo "make sure you install the latest version of quarto: https://quarto.org/docs/get-started/" ;;
esac