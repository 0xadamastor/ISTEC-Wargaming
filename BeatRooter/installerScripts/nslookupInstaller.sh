#!/bin/bash
# ------------------------------------
# Install DNS Utils (nslookup & dig) Script
# ------------------------------------
clear
echo "======================================"
echo "   INSTALAR DNS UTILS (nslookup/dig)"
echo "======================================"
echo ""
echo "Este script instala as ferramentas:"
echo "  - nslookup"
echo "  - dig"
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
        echo "[*] A instalar dnsutils (contém nslookup e dig)..."
        sudo apt update
        sudo apt install -y dnsutils
        
    elif command -v dnf >/dev/null 2>&1; then
        echo "[+] Detectado DNF (Fedora/RHEL)"
        echo "[*] A instalar bind-utils (contém nslookup e dig)..."
        sudo dnf install -y bind-utils
        
    elif command -v pacman >/dev/null 2>&1; then
        echo "[+] Detectado Pacman (Arch/Manjaro)"
        
        # Verificar se yay está disponível
        if command -v yay >/dev/null 2>&1; then
            echo "[+] AUR helper (yay) detectado!"
            echo "[*] A instalar bind (contém nslookup e dig)..."
            echo ""
            echo "Escolha o método de instalação:"
            echo "1) pacman (repositório oficial)"
            echo "2) yay (AUR - pode ter versão mais recente)"
            echo ""
            read -p "Opção [1-2]: " aur_choice
            
            case $aur_choice in
                1)
                    echo "[*] A instalar via pacman..."
                    sudo pacman -Sy --noconfirm bind
                    ;;
                2)
                    echo "[*] A instalar via yay (AUR)..."
                    yay -Sy --noconfirm bind
                    ;;
                *)
                    echo "[!] Opção inválida. A usar pacman por defeito..."
                    sudo pacman -Sy --noconfirm bind
                    ;;
            esac
        else
            echo "[*] AUR helper não detectado. A usar pacman..."
            echo "[*] A instalar bind (contém nslookup e dig)..."
            sudo pacman -Sy --noconfirm bind
        fi
        
    elif command -v zypper >/dev/null 2>&1; then
        echo "[+] Detectado Zypper (OpenSUSE)"
        echo "[*] A instalar bind-utils (contém nslookup e dig)..."
        sudo zypper install -y bind-utils
        
    else
        echo "[!] Gestor de pacotes não suportado!"
        exit 1
    fi
    
    echo ""
    echo "[✔] DNS Utils instalados com sucesso!"
    echo ""
    echo "[✔] Ferramentas disponíveis:"
    echo "    - nslookup dominio.com"
    echo "    - dig dominio.com"
    echo "    - dig @8.8.8.8 dominio.com"
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
