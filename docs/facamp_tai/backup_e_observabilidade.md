# Backup e observabilidade do TechStore

## Escopo e responsabilidade

O banco do MVP está no Neon e a aplicação está no Render. O projeto não grava
backups nem credenciais no repositório. A política de retenção e os recursos de
backup/recuperação devem ser confirmados no painel do provedor antes da
apresentação, pois podem variar conforme o plano contratado.

## Rotina de conferência antes da demonstração

1. No Neon, confirme o projeto, a branch usada pelo MVP e a área de backup ou
   recuperação disponível no plano. Faça uma captura sem exibir a URL de
   conexão.
2. No computador do grupo, execute `flask --app app check-db`. O comando é
   somente leitura e confirma a conexão e as cinco contagens principais.
3. No Render, confirme que o último deploy está `Live` e que a rota `/` retorna
   HTTP 200. Os logs não devem conter segredos.
4. Mantenha `01_schema.sql`, `02_seed.sql`, `03_validacao.sql` e
   `04_testes_constraints.sql` versionados: eles permitem reconstruir e validar
   a estrutura didática em outro banco PostgreSQL.

## Teste de recuperação seguro

Uma restauração nunca deve ser ensaiada sobre a branch `production`. Para
comprovar recuperação, crie uma branch ou banco temporário no provedor,
reconstrua-o com os scripts SQL versionados, rode `03_validacao.sql` e então
elimine somente esse ambiente temporário.

## Limitações assumidas pelo MVP

- Não há automação própria de backup, migrations ou monitoramento contínuo.
- O plano gratuito do Render pode suspender a instância após inatividade.
- O checkout deve usar dados fictícios, pois o projeto é acadêmico e não possui
  autenticação completa, política de privacidade ou pagamentos reais.
