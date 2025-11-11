from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from models.app import AppResponse
from services.supabase_service import SupabaseService
from typing import Dict, Any
import json

router = APIRouter()

def get_current_user(request: Request) -> str:
    user_id = getattr(request.state, 'user', None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user_id

def _get_app_template(app_data: Dict[str, Any]) -> str:
    """Generate HTML template based on app type and screens"""
    app_name = app_data.get('name', 'Meu App')
    color = app_data.get('color', '#4E9FFF')
    screens = app_data.get('screens', ['Home'])
    app_type = app_data.get('type', 'app')

    # Template mapping based on app type
    templates = {
        'app': _get_generic_app_template,
        'game': _get_game_app_template,
        'shopping': _get_shopping_app_template,
        'chat': _get_chat_app_template,
    }

    template_func = templates.get(app_type, _get_generic_app_template)
    return template_func(app_name, color, screens)

def _get_generic_app_template(app_name: str, color: str, screens: list) -> str:
    """Generic app template with navigation"""
    nav_items = ''.join([
        f'<div class="nav-item" data-screen="{screen}">{screen}</div>'
        for screen in screens[:4]  # Max 4 nav items
    ])

    screen_content = ''.join([
        f'''
        <div class="screen" id="screen-{screen.lower()}" style="display: {'block' if i == 0 else 'none'};">
            <div class="screen-header">
                <h2>{screen}</h2>
            </div>
            <div class="screen-content">
                <div class="content-card">
                    <h3>Bem-vindo à tela {screen}</h3>
                    <p>Esta é uma prévia da tela {screen} do seu app.</p>
                    <div class="mock-elements">
                        <div class="mock-button">Botão de Ação</div>
                        <div class="mock-input">
                            <label>Campo de entrada</label>
                            <input type="text" placeholder="Digite algo..." readonly>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        ''' for i, screen in enumerate(screens)
    ])

    return f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - Preview</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, {color}, {color}dd);
            min-height: 100vh;
            color: white;
            overflow-x: hidden;
        }}

        .app-container {{
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        .header {{
            padding: 20px;
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }}

        .app-title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 8px;
        }}

        .app-subtitle {{
            opacity: 0.8;
            font-size: 14px;
        }}

        .screen {{
            flex: 1;
            padding: 20px;
            display: none;
        }}

        .screen.active {{
            display: block;
        }}

        .screen-header {{
            margin-bottom: 20px;
        }}

        .screen-header h2 {{
            font-size: 28px;
            font-weight: 600;
        }}

        .screen-content {{
            max-width: 400px;
            margin: 0 auto;
        }}

        .content-card {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }}

        .content-card h3 {{
            margin-bottom: 12px;
            font-size: 20px;
        }}

        .content-card p {{
            margin-bottom: 20px;
            opacity: 0.9;
            line-height: 1.5;
        }}

        .mock-elements {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .mock-button {{
            background: {color};
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            font-weight: 500;
            cursor: pointer;
            transition: transform 0.2s;
        }}

        .mock-button:hover {{
            transform: scale(1.05);
        }}

        .mock-input {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .mock-input label {{
            font-size: 14px;
            font-weight: 500;
        }}

        .mock-input input {{
            padding: 12px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 16px;
        }}

        .mock-input input::placeholder {{
            color: rgba(255, 255, 255, 0.6);
        }}

        .nav-bar {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            padding: 16px;
            display: flex;
            justify-content: space-around;
            z-index: 1000;
        }}

        .nav-item {{
            text-align: center;
            opacity: 0.7;
            transition: opacity 0.3s;
            cursor: pointer;
            padding: 8px 12px;
            border-radius: 8px;
            font-weight: 500;
        }}

        .nav-item.active {{
            opacity: 1;
            background: rgba(255, 255, 255, 0.2);
        }}

        .preview-notice {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 12px;
            z-index: 1001;
        }}
    </style>
</head>
<body>
    <div class="preview-notice">
        🔍 Modo Preview - AppQuanta
    </div>

    <div class="app-container">
        <div class="header">
            <div class="app-title">{app_name}</div>
            <div class="app-subtitle">Preview interativo</div>
        </div>

        {screen_content}

        <div class="nav-bar">
            {nav_items}
        </div>
    </div>

    <script>
        // Navigation functionality
        const navItems = document.querySelectorAll('.nav-item');
        const screens = document.querySelectorAll('.screen');

        function switchScreen(screenName) {{
            // Hide all screens
            screens.forEach(screen => {{
                screen.classList.remove('active');
                screen.style.display = 'none';
            }});

            // Show selected screen
            const targetScreen = document.getElementById(`screen-${{screenName.toLowerCase()}}`);
            if (targetScreen) {{
                targetScreen.classList.add('active');
                targetScreen.style.display = 'block';
            }}

            // Update nav active state
            navItems.forEach(item => {{
                item.classList.remove('active');
                if (item.dataset.screen === screenName) {{
                    item.classList.add('active');
                }}
            }});
        }}

        // Add click handlers
        navItems.forEach(item => {{
            item.addEventListener('click', () => {{
                const screenName = item.dataset.screen;
                switchScreen(screenName);
            }});
        }});

        // Initialize first screen
        if (navItems.length > 0) {{
            switchScreen(navItems[0].dataset.screen);
        }}
    </script>
