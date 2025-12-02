# T1021.002 SMB / Windows admin shares (ATT&CK)
---
A técnica T1021.002 do MITRE ATT&CK descreve o uso de partilhas de administrador do Windows (como C$, ADMIN$, IPC$) através do protocolo SMB para realizar movimento lateral dentro de uma rede comprometida.

 O atacante utiliza credenciais válidas ou hashes NTLM (Pass-the-Hash) para aceder remotamente a outros sistemas, tendo como objetivo chegar ao domain controller ou obter informações de um utilizador em específico.


## O que é SMB/Admin Shares?

O protocolo SMB (Server Message Block) permite acesso remoto a ficheiros, pastas e serviços.  
O Windows cria, por defeito, partilhas de admin como:
- **C$** → acesso ao disco C:
- **ADMIN$** → acesso ao diretório Windows
- **IPC$** → canal de comunicação para pipes nomeados

Estas partilhas permitem conexões de admin remotas e também permitem que um atacante, com credenciais válidas, tenha acesso remoto total.

### Como funciona o ataque

1. O atacante obtém credenciais (OSINT, engenharia social, password recycling ou leaks). / Ou obtém hashes NTLM após comprometer a primeira máquina.
2. Liga-se às partilhas via SMB.  
3. Faz upload de um payload (ex.: `agent.exe`) para `C$\Windows\Temp` ou `ADMIN$`.  
4. Utiliza serviços remotos (PsExec, SMBExec, WMI) para executar o payload.  
5. Ganha um shell remoto e continua o movimento lateral.

### Porque é que é importante no MITRE?

- Usa funcionalidade legítima do Windows.  
- Muitas organizações deixam SMB aberto internamente.  
- Fácil escalar privilégios quando se obtém acesso a sistemas, principalmente como admin.
- Pouco ruído na rede.

---

# MITRE D3FEND

## D3-FW Network Isolation

- Bloquear tráfego SMB quando as máquinas não precisam.

## D3-AC Account Use Policies

- Admin da máquina A não deve funcionar na máquina B.
- Não usar contas administrativas locais repetidas entre máquinas.
- Remover pastas sensíveis escondidas na rede.

## Medidas de Detecção
- Alertas para logins no SMB.
- Monitorizar criação de ficheiros em pastas sensíveis. 
- Deteção de execução remota via SVCCTL, WinRM ou PsExec.  

---

## Modus Operandi

- **Reconhecimento Passivo**  
- **Lateral Movement (T1021.002)**  

## Etapas do Modus Operandi

### 1. Reconhecimento Passivo
Recolha de informação sem tocar na infraestrutura alvo:
- Pesquisa no LinkedIn, através de engenharia social ou até mesmo encontra leaks online.
- Analisa metadados em ficheiros publicados.
- Pesquisa no Shodan e encontra serviços desatualizados.

### 2. Seleção do Ponto de Entrada
Identificação de um endpoint fraco que pode ser pivoted:
- PC de um funcionário com SMB aberto.
- Conta com password simples ou leaked.
- Por vezes, até guest accounts.

### 3. Lateral Movement
1. Aceder às shares administrativas (C$, ADMIN$).  
2. Fazer upload do payload para uma das pastas.  
3. Execução remota através do PsExec ou SMBExec.  
4. Ganha-se acesso pleno ao sistema.

### 4. Privilege Escalation
Depois da primeira máquina:
- Dump de LSASS para obter credenciais.  
- Enumeração do Active Directory.  
- Escalation para Domain Admin.

### 5. Objetivo Final e Impacto
Dependendo da operação:
- Exfiltração de dados.  
- Encriptação para ransomware.  
- Instalação de backdoors.
- Persistence Techniques.
