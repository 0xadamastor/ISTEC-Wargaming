#!/bin/bash
# -------------------------------
# Install or compile Nmap Script
# -------------------------------
clear
echo "======================================"
echo "          INSTALAR NMAP"
echo "======================================"
echo ""
echo "1) Instalar via repositório oficial"
echo "2) Compilar manualmente via GitHub"
echo "0) Sair"
echo ""
read -p "Escolha uma opção: " opcao

# -------------------------------
# FUNÇÃO: Instala pelo repositório
# -------------------------------
install_repo() {
    echo "[*] A detectar gestor de pacotes..."
    
    if command -v apt >/dev/null 2>&1; then
        echo "[+] Detectado APT (Debian/Ubuntu)"
        sudo apt update
        sudo apt install -y nmap
        
    elif command -v dnf >/dev/null 2>&1; then
        echo "[+] Detectado DNF (Fedora/RHEL)"
        sudo dnf install -y nmap
        
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
                    sudo pacman -Sy --noconfirm nmap
                    ;;
                2)
                    echo "[*] A instalar via yay (AUR)..."
                    yay -Sy --noconfirm nmap
                    ;;
                *)
                    echo "[!] Opção inválida. A usar pacman por defeito..."
                    sudo pacman -Sy --noconfirm nmap
                    ;;
            esac
        else
            echo "[*] AUR helper não detectado. A usar pacman..."
            sudo pacman -Sy --noconfirm nmap
        fi
        
    elif command -v zypper >/dev/null 2>&1; then
        echo "[+] Detectado Zypper (OpenSUSE)"
        sudo zypper install -y nmap
        
    else
        echo "[!] Gestor de pacotes não suportado!"
        echo "Instale manualmente ou escolha a opção de compilação."
        exit 1
    fi
    
    echo ""
    echo "[✔] Instalação concluída!"
}

# -------------------------------
# FUNÇÃO: Compilar manualmente
# -------------------------------
compile_manual() {
    echo "[*] A instalar dependências da compilação..."
    
    # Instalar dependências mais comuns
    if command -v apt >/dev/null 2>&1; then
        sudo apt update
        sudo apt install -y git build-essential liblua5.3-dev libssl-dev
        
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y git gcc gcc-c++ make openssl-devel lua-devel
        
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --noconfirm git base-devel openssl lua
        
    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install -y git gcc gcc-c++ make libopenssl-devel lua-devel
        
    else
        echo "[!] Não foi possível instalar dependências automaticamente."
        echo "Instale-as manualmente e tente outra vez."
        exit 1
    fi
    
    echo ""
    echo "[*] A transferir código do Nmap do GitHub..."
    
    # Limpar diretório anterior se existir
    if [ -d "nmap" ]; then
        echo "[*] A remover instalação anterior..."
        rm -rf nmap
    fi
    
    git clone https://github.com/nmap/nmap || { echo "Erro no git clone"; exit 1; }
    cd nmap || exit
    
    echo "[*] A preparar build..."
    ./configure || { echo "Erro no configure"; exit 1; }
    
    echo "[*] A compilar (pode demorar)..."
    make || { echo "Erro na compilação"; exit 1; }
    
    echo "[*] A instalar..."
    sudo make install || { echo "Erro na instalação"; exit 1; }
    
    # Limpar diretório de compilação
    cd ..
    echo "[*] A limpar ficheiros temporários..."
    rm -rf nmap
    
    echo ""
    echo "[✔] Nmap compilado e instalado com sucesso!"
}

# -------------------------------
# EXECUTAR OPÇÃO
# -------------------------------
case $opcao in
    1)
        install_repo
        ;;
    2)
        compile_manual
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