</body>
</html>
'''

def _get_game_app_template(app_name: str, color: str, screens: list) -> str:
    """Game app template with gaming elements"""
    return f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - Game Preview</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, {color}, #000);
            min-height: 100vh;
            color: white;
            overflow-x: hidden;
        }}

        .game-container {{
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}

        .game-title {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}

        .game-area {{
            width: 300px;
            height: 300px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 30px;
            border: 2px solid {color};
        }}

        .play-button {{
            background: {color};
            color: white;
            padding: 16px 32px;
            border-radius: 50px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}

        .play-button:hover {{
            transform: scale(1.1);
        }}

        .game-stats {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }}

        .stat {{
            background: rgba(255, 255, 255, 0.1);
            padding: 12px 20px;
            border-radius: 8px;
            text-align: center;
        }}

        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: {color};
        }}

        .stat-label {{
            font-size: 12px;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-title">{app_name}</div>

        <div class="game-stats">
            <div class="stat">
                <div class="stat-value">0</div>
                <div class="stat-label">Pontos</div>
            </div>
            <div class="stat">
                <div class="stat-value">1</div>
                <div class="stat-label">Nível</div>
            </div>
        </div>

        <div class="game-area">
            <div class="play-button" onclick="playGame()">JOGAR</div>
        </div>

        <div style="text-align: center; opacity: 0.8;">
            🎮 Game Preview - AppQuanta
        </div>
    </div>

    <script>
        function playGame() {{
            const button = document.querySelector('.play-button');
            button.textContent = '🎮 Jogando...';
            setTimeout(() => {{
                button.textContent = 'JOGAR';
            }}, 2000);
        }}
    </script>
</body>
</html>
'''

