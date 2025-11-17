#!/bin/bash
# ------------------------------------
# Install or Compile Sublist3r Script
# ------------------------------------
clear
echo "======================================"
echo "          INSTALAR SUBLIST3R"
echo "======================================"
echo ""
echo "1) Instalar via repositório oficial"
echo "2) Instalar manualmente via GitHub (versão atualizada)"
echo "0) Sair"
echo ""
read -p "Escolha uma opção: " opcao

# ------------------------------------
# FUNÇÃO: Instalar via repositório
# ------------------------------------
install_repo() {
    echo "[*] A detectar gestor de pacotes..."
    
    if command -v apt >/dev/null 2>&1; then
        echo "[+] Detectado APT (Debian/Ubuntu)"
        sudo apt update
        sudo apt install -y sublist3r
        
    elif command -v pacman >/dev/null 2>&1; then
        echo "[+] Detectado Pacman (Arch/Manjaro)"
        
        # Verificar se yay está disponível
        if command -v yay >/dev/null 2>&1; then
            echo "[+] AUR helper (yay) detectado!"
            echo "[!] Sublist3r NÃO existe no repositório oficial do Arch."
            echo ""
            echo "Escolha o método de instalação:"
            echo "1) Instalar via yay (AUR)"
            echo "2) Instalar manualmente via GitHub (opção 2 do menu principal)"
            echo ""
            read -p "Opção [1-2]: " aur_choice
            
            case $aur_choice in
                1)
                    echo "[*] A instalar via yay (AUR)..."
                    yay -Sy --noconfirm sublist3r
                    ;;
                2)
                    echo "[*] A redirecionar para instalação manual..."
                    install_manual
                    return
                    ;;
                *)
                    echo "[!] Opção inválida. A usar yay por defeito..."
                    yay -Sy --noconfirm sublist3r
                    ;;
            esac
        else
            echo "[!] Sublist3r NÃO existe no repositório oficial Arch."
            echo "[!] AUR helper (yay) não detectado."
            echo "Instale o yay ou use a opção 2 para instalar manualmente."
            exit 1
        fi
        
    elif command -v dnf >/dev/null 2>&1; then
        echo "[!] Sublist3r NÃO existe no repositório DNF."
        echo "Use a opção 2."
        exit 1
        
    elif command -v zypper >/dev/null 2>&1; then
        echo "[!] Sublist3r NÃO existe no repositório Zypper."
        echo "Use a opção 2."
        exit 1
        
    else
        echo "[!] Gestor de pacotes não reconhecido!"
        exit 1
    fi
    
    echo ""
    echo "[✔] Sublist3r instalado com sucesso!"
}

# ------------------------------------
# FUNÇÃO: Instalação manual via GitHub
# ------------------------------------
install_manual() {
    echo "[*] A instalar dependências (Python, pip, git)..."
    
    # Dependências
    if command -v apt >/dev/null 2>&1; then
        sudo apt update
        sudo apt install -y python3 python3-pip git
        
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y python3 python3-pip git
        
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --noconfirm python python-pip git
        
    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install -y python3 python3-pip git
        
    else
        echo "[!] Não consegui instalar dependências automaticamente."
        exit 1
    fi
    
    echo ""
    echo "[*] A transferir Sublist3r do GitHub..."
    
    # Definir diretório de instalação
    INSTALL_DIR="/opt/Sublist3r"
    
    # Limpar instalação anterior se existir
    if [ -d "$INSTALL_DIR" ]; then
        echo "[*] A remover instalação anterior..."
        sudo rm -rf "$INSTALL_DIR"
    fi
    
    # Remover link simbólico antigo se existir
    if [ -L "/usr/local/bin/sublist3r" ]; then
        echo "[*] A remover link simbólico anterior..."
        sudo rm -f /usr/local/bin/sublist3r
    fi
    
    # Clonar para diretório temporário
    git clone https://github.com/aboul3la/Sublist3r /tmp/Sublist3r || { echo "Erro no git clone"; exit 1; }
    
    echo "[*] A mover para $INSTALL_DIR..."
    sudo mv /tmp/Sublist3r "$INSTALL_DIR"
    
    cd "$INSTALL_DIR" || exit
    
    echo "[*] A instalar requisitos Python..."
    pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt
    
    echo "[*] A criar link simbólico para /usr/local/bin..."
    sudo chmod +x "$INSTALL_DIR/sublist3r.py"
    sudo ln -sf "$INSTALL_DIR/sublist3r.py" /usr/local/bin/sublist3r
    
    echo ""
    echo "[✔] Sublist3r instalado manualmente com sucesso!"
    echo "[✔] Localização: $INSTALL_DIR"
    echo "[✔] Use: sublist3r -d dominio.com"
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