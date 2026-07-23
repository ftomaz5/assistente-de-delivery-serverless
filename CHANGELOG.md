# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.
O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Corrigido
- **Bug crítico:** o arquivo `statemachine/delivery-assistant.asl.json` continha
  conteúdo de rascunho antes da definição, tornando o JSON inválido e impedindo
  `sam build`/`sam deploy`. Restaurado para conter apenas a máquina de estados válida.

### Adicionado
- Testes unitários (pytest) com **100% de cobertura** das duas Lambdas.
- Teste de sanidade da máquina de estados (guarda contra regressão do JSON).
- CI: ruff + pytest com cobertura + `cfn-lint`.
- `requirements-dev.txt`, `ruff.toml`, `pytest.ini`.
- Documentação de variáveis de ambiente e fluxo de testes locais no README.
- Guia de contribuição, template de PR, validação de título (Conventional Commits) e Dependabot.

## [0.1.0]

### Adicionado
- Pipeline serverless com Step Functions, Lambdas (validar/notificar), Bedrock e SNS.
- Template AWS SAM e evento de exemplo.
