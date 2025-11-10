# Backend FastAPI do AppQuanta

Uma API backend moderna e eficiente para a aplicação AppQuanta, construída com FastAPI e integrada com Autenticação Firebase e Firestore.

## Funcionalidades

- **Autenticação de Usuário**: Registrar e fazer login de usuários com Firebase Auth
- **Gerenciamento de Tokens JWT**: Proteger endpoints da API com autenticação JWT
- **Gerenciamento de Apps**: Operações CRUD para aplicações de usuários armazenadas no Firestore
- **Documentação Automática**: Interface Swagger UI disponível em `/docs`
- **Suporte a CORS**: Configurado para integração com app Flutter
- **Tratamento de Erros**: Respostas de erro padronizadas
- **Implantação 24/7**: Pronto para implantação no Render

## Pilha Tecnológica

- **Framework**: FastAPI
- **Autenticação**: Firebase Auth + JWT
- **Banco de Dados**: Firebase Firestore
- **Implantação**: Render
- **Linguagem**: Python 3.11+

## Estrutura do Projeto

```
appQuanta-server/
├── main.py                 # Ponto de entrada da aplicação FastAPI
├── models/
│   ├── user.py            # Modelos Pydantic relacionados ao usuário
│   └── app.py             # Modelos Pydantic relacionados ao app
├── routes/
│   ├── auth.py            # Endpoints de autenticação
│   └── apps.py            # Endpoints de gerenciamento de apps
├── services/
│   └── firebase_service.py # Integração com Firebase
├── requirements.txt        # Dependências Python
├── Procfile               # Configuração de implantação no Render
├── .env.example           # Modelo de variáveis de ambiente
└── README.md              # Este arquivo
```

## Endpoints da API

### Autenticação
- `POST /api/v1/auth/register` - Registrar novo usuário
- `POST /api/v1/auth/login` - Fazer login do usuário e obter token JWT

### Gerenciamento de Apps (Protegido)
- `GET /api/v1/apps` - Obter apps do usuário
- `POST /api/v1/apps/create` - Criar novo app
- `PUT /api/v1/apps/{app_id}` - Atualizar app
- `DELETE /api/v1/apps/{app_id}` - Deletar app

## Formato de Resposta

Todas as respostas da API seguem este formato padronizado:

```json
{
  "success": true,
  "message": "Operação concluída com sucesso.",
  "data": { ... }
}
```

## Configuração e Instalação

1. **Clone o repositório**
   ```bash
   git clone <repository-url>
   cd appQuanta-server
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   - Copie `.env.example` para `.env`
   - Preencha suas credenciais do projeto Firebase
   - Gere um segredo JWT seguro
   - [Arquivo de Chaves](https://docs.google.com/document/d/1DYIuvFTs5DRbp6LwzNFXGFMxxTC7comACQTXzwO7NfA/edit?usp=sharing)

5. **Execute o servidor**
   ```bash
   python main.py
   ```

   O servidor iniciará em `http://localhost:8000`

## Configuração do Firebase

1. Crie um projeto Firebase em https://console.firebase.google.com/
2. Habilite Autenticação e Firestore
3. Gere uma chave de conta de serviço (arquivo JSON)
4. Defina as seguintes variáveis de ambiente:
   - `FIREBASE_PROJECT_ID`
   - `FIREBASE_PRIVATE_KEY` (formate com \n para quebras de linha)
   - `FIREBASE_CLIENT_EMAIL`
   - `JWT_SECRET`

## Integração com Flutter

### Autenticação
```dart
// Registrar
final response = await http.post(
  Uri.parse('https://your-render-app.com/api/v1/auth/register'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'email': 'user@example.com',
    'password': 'password123',
    'display_name': 'Nome do Usuário'
  }),
);

// Login
final response = await http.post(
  Uri.parse('https://your-render-app.com/api/v1/auth/login'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'email': 'user@example.com',
    'password': 'password123'
  }),
);

// Extrair token da resposta
final token = jsonDecode(response.body)['data']['access_token'];
```

### Gerenciamento de Apps
```dart
// Obter apps
final response = await http.get(
  Uri.parse('https://your-render-app.com/api/v1/apps'),
  headers: {
    'Authorization': 'Bearer $token',
    'Content-Type': 'application/json'
  },
);

// Criar app
final response = await http.post(
  Uri.parse('https://your-render-app.com/api/v1/apps/create'),
  headers: {
    'Authorization': 'Bearer $token',
    'Content-Type': 'application/json'
  },
  body: jsonEncode({
    'name': 'Meu App',
    'description': 'Descrição do app',
    'status': 'active'
  }),
);
```

## Implantação no Render

1. **Conecte seu repositório GitHub ao Render**
2. **Crie um novo Web Service**
3. **Configure as definições de build**:
   - **Comando de Build**: `pip install -r requirements.txt`
   - **Comando de Início**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Defina as variáveis de ambiente** no painel do Render:
   - `FIREBASE_PROJECT_ID`
   - `FIREBASE_PRIVATE_KEY`
   - `FIREBASE_CLIENT_EMAIL`
   - `JWT_SECRET`
   - `PORT` (definido automaticamente pelo Render)

## Desenvolvimento

- **Documentação da API**: Visite `http://localhost:8000/docs` para a interface Swagger UI
- **Testes**: Use Postman ou ferramentas similares para testar endpoints
- **Linting**: Execute `flake8` para verificações de qualidade de código

## Contribuição

1. Faça um fork do repositório
2. Crie uma branch de funcionalidade
3. Faça suas alterações
4. Teste exaustivamente
5. Envie um pull request

## Licença

Este projeto está licenciado sob a Licença MIT.
