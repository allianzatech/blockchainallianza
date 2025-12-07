#!/usr/bin/env python3
"""
Script para adicionar coluna metadata na tabela stakes
"""
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# Obter URL do banco (com fallback)
DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('NEON_DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL ou NEON_DATABASE_URL não configurada")
    exit(1)

print("=" * 80)
print("🔧 Adicionando coluna 'metadata' na tabela 'stakes'")
print("=" * 80)

try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True  # Usar autocommit para ALTER TABLE
    cursor = conn.cursor()
    
    print("✅ Conectado ao banco\n")
    
    # Verificar se a coluna já existe
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'stakes' AND column_name = 'metadata'
    """)
    
    if cursor.fetchone() is None:
        print("➕ Adicionando coluna 'metadata' (JSONB)...")
        cursor.execute("""
            ALTER TABLE stakes 
            ADD COLUMN metadata JSONB;
        """)
        print("✅ Coluna 'metadata' adicionada com sucesso!")
    else:
        print("✅ Coluna 'metadata' já existe")
    
    print("\n" + "=" * 80)
    print("✅ Migração concluída!")
    print("=" * 80)
    
    conn.close()
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

