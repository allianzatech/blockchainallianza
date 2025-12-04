#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 Leaderboard de Contribuições - Allianza Testnet
Sistema de gamificação para desenvolvedores
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import hashlib

class TestnetLeaderboard:
    """Sistema de leaderboard para gamificar contribuições"""
    
    def __init__(self, data_dir: str = "proofs/testnet/leaderboard"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.leaderboard_file = self.data_dir / "leaderboard.json"
        self.activities_file = self.data_dir / "activities.json"
        
        # Carregar dados existentes
        self.leaderboard = self._load_leaderboard()
        self.activities = self._load_activities()
    
    def _load_leaderboard(self) -> Dict:
        """Carregar leaderboard do arquivo"""
        if self.leaderboard_file.exists():
            try:
                with open(self.leaderboard_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"users": {}, "last_updated": datetime.now().isoformat()}
    
    def _load_activities(self) -> List[Dict]:
        """Carregar atividades recentes"""
        if self.activities_file.exists():
            try:
                with open(self.activities_file, 'r', encoding='utf-8') as f:
                    activities = json.load(f)
                    # Filtrar atividades antigas (manter apenas últimas 100)
                    cutoff = datetime.now() - timedelta(days=7)
                    return [
                        a for a in activities 
                        if datetime.fromisoformat(a.get('timestamp', '2000-01-01')) > cutoff
                    ][:100]
            except:
                pass
        return []
    
    def _save_leaderboard(self):
        """Salvar leaderboard"""
        self.leaderboard["last_updated"] = datetime.now().isoformat()
        with open(self.leaderboard_file, 'w', encoding='utf-8') as f:
            json.dump(self.leaderboard, f, indent=2, ensure_ascii=False)
    
    def _save_activities(self):
        """Salvar atividades"""
        # Manter apenas últimas 100 atividades
        self.activities = self.activities[-100:]
        with open(self.activities_file, 'w', encoding='utf-8') as f:
            json.dump(self.activities, f, indent=2, ensure_ascii=False)
    
    def _get_user_id(self, identifier: str) -> str:
        """Gerar ID único para usuário baseado em identificador"""
        # Usar hash do identificador para privacidade
        return hashlib.sha256(identifier.encode()).hexdigest()[:16]
    
    def _get_or_create_user(self, identifier: str, name: Optional[str] = None) -> str:
        """Obter ou criar usuário no leaderboard"""
        user_id = self._get_user_id(identifier)
        
        if user_id not in self.leaderboard["users"]:
            self.leaderboard["users"][user_id] = {
                "name": name or f"User_{user_id[:8]}",
                "points": 0,
                "tests_run": 0,
                "proofs_generated": 0,
                "qss_requests": 0,
                "first_seen": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat(),
                "badges": []
            }
        
        self.leaderboard["users"][user_id]["last_active"] = datetime.now().isoformat()
        return user_id
    
    def add_activity(self, activity_type: str, identifier: str, details: Dict = None):
        """Adicionar atividade ao leaderboard"""
        user_id = self._get_or_create_user(identifier)
        user = self.leaderboard["users"][user_id]
        
        # Pontos por tipo de atividade
        points_map = {
            "test_run": 10,
            "test_success": 20,
            "proof_generated": 15,
            "qss_request": 5,
            "first_test": 50,  # Bônus para primeiro teste
            "first_proof": 50,  # Bônus para primeira prova
            "all_tests_passed": 100,  # Bônus para passar todos os testes
        }
        
        points = points_map.get(activity_type, 0)
        user["points"] += points
        
        # Atualizar contadores
        if activity_type == "test_run":
            user["tests_run"] += 1
            if user["tests_run"] == 1:
                self._add_badge(user_id, "first_test")
        elif activity_type == "proof_generated":
            user["proofs_generated"] += 1
            if user["proofs_generated"] == 1:
                self._add_badge(user_id, "first_proof")
        elif activity_type == "qss_request":
            user["qss_requests"] += 1
        
        # Adicionar à lista de atividades
        activity = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "user_name": user["name"],
            "type": activity_type,
            "points": points,
            "details": details or {}
        }
        self.activities.append(activity)
        
        # Salvar
        self._save_leaderboard()
        self._save_activities()
        
        return points
    
    def _add_badge(self, user_id: str, badge_type: str):
        """Adicionar badge ao usuário"""
        if user_id not in self.leaderboard["users"]:
            return
        
        badges_map = {
            "first_test": {"name": "Primeiro Teste", "icon": "🎯", "color": "blue"},
            "first_proof": {"name": "Primeira Prova", "icon": "🔐", "color": "green"},
            "all_tests_passed": {"name": "Mestre dos Testes", "icon": "🏆", "color": "gold"},
            "qss_master": {"name": "Mestre QSS", "icon": "⚡", "color": "purple"},
            "power_user": {"name": "Power User", "icon": "💪", "color": "red"},
        }
        
        badge = badges_map.get(badge_type)
        if badge and badge_type not in [b["type"] for b in self.leaderboard["users"][user_id]["badges"]]:
            self.leaderboard["users"][user_id]["badges"].append({
                "type": badge_type,
                "name": badge["name"],
                "icon": badge["icon"],
                "color": badge["color"],
                "earned_at": datetime.now().isoformat()
            })
    
    def get_top_users(self, limit: int = 10) -> List[Dict]:
        """Obter top usuários por pontos"""
        users = list(self.leaderboard["users"].values())
        users.sort(key=lambda u: u["points"], reverse=True)
        return users[:limit]
    
    def get_recent_activities(self, limit: int = 20) -> List[Dict]:
        """Obter atividades recentes"""
        return self.activities[-limit:][::-1]  # Reverter para mostrar mais recentes primeiro
    
    def get_user_stats(self, identifier: str) -> Optional[Dict]:
        """Obter estatísticas de um usuário"""
        user_id = self._get_user_id(identifier)
        if user_id in self.leaderboard["users"]:
            user = self.leaderboard["users"][user_id].copy()
            user["rank"] = self._get_user_rank(user_id)
            return user
        return None
    
    def _get_user_rank(self, user_id: str) -> int:
        """Obter ranking do usuário"""
        users = list(self.leaderboard["users"].values())
        users.sort(key=lambda u: u["points"], reverse=True)
        
        for idx, user in enumerate(users, 1):
            if self._get_user_id(user.get("name", "")) == user_id:
                return idx
        
        return len(users) + 1
    
    def get_stats_summary(self) -> Dict:
        """Obter resumo de estatísticas"""
        users = self.leaderboard["users"]
        total_users = len(users)
        total_points = sum(u["points"] for u in users.values())
        total_tests = sum(u["tests_run"] for u in users.values())
        total_proofs = sum(u["proofs_generated"] for u in users.values())
        total_qss = sum(u["qss_requests"] for u in users.values())
        
        return {
            "total_users": total_users,
            "total_points": total_points,
            "total_tests": total_tests,
            "total_proofs": total_proofs,
            "total_qss_requests": total_qss,
            "avg_points_per_user": total_points / total_users if total_users > 0 else 0,
            "last_updated": self.leaderboard.get("last_updated", datetime.now().isoformat())
        }

