#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 SIEM EXPORTER - QaaS Enterprise
Exporta logs para Splunk, Elastic, e outros SIEMs
"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime, timezone
import sqlite3

class SIEMExporter:
    """Exportador de logs para SIEM (Splunk, Elastic, etc.)"""
    
    def __init__(self, db_path: str = "qaas_audit.db"):
        self.db_path = db_path
    
    def export_ndjson(self, limit: int = 1000, filters: Dict[str, Any] = None) -> str:
        """
        Exportar logs em formato ND-JSON (Newline Delimited JSON)
        Formato padrão para Splunk e Elasticsearch
        
        Args:
            limit: Número máximo de logs
            filters: Filtros opcionais (blockchain, action, etc.)
        
        Returns:
            String ND-JSON
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Construir query com filtros
        query = "SELECT * FROM audit_logs WHERE 1=1"
        params = []
        
        if filters:
            if filters.get("blockchain"):
                query += " AND blockchain = ?"
                params.append(filters["blockchain"])
            if filters.get("action"):
                query += " AND action = ?"
                params.append(filters["action"])
            if filters.get("user_id"):
                query += " AND user_id = ?"
                params.append(filters["user_id"])
            if filters.get("start_date"):
                query += " AND timestamp >= ?"
                params.append(filters["start_date"])
            if filters.get("end_date"):
                query += " AND timestamp <= ?"
                params.append(filters["end_date"])
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        # Converter para ND-JSON
        ndjson_lines = []
        for row in rows:
            log_dict = dict(zip(columns, row))
            # Adicionar metadados SIEM
            log_dict["_siem_source"] = "qaas_enterprise"
            log_dict["_siem_type"] = "quantum_security_audit"
            log_dict["_exported_at"] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            ndjson_lines.append(json.dumps(log_dict))
        
        conn.close()
        return "\n".join(ndjson_lines)
    
    def export_csv(self, limit: int = 1000) -> str:
        """Exportar logs em formato CSV"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM audit_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        # Gerar CSV
        csv_lines = [",".join(columns)]  # Header
        for row in rows:
            csv_lines.append(",".join([str(val) if val else "" for val in row]))
        
        conn.close()
        return "\n".join(csv_lines)
    
    def export_splunk_hec(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Exportar logs no formato Splunk HTTP Event Collector (HEC)
        
        Returns:
            Lista de eventos no formato HEC
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM audit_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        hec_events = []
        for row in rows:
            log_dict = dict(zip(columns, row))
            hec_event = {
                "time": log_dict.get("timestamp", ""),
                "host": "qaas-enterprise",
                "source": "quantum_security_service",
                "sourcetype": "qaas:audit",
                "event": log_dict
            }
            hec_events.append(hec_event)
        
        conn.close()
        return hec_events
    
    def export_elastic(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Exportar logs no formato Elasticsearch
        
        Returns:
            Lista de documentos Elasticsearch
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM audit_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        elastic_docs = []
        for row in rows:
            log_dict = dict(zip(columns, row))
            # Adicionar metadados Elastic
            elastic_doc = {
                "_index": "qaas-audit-logs",
                "_type": "_doc",
                "_source": log_dict
            }
            elastic_docs.append(elastic_doc)
        
        conn.close()
        return elastic_docs
















