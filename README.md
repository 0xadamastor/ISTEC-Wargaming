# ISTEC-Wargaming

```
    _          _   _  __  __                  
   / \   _ __ | |_(_) \ \/ /___ _ __ _____  __
  / _ \ | '_ \| __| |  \  // _ \ '__/ _ \ \/ /
 / ___ \| | | | |_| |  /  \  __/ | | (_) >  < 
/_/   \_\_| |_|\__|_| /_/\_\___|_|  \___/_/\_\

```

> Uma **playground** para exercícios de defesa (Blue Team), ataque (Red Team) e colaboração (Purple Team).
> Usamos este repositório para treinar deteções, simular incidentes, construir playbooks e melhorar a resiliência da tua infra.

---

## 🎯 Objetivo

Criar um **laboratório reproducível** com artefactos, scripts, deteções, playbooks e exercícios para testar e validar capacidades de segurança ofensiva e defensiva — e, principalmente, para fomentar a colaboração entre equipas (Purple Team).

---

## 🔥 O que tem neste repositório

* `blueteam/` — o lado da força.
* `redteam/` — o lado negro da força.

---

## 📚 Indice (Table of Contents)

1. [Como usar](#%EF%B8%8F-como-usar)
2. [Ferramentas e regras](#%EF%B8%8F-ferramentas-e-regras)
3. [Checklist Purple Team](#-checklist-purple-team)
4. [Ideias para Projeto](#-ideias-para-projeto)
5. [Contribuir](#-contribuir)
6. [Licença](#-licen%C3%A7a)

---

# ⚙️ Como usar

### 1) Clonar

```bash
git clone https://github.com/definitelynotrafa/ISTEC-Wargaming.git
cd ISTEC-Wargaming
```

### 2) Preparar laboratório

```bash
cd antixerox/docker
# Exemplo: levantar um AD + host Windows + SIEM
docker-compose up -d
```
---

# 🛠️ Ferramentas e regras

* **Red Team:**
* **Blue Team:**
* **Purple Team:**

---

# ✅ Checklist Purple Team

* [x] Fazer alguma coisa!
* [ ] Defenir um nome para o projeto do diário
* [ ] Escolher a plataforma, ferramenta e linguagem do diário
---

# 💡 Ideias para Projeto

### 1. **Diário Hacker** — `diariohacker/`

**Descrição curta**  
Um diário/registro técnico para pentesters: cada entrada documenta data, objetivo, TTPs usados, telemetria recolhida e vulnerabilidades identificadas — como um mapa mental de um hacker.

**Nomes (ideias)**  
- BeatRooter

**Plataforma (defenido)**  
- Multiplataforma (markdown + CLI) — funciona em qualquer SO.  

**Ferramenta(s)**  
- Base: ficheiros Markdown versionados (`diariohacker/diario.md`).  

**Linguagem (ideias & trade-offs)**  
- **Python** — Mais simples e rápido para desenvolver; excelente para scripts CLI, parsing e geração de relatórios. (Prós: rapidez de prototipagem; Contras: desempenho puro). 
- **C++** — Muito rápido e baixo nível, mas geralmente demasiado pesado para um início de projeto; só se precisarmos de processamento intensivo.  
- **JavaScript/Node** — Útil se formos também fazer uma UI web ou SPA integrada.

---

# 🤝 Contribuir

Contribuições são bem-vindas! Para contribuir:

1. Fork → branch feature/bugfix → pull request.
2. Inclui: objetivo, risco/impacto, instruções de teste, telemetria esperada.
3. Evita ser estúpido.

---

# 📜 Licença

Não roubes nada. Se não a tua mãe vai ter uma surpresa logo à noite!