def _get_shopping_app_template(app_name: str, color: str, screens: list) -> str:
    """Shopping app template with products"""
    return f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - Shopping Preview</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, {color}, #f8f9fa);
            min-height: 100vh;
            color: #333;
        }}

        .store-container {{
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
        }}

        .store-header {{
            text-align: center;
            margin-bottom: 30px;
        }}

        .store-title {{
            font-size: 28px;
            font-weight: bold;
            color: {color};
            margin-bottom: 8px;
        }}

        .products-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin-bottom: 20px;
        }}

        .product-card {{
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .product-image {{
            width: 80px;
            height: 80px;
            background: {color};
            border-radius: 8px;
            margin: 0 auto 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
        }}

        .product-name {{
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .product-price {{
            color: {color};
            font-weight: bold;
        }}

        .cart-button {{
            background: {color};
            color: white;
            padding: 12px;
            border-radius: 8px;
            margin-top: 20px;
            cursor: pointer;
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <div class="store-container">
        <div class="store-header">
            <div class="store-title">{app_name}</div>
            <div style="opacity: 0.7;">🛒 Shopping Preview</div>
        </div>

        <div class="products-grid">
            <div class="product-card">
                <div class="product-image">📱</div>
                <div class="product-name">Produto 1</div>
                <div class="product-price">R$ 99,90</div>
            </div>
            <div class="product-card">
                <div class="product-image">💻</div>
                <div class="product-name">Produto 2</div>
                <div class="product-price">R$ 299,90</div>
            </div>
            <div class="product-card">
                <div class="product-image">🎧</div>
                <div class="product-name">Produto 3</div>
                <div class="product-price">R$ 149,90</div>
            </div>
            <div class="product-card">
                <div class="product-image">⌚</div>
                <div class="product-name">Produto 4</div>
                <div class="product-price">R$ 199,90</div>
            </div>
        </div>

        <button class="cart-button" onclick="addToCart()">
            🛒 Ver Carrinho (0 itens)
        </button>
    </div>

    <script>
        function addToCart() {{
            const button = document.querySelector('.cart-button');
            button.textContent = '🛒 Ver Carrinho (1 item)';
            setTimeout(() => {{
                button.textContent = '🛒 Ver Carrinho (0 itens)';
            }}, 2000);
        }}
    </script>
</body>
</html>
'''

def _get_chat_app_template(app_name: str, color: str, screens: list) -> str:
    """Chat app template with messages"""
    return f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - Chat Preview</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 0;
        }}

        .chat-container {{
            max-width: 400px;
            margin: 0 auto;
            height: 100vh;
            background: white;
            display: flex;
            flex-direction: column;
        }}

        .chat-header {{
            background: {color};
            color: white;
            padding: 16px;
            font-weight: 600;
        }}

        .messages {{
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .message {{
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.4;
        }}

        .message.sent {{
            background: {color};
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }}

        .message.received {{
            background: #f0f0f0;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }}

        .message-input {{
            padding: 16px;
            border-top: 1px solid #eee;
            display: flex;
            gap: 12px;
        }}

        .message-input input {{
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #ddd;
            border-radius: 24px;
            outline: none;
        }}

        .send-button {{
            background: {color};
            color: white;
            border: none;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            {app_name} 💬
        </div>

        <div class="messages" id="messages">
            <div class="message received">
                Olá! Bem-vindo ao chat preview do AppQuanta!
            </div>
            <div class="message sent">
                Obrigado! Como funciona?
            </div>
            <div class="message received">
                Esta é uma prévia do seu app de chat. Você pode personalizar as mensagens e funcionalidades.
            </div>
        </div>

        <div class="message-input">
            <input type="text" placeholder="Digite sua mensagem..." id="messageInput">
            <button class="send-button" onclick="sendMessage()">📤</button>
        </div>
    </div>

    <script>
        function sendMessage() {{
            const input = document.getElementById('messageInput');
            const messages = document.getElementById('messages');

            if (input.value.trim()) {{
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message sent';
                messageDiv.textContent = input.value;
                messages.appendChild(messageDiv);
                input.value = '';

                // Scroll to bottom
                messages.scrollTop = messages.scrollHeight;

                // Simulate response
                setTimeout(() => {{
                    const responseDiv = document.createElement('div');
                    responseDiv.className = 'message received';
                    responseDiv.textContent = 'Mensagem recebida! 👍';
                    messages.appendChild(responseDiv);
                    messages.scrollTop = messages.scrollHeight;
                }}, 1000);
            }}
        }}

        // Enter key support
        document.getElementById('messageInput').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                sendMessage();
            }}
        }});
    </script>
</body>
</html>
'''

@router.get("/apps/{app_id}/preview", response_class=HTMLResponse)
async def get_app_preview(app_id: str, request: Request):
    """Generate and return HTML preview for an app"""
    user_id = get_current_user(request)

    try:
        # Get app data
        app = SupabaseService.get_app(app_id, user_id)
        if not app:
            raise HTTPException(status_code=404, detail="App not found or access denied")

        # Convert app to dict and add additional preview data
        app_dict = app.dict()

        # Add default preview data if not present
        if 'color' not in app_dict or not app_dict['color']:
            app_dict['color'] = '#4E9FFF'

        if 'screens' not in app_dict or not app_dict['screens']:
            app_dict['screens'] = ['Home', 'About', 'Contact']

        if 'type' not in app_dict or not app_dict['type']:
            app_dict['type'] = 'app'

        # Generate HTML preview
        html_content = _get_app_template(app_dict)

        return HTMLResponse(content=html_content, status_code=200)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating preview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate preview: {str(e)}")

@router.post("/apps/{app_id}/generate-apk", response_model=dict)
async def generate_apk(app_id: str, request: Request):
    """Generate APK for an app (placeholder for future implementation)"""
    user_id = get_current_user(request)

    try:
        # Get app data
        app = SupabaseService.get_app(app_id, user_id)
        if not app:
            raise HTTPException(status_code=404, detail="App not found or access denied")

        # For now, return a placeholder response
        # In the future, this would trigger actual APK generation
        return {
            "success": True,
            "message": "APK generation started. This feature will be available soon.",
            "data": {
                "app_id": app_id,
                "status": "queued",
                "estimated_time": "5-10 minutes"
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start APK generation: {str(e)}")

@router.get("/apps/{app_id}/apk-status", response_model=dict)
async def get_apk_status(app_id: str, request: Request):
    """Get APK generation status"""
    user_id = get_current_user(request)

    try:
        # Get app data
        app = SupabaseService.get_app(app_id, user_id)
        if not app:
            raise HTTPException(status_code=404, detail="App not found or access denied")

        # For now, return placeholder status
        # In the future, this would check actual generation status
        return {
            "success": True,
            "message": "APK status retrieved.",
            "data": {
                "app_id": app_id,
                "status": "not_started",  # pending, generating, completed, failed
                "progress": 0,
                "apk_url": None
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get APK status: {str(e)}")
