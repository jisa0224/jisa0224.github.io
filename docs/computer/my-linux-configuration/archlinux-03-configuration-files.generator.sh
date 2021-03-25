#!/usr/bin/env bash

# 這個備份 scirpt 所在的資料夾
BASEDIR=$(dirname "$0")

DOC="${BASEDIR}/archlinux-03-configuration-files.md"

writeFile() {
    fileName=$1
    fileType=$2
    echo '##' "${fileName/~/\~}" >> $DOC
    echo                         >> $DOC
    echo '```' "$fileType"       >> $DOC
    cat "$fileName"              >> $DOC
    echo '```'                   >> $DOC
    echo                         >> $DOC
}

echo '# Arch Linux (三) 設定檔' > $DOC
echo '' >> $DOC
echo '這裡放置一些太長沒辦法放在主要文章裡的設定檔。' >> $DOC
echo '' >> $DOC
writeFile ~/.envars shell
writeFile ~/.bash_profile shell
writeFile ~/.bashrc shell
writeFile ~/Desktop/root.desktop
writeFile ~/Desktop/home.desktop
writeFile ~/Desktop/trash.desktop
writeFile ~/.local/share/templates/empty-file.desktop
writeFile ~/.config/fontconfig/fonts.conf XML
writeFile ~/.config/nvim/init.vim