# Contribuindo

Obrigado por dedicar tempo a este projeto! Este repositório segue algumas
convenções simples para manter o histórico limpo e o CI verde.

## Padrão de commits — Conventional Commits

As mensagens de commit (e os títulos de Pull Request) seguem
[Conventional Commits](https://www.conventionalcommits.org/pt-br/):

```
<tipo>(<escopo opcional>): <descrição no imperativo>
```

Tipos usados neste projeto:

| Tipo | Quando usar |
|------|-------------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Apenas documentação |
| `test` | Adição ou ajuste de testes |
| `refactor` | Mudança de código que não altera comportamento |
| `perf` | Melhoria de desempenho |
| `build` | Build, dependências ou empacotamento |
| `ci` | Pipelines e automação |
| `chore` | Tarefas de manutenção |

Exemplos:

```
feat(api): adiciona endpoint de orçamento com múltiplos produtos
fix(frete): corrige cálculo grátis exatamente em R$300
docs: documenta variáveis de ambiente no README
```

Uma mudança que quebra compatibilidade leva `!` após o tipo/escopo
(`feat!:` ou `feat(api)!:`) e uma seção `BREAKING CHANGE:` no corpo.

## Fluxo de trabalho

1. Crie um branch a partir de `main`: `git switch -c feat/minha-mudanca`.
2. Faça commits pequenos e descritivos seguindo o padrão acima.
3. Garanta que **lint e testes passam localmente** antes de abrir o PR.
4. Abra o Pull Request — o CI roda automaticamente e o título do PR é validado.

## Versionamento e releases

O projeto usa **SemVer** (`vMAJOR.MINOR.PATCH`). Publicar uma tag `vX.Y.Z`
dispara o workflow de release, que cria a GitHub Release automaticamente.

```bash
git tag v1.1.0
git push origin v1.1.0
```
