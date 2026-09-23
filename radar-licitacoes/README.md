# Radar Licitações MVP

MVP para captar, filtrar e pontuar oportunidades de contratação pública.

## O que já faz

- FastAPI em Docker
- PostgreSQL isolado
- ingestão de feed ATOM/XML configurável
- deduplicação por ID externo
- score inicial por palavras-chave
- endpoint de ingestão
- endpoint para listar oportunidades

A Plataforma de Contratación del Sector Público publica conjuntos de dados abertos em XML/ATOM destinados a reutilização automática. O URL concreto do feed fica em `PLACSP_ATOM_URL` para podermos trocar a origem sem alterar código.

## Deploy

```bash
cp .env.example .env
# editar PLACSP_ATOM_URL e palavras-chave
docker compose up -d --build
```

API:
- `GET /health`
- `POST /ingest`
- `GET /opportunities?min_score=20&limit=50`

Porta padrão: `8088`.

## Próximas etapas

1. fixar os feeds oficiais da PLACSP/OpenPLACSP;
2. extrair CPV, orçamento, localidade, prazo e órgão;
3. perfis de empresas/ICP;
4. score semântico com LLM;
5. relatório diário por email só para usuários com opt-in;
6. landing + Stripe;
7. monitoramento e métricas.
