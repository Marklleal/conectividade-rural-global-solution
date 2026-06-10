# Mission Control AI — ConnectSat

Sistema de monitoramento operacional para a trilha **ConnectSat** da Global Solution 2026.1, focado em conectividade rural via satélite LEO. O projeto simula telemetria de uma missão de telecomunicações, aplica regras de decisão em Python para gerar alertas e usa IA generativa via Ollama Cloud para transformar dados técnicos em diagnósticos operacionais claros e conectados ao impacto social da conectividade rural.

---

## Vídeo de demonstração

[![Assistir demonstração no YouTube](https://img.youtube.com/vi/SEU_VIDEO_AQUI/0.jpg)](https://www.youtube.com/watch?v=SEU_VIDEO_AQUI)

---

## Sobre o projeto

O **Mission Control AI — ConnectSat** foi desenvolvido para monitorar uma missão simulada de conectividade rural baseada em satélites de telecomunicações em órbita baixa, no estilo de constelações LEO como Starlink, OneWeb e futuras redes nacionais. 

A solução recebe dados simulados de telemetria, detecta anomalias com lógica determinística em Python e consulta um modelo de linguagem via Ollama Cloud para explicar o estado da missão em linguagem natural, sem delegar toda a decisão operacional ao modelo. 

O diferencial do projeto está em traduzir problemas técnicos orbitais para **impactos concretos na Terra**, mostrando como falhas de enlace podem afetar escolas rurais, telemedicina e pequenos negócios sem acesso a fibra óptica. 

---

## Contexto do problema

A proposta da Global Solution 2026.1 privilegia soluções que conectem tecnologia espacial a problemas reais da sociedade, e não apenas sistemas “legais” de monitoramento orbital sem impacto claro. 

Na trilha ConnectSat, o problema central é a dependência crescente de conectividade satelital para inclusão digital em regiões remotas, onde escolas, postos de saúde e atividades econômicas locais dependem de enlaces estáveis para operar. 

Quando o satélite opera bem, há continuidade de serviço, acesso à informação e suporte a telemedicina. Quando falha, quem sofre não é apenas o operador técnico, mas comunidades inteiras que perdem acesso a comunicação essencial. 

---

## Objetivo da solução

Nosso objetivo foi construir um sistema capaz de:

- Simular a operação de um satélite de telecomunicações em LEO. 
- Monitorar parâmetros críticos de conectividade. 
- Aplicar regras em Python para classificar eventos como normal, atenção ou crítico. 
- Disparar respostas automatizadas em cenários críticos. 
- Utilizar IA generativa para contextualizar a situação em linguagem natural. 
- Traduzir cada anomalia técnica para seu impacto social na conectividade rural. 

---

## Trilha escolhida: ConnectSat

**Satélite simulado:** satélite de telecomunicações em LEO, inspirado em constelações modernas de conectividade. 

**Parâmetros monitorados:**
- Latência de uplink. 
- Throughput do feixe. 
- Saúde da antena phased-array. 
- Beam steering. 
- Carga térmica do transponder. 

**Personas atendidas:**
- NOC engineer da operadora. 
- Coordenador de programa de inclusão digital. 
- Cliente final em comunidade rural. 

**Setor de impacto:**
- Comunicação e inclusão digital para escolas rurais, telemedicina e pequenos negócios sem fibra. 

---

## Arquitetura do projeto

A solução foi organizada conforme a estrutura oficial proposta no desafio, mantendo separação clara entre entrada, interface, telemetria, regras e IA. 

```text
mission-control-ai/
│
├── README.md
├── main.py
├── banner_ascii.py
├── requirements.txt
├── .env.example
├── src/
│   ├── __init__.py
│   ├── ui.py
│   ├── engine.py
│   ├── telemetria.py
│   └── alertas.py
├── prompts/
│   └── system_prompt.md
├── data/
│   └── cenarios.json
└── assets/
    ├── screenshot_banner.png
    └── screenshot_analise.png
```

### Papel de cada arquivo

- `main.py`: ponto de entrada do sistema. 
- `src/ui.py`: interface CLI estilo Claude Code com banner, comandos e painéis. 
- `src/engine.py`: orquestra telemetria, alertas e integração com LLM. 
- `src/telemetria.py`: gera ou lê os dados simulados da missão. 
- `src/alertas.py`: aplica thresholds e lógica de decisão em Python. 
- `prompts/system_prompt.md`: define a persona e as restrições do modelo. 
- `banner_ascii.py`: script auxiliar para customização do banner do terminal. 

---

## Tecnologias utilizadas

Conforme a stack recomendada no enunciado, o projeto foi construído em Python com integração ao Ollama Cloud e interface terminal em estilo moderno. 

- **Python 3.10+**. 
- **Ollama Cloud** com modelo `gpt-oss:120b`. 
- **ollama** para integração com o modelo. 
- **python-dotenv** para carregamento seguro da API key. 
- **Rich** para painéis e renderização visual no terminal. 
- **prompt-toolkit** para input interativo na CLI. 
- **PyFiglet** para o banner ASCII. 

---

## Como a missão funciona

O fluxo principal do sistema segue quatro etapas:

1. **Coleta de telemetria**  
   O módulo `src/telemetria.py` gera snapshots da missão com os parâmetros monitorados da trilha ConnectSat.

2. **Avaliação de alertas**  
   O módulo `src/alertas.py` aplica regras determinísticas em Python para identificar estados de atenção e criticidade, além de disparar pelo menos uma ação automática em cenários críticos, como exige o enunciado. 

3. **Análise contextual por IA**  
   O `src/engine.py` injeta os dados reais da missão e os alertas ativos no prompt enviado ao Ollama Cloud, evitando “IA decorativa” com prompt estático. 

4. **Apresentação na CLI**  
   A `src/ui.py` exibe um snapshot legível do status atual e a interpretação da IA em um painel limpo, mantendo o foco na camada de domínio. 

---

## Lógica de decisão da missão

A classificação operacional não depende apenas da IA. O enunciado exige explicitamente que a lógica de tomada de decisão esteja em Python, e não só no prompt. 

Na nossa implementação:

- Latência elevada pode gerar alerta de atenção.
- Throughput reduzido pode indicar degradação de capacidade.
- Beam steering desalinhado pode comprometer cobertura.
- Queda na saúde da antena phased-array pode sinalizar falha parcial do subsistema de comunicação.
- Sobrecarga térmica do transponder pode gerar estado crítico com resposta automatizada.

A IA não substitui essa decisão. Ela recebe os dados já avaliados pelo código e explica causa provável, severidade, ação sugerida e impacto terrestre. 

---

## Proposta de valor e modelo de negócio

A Global Solution 2026.1 pede que o grupo articule claramente quem se beneficia na Terra e quem paga pela solução. 

### 1. Qual problema real terrestre esta missão resolve?

O projeto responde ao problema da instabilidade e baixa visibilidade operacional em enlaces de conectividade rural via satélite. Em regiões sem fibra, uma falha de comunicação pode interromper aulas remotas, consultas médicas e atividades econômicas locais.

### 2. Quem paga pela solução?

O modelo mais plausível é **híbrido**:
- setor público, em programas de inclusão digital, educação conectada e saúde remota;
- setor privado, por operadoras, integradoras e provedores de telecomunicação satelital.

### 3. Qual métrica de impacto concreto?

Uma operação estável por 1 ano pode ser associada, por exemplo, a:
- dezenas ou centenas de escolas rurais com conectividade contínua;
- postos de saúde remotos com teleatendimento confiável;
- pequenos negócios locais mantendo operação digital básica sem dependência de infraestrutura terrestre cara.

### 4. Qual modelo de negócio?

O modelo pode ser descrito como:
- **monitoramento operacional como serviço** para operadoras;
- **plataforma de observabilidade + IA explicativa** para conectividade rural;
- contratos B2B/B2G com operadoras, governo e programas públicos de inclusão digital.

---

## Persona operacional

A persona principal do sistema é o **NOC engineer** de uma operadora de conectividade rural via satélite. 

A resposta do sistema também é útil para duas personas secundárias:
- coordenador de programa de inclusão digital;
- cliente final em comunidade rural. 

Essa escolha orienta o tom do system prompt e garante que a análise não fique genérica. 

---

## Comandos da CLI

A interface foi mantida próxima ao estilo Claude Code, com comandos básicos e foco em leitura rápida. 

- `/help` — mostra os comandos disponíveis.
- `/status` — exibe o snapshot atual da missão.
- `/about` — explica o contexto da trilha ConnectSat.
- `/clear` — limpa a tela e redesenha o banner.
- `/exit` — encerra a aplicação.

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/mission-control-ai.git
cd mission-control-ai
```

### 2. Crie um ambiente virtual

**Windows**
```bash
python -m venv .venv
.venv\\Scripts\\activate
```

**Linux/macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com:

```env
OLLAMA_API_KEY=sua_chave_aqui
```

> Importante: a chave não deve ser versionada no GitHub. O enunciado prevê penalidade automática caso a API key apareça no histórico do repositório. 

---

## Execução

Com o ambiente configurado, execute:

```bash
python main.py
```

Ao iniciar, o sistema deve abrir a CLI com banner ASCII, comandos básicos e integração com o motor da missão. 

---

## Prints reais do sistema

> O desafio exige pelo menos **2 prints reais** do sistema funcionando dentro da pasta `assets/` e referenciados no README. 

### Banner inicial

![Banner inicial da CLI](assets/screenshot_banner.png)

### Análise da missão com IA

![Análise da missão com IA](assets/screenshot_analise.png)

> Substitua os nomes dos arquivos se vocês usarem outros nomes em `assets/`.

---

## Exemplo de uso

Perguntas que podem ser feitas na CLI:

- `Como está a missão agora?`
- `Explique o risco atual para conectividade rural.`
- `Analise o cenário crise_total.`
- `Qual o impacto da sobrecarga térmica no serviço?`

A cada execução, a telemetria atual é combinada com alertas reais do ciclo e enviada ao modelo para gerar uma análise contextualizada. 

---

## Cenários de teste

Durante o desenvolvimento, os principais cenários testados foram:

- **Normal** — operação estável, sem alertas relevantes.
- **Atenção** — latência degradada ou throughput baixo.
- **Crítico** — beam steering desalinhado, falha parcial de antena ou sobrecarga térmica.
- **Extremo** — combinação de múltiplas falhas simultâneas.

O objetivo dos testes foi validar:
- coerência dos thresholds em Python;
- estabilidade da resposta do LLM;
- clareza do status exibido na CLI;
- conexão explícita entre diagnóstico técnico e impacto terrestre. 

---

## Limitações conhecidas

O próprio enunciado recomenda documentar limitações conhecidas no README como sinal de honestidade técnica. 

Atualmente, as principais limitações deste projeto são:

- A telemetria é **simulada**, não proveniente de uma operadora ou satélite real.
- Os thresholds de alerta foram calibrados para fins didáticos e demonstrativos.
- A resposta do LLM pode variar entre execuções, mesmo com temperatura baixa, porque modelos generativos não são totalmente determinísticos. 
- O sistema não representa dinâmica orbital real nem modelagem física de enlace.
- A CLI foi mantida propositalmente simples, porque a prioridade do projeto está na camada de domínio, não no polimento visual excessivo. 
- A contextualização de impacto terrestre é qualitativa e ilustrativa, não baseada em dados operacionais reais de cobertura.

---

## Licença / uso acadêmico

Projeto desenvolvido para fins acadêmicos na disciplina **Prompt Engineering and Artificial Intelligence**, dentro da **Global Solution 2026.1** da FIAP. 
