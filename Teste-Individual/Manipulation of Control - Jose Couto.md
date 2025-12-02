# Manipulação de Controlo em PLCs (MITRE ATT&CK – T0831)

## Índice

1. [Introdução](#introducao)
2. [O que é um PLC?](#plc)
3. [Manipulação de Controlo (MITRE ATT&CK – T0831)](#manipulacao)
   - 3.1 Enquadramento MITRE
   - 3.2 Objetivo da técnica
   - 3.3 Como ocorre
   - 3.4 Vetores comuns de ataque
4. [Exemplo didático – Concurso de Bolos](#exemplo)
5. [Esquema do ataque a um PLC](#esquema)
6. [Casos reais de Manipulação de Controlo](#casos)
   - 6.1 Maroochy Shire, Austrália (2000)
   - 6.2 Stuxnet (2010)
   - 6.3 Industroyer / Ucrânia 2015
7. [Consequências potenciais](#consequencias)
8. [Detecção](#detecao)
9. [Mitigação](#mitigacao)
10. [A ligação com Wargaming](#wargaming)
11. [Conclusão](#conclusao)

---

## <a id="introducao"></a>1. Introdução

Wargaming é muitas vezes descrito como um exercício onde uns tentam atacar sistemas informáticos e outros tentam defender‑se. A definição parece correta, mas falha em captar a dimensão estratégica e cognitiva envolvida. A segurança industrial, especialmente quando falamos de PLCs e manipulação de controlo, demonstra que o verdadeiro wargaming exige técnica, antecipação e compreensão profunda do adversário.

Este documento apresenta de forma clara o que é um PLC, como funciona um ataque de manipulação de controlo segundo o MITRE ATT&CK, exemplos reais, impactos, mitigação e a ligação direta com wargaming.

---

## <a id="plc"></a>2. O que é um PLC?

Um **PLC (Controlador Lógico Programável)** é o dispositivo que governa processos industriais. Recebe dados de sensores, executa lógica programada e controla atuadores responsáveis por ações físicas como abrir válvulas, ligar bombas ou ajustar motores.

Presente em setores como água, energia, transportes, fábricas e ambientes críticos, o PLC é o ponto onde o digital encontra o mundo físico. Alterações indevidas na sua lógica podem gerar falhas, danos e interrupção operacional.

---

## <a id="manipulacao"></a>3. Manipulação de Controlo (MITRE ATT&CK – T0831)

### 3.1 Enquadramento MITRE

A técnica **T0831 – Manipulation of Control**, da framework **MITRE ATT&CK for ICS**, descreve situações em que um adversário altera parâmetros, lógica, setpoints ou comandos de controlo, com impacto direto no funcionamento físico do processo.

- **ID:** T0831
- **Tática:** Impact
- **Sub‑técnicas:** Nenhuma

### 3.2 Objetivo da técnica

- Modificar o comportamento de um processo industrial.
- Criar falhas físicas ou ambientais.
- Fazer o sistema operar de forma incorreta sem alertar operadores.
- Ou, em casos mais discretos, degradar lentamente equipamentos.

### 3.3 Como ocorre

- Alteração de lógica ladder ou blocos de função.
- Manipulação de setpoints (temperatura, pressão, nível).
- Injeção de comandos falsos entre PLC e atuadores.
- Modificação de temporizadores ou ramos de decisão.

### 3.4 Vetores comuns de ataque

- Acesso remoto indevido.
- Redes industriais mal segmentadas.
- Credenciais comprometidas.
- Engenharia social.
- Malware especializado para ICS.

---

## <a id="exemplo"></a>4. Exemplo didático – Concurso de Bolos

Para clarificar a manipulação de controlo num contexto social:

Se dois concorrentes de um concurso de bolos dependem de uma receita escrita e alguém altera discretamente a receita do adversário — mudando quantidades, tempos ou passos — o bolo final será um fracasso, mesmo que ele siga a receita "correta".

Este cenário traduz exatamente o impacto de alterar lógica ou setpoints num PLC: pequenas alterações geram grandes consequências e o operador nem sempre sabe que algo foi manipulado.

---

## <a id="esquema"></a>5. Esquema do ataque a um PLC

```
SENSOR (nível / fluxo)
         ↓
       PLC
→ lógica (ladder / blocos)
         ↓
Ataque: Manipulation of Control (T0831)
→ alteração de lógica / parâmetros / ramos / temporizadores
         ↓
ATUADOR (bomba / válvula)
         ↓
PROCESSO (ex: água)
```

---

## <a id="casos"></a>6. Casos reais de Manipulação de Controlo

### 6.1 Maroochy Shire, Austrália (2000)

O primeiro incidente conhecido de manipulação industrial sem malware. Um ex‑funcionário adquiriu acesso aos controladores de saneamento e enviou comandos falsos, libertando mais de 800 000 litros de esgoto em espaços públicos. Demonstrou que ataques ICS não precisam de alta complexidade — apenas acesso e intenção.

### 6.2 Stuxnet (2010)

Malware criado para alterar logicamente PLCs Siemens. Destruiu centrífugas nucleares através de manipulação de velocidade, enquanto apresentava dados falsos aos operadores.

### 6.3 Industroyer / Ucrânia 2015

Atacantes enviaram comandos legítimos mas não autorizados para abrir disjuntores elétricos. O resultado foram apagões que afetaram centenas de milhares de pessoas.

Estes casos provam que o "T0831" é um vetor real, usado por grupos avançados e com impacto mensurável.

---

## <a id="consequencias"></a>7. Consequências potenciais

A manipulação de controlo pode resultar em:

- Danos permanentes em equipamento.
- Interrupção de produção.
- Impacto ambiental grave.
- Perigos à segurança humana.
- Perda financeira e reputacional.
- Encobrimento de atividades maliciosas com dados falsificados.

---

## <a id="detecao"></a>8. Detecção

Segundo o MITRE, **não existe atualmente um método standard para detetar manipulação de controlo**. Na prática, recorre‑se a:

- Monitorização de setpoints e padrões de operação.
- Alertas para alterações de lógica.
- Análise de comportamento anómalo em atuadores.
- Comparação constante entre lógica ativa e gold image.

---

## <a id="mitigacao"></a>9. Mitigação

As medidas mais eficazes incluem:

1. **Autenticidade na comunicação**  
   Uso de MACs, assinaturas digitais, VPN ou TLS industrial.

2. **Validação fora da banda**  
   Segundo canal de verificação para dados críticos.

3. **Backups imutáveis (gold images)**  
   Permitem restaurar lógica legítima rapidamente.

4. **Hardening dos sistemas**  
   Segmentação, controlo de acessos e monitorização de alterações.

5. **Normas e compliance**  
   IEC 62443, NERC CIP e outras reforçam boas práticas.

---

## <a id="wargaming"></a>10. A ligação com Wargaming

Iniciar a apresentação com a definição limitada de wargaming ("ataque e defesa") permite mostrar a sua insuficiência quando analisamos ataques reais a PLCs. No contexto industrial, o wargaming é essencial para testar:

- como o adversário pensa,
- como planeia o ataque,
- e como manipula o terreno — que, neste caso, é a lógica e o processo físico.

No final, wargaming não é apenas confronto. É estratégia.

### Definição final:

**"Wargaming é um desafio tecnológico e mental. Requer compreender o adversário, antecipar os seus passos e preparar o terreno antes do conflito. Não se resume a atacar ou defender — é estratégia aplicada."**

---

## <a id="conclusao"></a>11. Conclusão

A técnica T0831 demonstra que a manipulação de controlo é uma das ameaças mais críticas aos sistemas industriais, porque altera diretamente o comportamento físico do processo. Casos como Maroochy, Stuxnet e Industroyer provam que esta técnica é usada há mais de duas décadas para causar interrupções, danos e impacto operacional.

Mitigar esta ameaça exige autenticidade na comunicação, validação independente, backups imutáveis, hardening e monitorização contínua. Mas acima de tudo exige pensamento estratégico — competências que wargaming ajuda a desenvolver, simulando adversários reais num ambiente controlado.

A segurança industrial não é apenas tecnologia. É antecipação, raciocínio e capacidade de pensar como quem quer manipular o sistema.
