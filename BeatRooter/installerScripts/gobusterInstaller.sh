#!/bin/bash
# ------------------------------------
# Install or Compile GoBuster Script
# ------------------------------------
clear
echo "======================================"
echo "          INSTALAR GOBUSTER"
echo "======================================"
echo ""
echo "1) Instalar via repositório oficial"
echo "2) Compilar manualmente via GitHub"
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
        sudo apt install -y gobuster
        
    elif command -v dnf >/dev/null 2>&1; then
        echo "[!] O GoBuster NÃO está nos repos oficiais Fedora/DNF."
        echo "Use a opção 2 para compilar manualmente."
        exit 1
        
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
                    sudo pacman -Sy --noconfirm gobuster
                    ;;
                2)
                    echo "[*] A instalar via yay (AUR)..."
                    yay -Sy --noconfirm gobuster
                    ;;
                *)
                    echo "[!] Opção inválida. A usar pacman por defeito..."
                    sudo pacman -Sy --noconfirm gobuster
                    ;;
            esac
        else
            echo "[*] AUR helper não detectado. A usar pacman..."
            sudo pacman -Sy --noconfirm gobuster
        fi
        
    elif command -v zypper >/dev/null 2>&1; then
        echo "[!] O GoBuster NÃO está nos repos oficiais OpenSUSE."
        echo "Use a opção 2 para compilar manualmente."
        exit 1
        
    else
        echo "[!] Gestor de pacotes não suportado!"
        echo "Instale manualmente ou escolha compilação."
        exit 1
    fi
    
    echo ""
    echo "[✔] GoBuster instalado com sucesso!"
}

# ------------------------------------
# FUNÇÃO: Compilar manualmente
# ------------------------------------
compile_manual() {
    echo "[*] A instalar dependências e Go..."
    
    # Instalar Go dependendo do gestor de pacotes
    if command -v apt >/dev/null 2>&1; then
        sudo apt update
        sudo apt install -y git golang
        
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y git golang
        
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --noconfirm git go
        
    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install -y git go
        
    else
        echo "[!] Não consegui instalar Go automaticamente."
        exit 1
    fi
    
    echo ""
    echo "[*] A transferir código do GoBuster do GitHub..."
    
    # Limpar diretório anterior se existir
    if [ -d "gobuster" ]; then
        echo "[*] A remover instalação anterior..."
        rm -rf gobuster
    fi
    
    git clone https://github.com/OJ/gobuster || { echo "Erro no git clone"; exit 1; }
    cd gobuster || exit
    
    echo "[*] A compilar GoBuster..."
    go build || { echo "Erro no go build"; exit 1; }
    
    echo "[*] A mover binário para /usr/local/bin..."
    sudo mv gobuster /usr/local/bin/gobuster
    sudo chmod +x /usr/local/bin/gobuster
    
    # Limpar diretório de compilação
    cd ..
    rm -rf gobuster
    
    echo ""
    echo "[✔] GoBuster compilado e instalado com sucesso!"
}

# ------------------------------------
# EXECUTAR OPÇÃO
# ------------------------------------
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