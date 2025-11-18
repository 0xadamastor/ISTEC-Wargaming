#!/bin/bash
# ------------------------------------
# Install Whois Script
# ------------------------------------
clear
echo "======================================"
echo "          INSTALAR WHOIS"
echo "======================================"
echo ""
echo "1) Instalar via repositório oficial"
echo "0) Sair"
echo ""
read -p "Escolha uma opção: " opcao

# ------------------------------------
# FUNÇÃO: Instalar pelo repositório
# ------------------------------------
install_repo() {
    echo "[*] A detectar gestor de pacotes..."
    
    if command -v apt >/dev/null 2>&1; then
        echo "[+] Detectado APT (Debian/Ubuntu)"
        sudo apt update
        sudo apt install -y whois
        
    elif command -v dnf >/dev/null 2>&1; then
        echo "[+] Detectado DNF (Fedora/RHEL)"
        sudo dnf install -y whois
        
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
                    sudo pacman -Sy --noconfirm whois
                    ;;
                2)
                    echo "[*] A instalar via yay (AUR)..."
                    yay -Sy --noconfirm whois
                    ;;
                *)
                    echo "[!] Opção inválida. A usar pacman por defeito..."
                    sudo pacman -Sy --noconfirm whois
                    ;;
            esac
        else
            echo "[*] AUR helper não detectado. A usar pacman..."
            sudo pacman -Sy --noconfirm whois
        fi
        
    elif command -v zypper >/dev/null 2>&1; then
        echo "[+] Detectado Zypper (OpenSUSE)"
        sudo zypper install -y whois
        
    else
        echo "[!] Gestor de pacotes não suportado!"
        exit 1
    fi
    
    echo ""
    echo "[✔] Whois instalado com sucesso!"
    echo "[✔] Use: whois dominio.com"
}

# ------------------------------------
# EXECUTAR OPÇÃO
# ------------------------------------
case $opcao in
    1)
        install_repo
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
