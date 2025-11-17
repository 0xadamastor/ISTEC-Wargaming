#!/bin/bash
# ------------------------------------
# Install or Compile ExifTool Script
# ------------------------------------
clear
echo "======================================"
echo "          INSTALAR EXIFTOOL"
echo "======================================"
echo ""
echo "1) Instalar via repositório oficial"
echo "2) Instalar manualmente via GitHub (versão mais recente)"
echo "0) Sair"
echo ""
read -p "Escolha uma opção: " opcao

# ------------------------------------
# FUNÇÃO: Instala pelo repositório
# ------------------------------------
install_repo() {
    echo "[*] A detectar gestor de pacotes..."
    
    if command -v apt >/dev/null 2>&1; then
        echo "[+] Detectado APT (Debian/Ubuntu)"
        sudo apt update
        sudo apt install -y libimage-exiftool-perl
        
    elif command -v dnf >/dev/null 2>&1; then
        echo "[+] Detectado DNF (Fedora/RHEL)"
        sudo dnf install -y perl-Image-ExifTool
        
    elif command -v pacman >/dev/null 2>&1; then
        echo "[+] Detectado Pacman (Arch/Manjaro)"
        
        # Verificar se yay está disponível
        if command -v yay >/dev/null 2>&1; then
            echo "[+] AUR helper (yay) detectado!"
            echo ""
            echo "Escolha o método de instalação:"
            echo "1) pacman (repositório oficial)"
            echo "2) yay (AUR - pode ter versão mais recente)"
            echo ""
            read -p "Opção [1-2]: " aur_choice
            
            case $aur_choice in
                1)
                    echo "[*] A instalar via pacman..."
                    sudo pacman -Sy --noconfirm exiftool
                    ;;
                2)
                    echo "[*] A instalar via yay (AUR)..."
                    yay -Sy --noconfirm exiftool
                    ;;
                *)
                    echo "[!] Opção inválida. A usar pacman por defeito..."
                    sudo pacman -Sy --noconfirm exiftool
                    ;;
            esac
        else
            echo "[*] AUR helper não detectado. A usar pacman..."
            sudo pacman -Sy --noconfirm exiftool
        fi
        
    elif command -v zypper >/dev/null 2>&1; then
        echo "[+] Detectado Zypper (OpenSUSE)"
        sudo zypper install -y exiftool
        
    else
        echo "[!] Gestor de pacotes não suportado!"
        echo "Use a opção de instalação manual."
        exit 1
    fi
    
    echo ""
    echo "[✔] ExifTool instalado com sucesso!"
}

# ------------------------------------
# FUNÇÃO: Instalar manualmente a partir do GitHub
# ------------------------------------
install_manual() {
    echo "[*] A instalar dependências essenciais (Perl)..."
    
    # Perl é obrigatório
    if command -v apt >/dev/null 2>&1; then
        sudo apt update
        sudo apt install -y perl wget unzip
        
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y perl wget unzip
        
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --noconfirm perl wget unzip
        
    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install -y perl wget unzip
        
    else
        echo "[!] Não consegui instalar dependências automaticamente."
        exit 1
    fi
    
    echo ""
    echo "[*] A transferir última versão do ExifTool do GitHub..."
    wget https://github.com/exiftool/exiftool/archive/refs/heads/master.zip -O exiftool.zip || { echo "Erro ao transferir!"; exit 1; }
    
    echo "[*] A extrair..."
    unzip -q exiftool.zip || { echo "Erro ao extrair!"; exit 1; }
    
    cd exiftool-master || exit
    
    echo "[*] A instalar binário exiftool..."
    sudo mkdir -p /usr/local/exiftool/
    sudo cp -r ./* /usr/local/exiftool/
    sudo chmod +x /usr/local/exiftool/exiftool
    sudo ln -sf /usr/local/exiftool/exiftool /usr/local/bin/exiftool
    
    cd ..
    rm -rf exiftool-master exiftool.zip
    
    echo ""
    echo "[✔] ExifTool instalado manualmente!"
}

# ------------------------------------
# EXECUTAR OPÇÃO
# ------------------------------------
case $opcao in
    1)
        install_repo
        ;;
    2)
        install_manual
        ;;
    0)
        echo "A sair..."
        exit 0
        ;;
    *)
        echo "Opção inválida."
        exit 1
        ;;
esac