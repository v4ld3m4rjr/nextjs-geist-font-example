import bcrypt
import jwt
import datetime
import streamlit as st
from utils.database import query_db
import psycopg2

SECRET_KEY = "your_secret_key_here"  # Em produção, usar variável de ambiente

def hash_password(password):
    """
    Cria um hash seguro da senha
    """
    try:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    except Exception as e:
        st.error(f"Erro ao criar hash da senha: {str(e)}")
        raise

def check_password(password, hashed):
    """
    Verifica se a senha corresponde ao hash
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    except Exception as e:
        st.error(f"Erro ao verificar senha: {str(e)}")
        return False

def create_token(user_id):
    """
    Cria um token JWT para o usuário
    """
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        st.error(f"Erro ao criar token: {str(e)}")
        raise

def verify_token(token):
    """
    Verifica e decodifica um token JWT
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        st.warning("Sessão expirada. Por favor, faça login novamente.")
        return None
    except jwt.InvalidTokenError:
        st.error("Token inválido.")
        return None
    except Exception as e:
        st.error(f"Erro ao verificar token: {str(e)}")
        return None

def validate_registration_data(email, password, name):
    """
    Valida os dados de registro
    """
    if not email or not password or not name:
        raise ValueError("Todos os campos são obrigatórios")
    
    if len(password) < 6:
        raise ValueError("A senha deve ter pelo menos 6 caracteres")
    
    if not '@' in email:
        raise ValueError("Email inválido")
    
    if len(name) < 2:
        raise ValueError("Nome deve ter pelo menos 2 caracteres")

def register_user(email, password, name):
    """
    Registra um novo usuário
    """
    try:
        # Validar dados
        validate_registration_data(email, password, name)
        
        # Verificar se email já existe
        check_query = "SELECT id FROM athlete_users WHERE email = %s"
        existing_user = query_db(check_query, (email,))
        
        if existing_user:
            raise ValueError("Este email já está registrado")
        
        # Criar hash da senha
        hashed = hash_password(password)
        
        # Inserir novo usuário
        query = """
        INSERT INTO athlete_users (email, password_hash, name, created_at) 
        VALUES (%s, %s, %s, NOW())
        """
        
        query_db(query, (email, hashed, name))
        st.success("Usuário registrado com sucesso!")
        return True
        
    except ValueError as e:
        st.error(str(e))
        return False
    except psycopg2.Error as e:
        st.error(f"Erro de banco de dados: {str(e)}")
        return False
    except Exception as e:
        st.error(f"Erro ao registrar usuário: {str(e)}")
        return False

def authenticate_user(email, password):
    """
    Autentica um usuário
    """
    try:
        if not email or not password:
            raise ValueError("Email e senha são obrigatórios")
        
        query = "SELECT id, password_hash FROM athlete_users WHERE email = %s"
        result = query_db(query, (email,))
        
        if not result:
            raise ValueError("Email ou senha incorretos")
        
        user = result[0]
        if check_password(password, user['password_hash'].tobytes()):
            return user['id']
        else:
            raise ValueError("Email ou senha incorretos")
            
    except ValueError as e:
        st.error(str(e))
        return None
    except Exception as e:
        st.error(f"Erro ao autenticar usuário: {str(e)}")
        return None

def get_user_info(user_id):
    """
    Obtém informações do usuário
    """
    try:
        query = "SELECT id, email, name, created_at FROM athlete_users WHERE id = %s"
        result = query_db(query, (user_id,))
        return result[0] if result else None
    except Exception as e:
        st.error(f"Erro ao obter informações do usuário: {str(e)}")
        return None
