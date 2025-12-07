#!/usr/bin/env python3
"""
Migração: Alterar coluna password para permitir NULL
"""
import os
from dotenv import load_dotenv
from database_neon import NeonDatabase

load_dotenv()

def migrate_password_nullable():
    """Alterar coluna password para permitir NULL"""
    db = NeonDatabase()
    conn = None
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        print("🔄 Iniciando migração: password nullable...")
        
        # Verificar se a coluna tem constraint NOT NULL
        cursor.execute("""
            SELECT 
                column_name, 
                is_nullable,
                column_default
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'password'
        """)
        column_info = cursor.fetchone()
        
        if column_info:
            is_nullable = column_info.get('is_nullable', 'NO')
            print(f"📋 Estado atual da coluna password: is_nullable={is_nullable}")
            
            if is_nullable == 'NO':
                # Alterar para permitir NULL
                print("🔧 Alterando coluna password para permitir NULL...")
                cursor.execute("""
                    ALTER TABLE users 
                    ALTER COLUMN password DROP NOT NULL;
                """)
                conn.commit()
                print("✅ Coluna 'password' alterada para permitir NULL com sucesso!")
            else:
                print("✅ Coluna 'password' já permite NULL")
        else:
            print("⚠️  Coluna 'password' não encontrada na tabela 'users'")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
            conn.close()
        raise

if __name__ == "__main__":
    migrate_password_nullable()

