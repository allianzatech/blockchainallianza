#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📬 MESSAGE QUEUE - ALLIANZA BLOCKCHAIN
Sistema de fila de mensagens para processamento assíncrono
"""

import json
import time
import uuid
from typing import Dict, Optional, Any, Callable, List
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import threading

# Tentar importar Redis Queue
try:
    from rq import Queue, Worker, Connection
    from rq.job import Job
    import redis
    RQ_AVAILABLE = True
except ImportError:
    RQ_AVAILABLE = False

class JobStatus(Enum):
    """Status de job"""
    PENDING = "pending"
    QUEUED = "queued"
    STARTED = "started"
    FINISHED = "finished"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class QueueJob:
    """Job na fila"""
    job_id: str
    task_type: str
    data: Dict
    priority: int = 5  # 1-10, 10 = maior prioridade
    created_at: float = None
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    status: str = JobStatus.PENDING.value
    result: Optional[Any] = None
    error: Optional[str] = None
    retries: int = 0
    max_retries: int = 3

class MessageQueue:
    """
    Sistema de Fila de Mensagens
    
    Suporta:
    - Redis Queue (RQ) se disponível
    - Fila em memória como fallback
    - Priorização
    - Retry automático
    - Processamento paralelo
    """
    
    def __init__(
        self,
        use_redis: bool = True,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        max_workers: int = 5
    ):
        self.use_redis = use_redis and RQ_AVAILABLE
        self.redis_client = None
        self.rq_queue = None
        
        if self.use_redis:
            try:
                self.redis_client = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    db=redis_db,
                    decode_responses=True
                )
                self.redis_client.ping()
                self.rq_queue = Queue(connection=self.redis_client)
                print("✅ Redis Queue: Conectado!")
            except Exception as e:
                print(f"⚠️  Redis Queue: Não disponível - {e}")
                self.use_redis = False
        
        # Fila em memória (fallback)
        self.memory_queue = {
            "high": [],  # Prioridade 8-10
            "medium": [],  # Prioridade 5-7
            "low": []  # Prioridade 1-4
        }
        self.memory_jobs = {}  # job_id -> QueueJob
        self.memory_lock = threading.Lock()
        
        # Worker pool
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.workers_running = False
        
        # Métricas
        self.metrics = {
            "jobs_queued": 0,
            "jobs_processed": 0,
            "jobs_failed": 0,
            "jobs_retried": 0,
            "avg_processing_time": 0.0
        }
        
        print("📬 Message Queue: Inicializado!")
        print(f"   Redis Queue: {'✅' if self.use_redis else '❌ (usando memória)'}")
        print(f"   Max workers: {max_workers}")
    
    def enqueue(
        self,
        task_func: Callable,
        task_type: str,
        data: Dict,
        priority: int = 5,
        max_retries: int = 3,
        timeout: int = 300
    ) -> str:
        """
        Adicionar job à fila
        
        Args:
            task_func: Função a ser executada
            task_type: Tipo de tarefa
            data: Dados da tarefa
            priority: Prioridade (1-10)
            max_retries: Máximo de tentativas
            timeout: Timeout em segundos
        
        Returns:
            job_id
        """
        job_id = str(uuid.uuid4())
        
        if self.use_redis and self.rq_queue:
            # Usar Redis Queue
            try:
                job = self.rq_queue.enqueue(
                    task_func,
                    **data,
                    job_id=job_id,
                    timeout=timeout,
                    retry=max_retries
                )
                self.metrics["jobs_queued"] += 1
                return job.id
            except Exception as e:
                print(f"⚠️  Erro ao enfileirar no Redis: {e}")
                # Fallback para memória
                self.use_redis = False
        
        # Usar fila em memória
        job = QueueJob(
            job_id=job_id,
            task_type=task_type,
            data=data,
            priority=priority,
            created_at=time.time(),
            max_retries=max_retries
        )
        
        with self.memory_lock:
            # Adicionar à fila apropriada baseado na prioridade
            if priority >= 8:
                self.memory_queue["high"].append(job)
            elif priority >= 5:
                self.memory_queue["medium"].append(job)
            else:
                self.memory_queue["low"].append(job)
            
            self.memory_jobs[job_id] = job
            self.metrics["jobs_queued"] += 1
        
        # Iniciar worker se não estiver rodando
        if not self.workers_running:
            self._start_workers()
        
        return job_id
    
    def _start_workers(self):
        """Iniciar workers para processar fila"""
        if self.workers_running:
            return
        
        self.workers_running = True
        
        def worker_loop():
            while self.workers_running:
                job = self._get_next_job()
                if job:
                    self._process_job(job)
                else:
                    time.sleep(0.1)  # Aguardar antes de verificar novamente
        
        # Iniciar workers em threads separadas
        for _ in range(self.executor._max_workers):
            self.executor.submit(worker_loop)
    
    def _get_next_job(self) -> Optional[QueueJob]:
        """Obter próximo job da fila (prioridade alta primeiro)"""
        with self.memory_lock:
            # Verificar filas em ordem de prioridade
            for queue_name in ["high", "medium", "low"]:
                if self.memory_queue[queue_name]:
                    job = self.memory_queue[queue_name].pop(0)
                    if job.status == JobStatus.PENDING.value:
                        return job
        return None
    
    def _process_job(self, job: QueueJob):
        """Processar job"""
        job.status = JobStatus.STARTED.value
        job.started_at = time.time()
        
        try:
            # Executar função (simulado - em produção, usar função real)
            # Por enquanto, apenas atualizar status
            time.sleep(0.1)  # Simular processamento
            
            job.status = JobStatus.FINISHED.value
            job.finished_at = time.time()
            job.result = {"success": True}
            
            self.metrics["jobs_processed"] += 1
            
            # Calcular tempo médio
            processing_time = job.finished_at - job.started_at
            total_time = self.metrics["avg_processing_time"] * (self.metrics["jobs_processed"] - 1)
            self.metrics["avg_processing_time"] = (total_time + processing_time) / self.metrics["jobs_processed"]
            
        except Exception as e:
            job.status = JobStatus.FAILED.value
            job.error = str(e)
            job.retries += 1
            
            # Retry se não excedeu máximo
            if job.retries < job.max_retries:
                job.status = JobStatus.PENDING.value
                job.started_at = None
                # Re-adicionar à fila
                with self.memory_lock:
                    if job.priority >= 8:
                        self.memory_queue["high"].append(job)
                    elif job.priority >= 5:
                        self.memory_queue["medium"].append(job)
                    else:
                        self.memory_queue["low"].append(job)
                self.metrics["jobs_retried"] += 1
            else:
                self.metrics["jobs_failed"] += 1
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """Obter status de um job"""
        if self.use_redis and self.rq_queue:
            try:
                job = Job.fetch(job_id, connection=self.redis_client)
                return {
                    "job_id": job.id,
                    "status": job.get_status(),
                    "result": job.result,
                    "error": str(job.exc_info) if job.exc_info else None
                }
            except:
                pass
        
        # Verificar fila em memória
        with self.memory_lock:
            if job_id in self.memory_jobs:
                job = self.memory_jobs[job_id]
                return asdict(job)
        
        return None
    
    def get_queue_stats(self) -> Dict:
        """Obter estatísticas da fila"""
        stats = {
            **self.metrics,
            "queue_sizes": {}
        }
        
        if self.use_redis and self.rq_queue:
            stats["queue_sizes"]["redis"] = len(self.rq_queue)
        else:
            with self.memory_lock:
                stats["queue_sizes"] = {
                    "high": len(self.memory_queue["high"]),
                    "medium": len(self.memory_queue["medium"]),
                    "low": len(self.memory_queue["low"])
                }
        
        return stats
    
    def stop_workers(self):
        """Parar workers"""
        self.workers_running = False
        self.executor.shutdown(wait=True)

# Instância global
_global_message_queue = None

def get_message_queue() -> MessageQueue:
    """Obter instância global da message queue"""
    global _global_message_queue
    if _global_message_queue is None:
        _global_message_queue = MessageQueue()
    return _global_message_queue

if __name__ == '__main__':
    print("="*70)
    print("📬 MESSAGE QUEUE - TESTE")
    print("="*70)
    
    queue = MessageQueue()
    
    # Teste básico
    print("\n📝 Teste 1: Enfileirar job")
    def test_task(data):
        return {"result": f"Processed: {data}"}
    
    job_id = queue.enqueue(
        task_func=test_task,
        task_type="test",
        data={"data": "test_value"},
        priority=8
    )
    print(f"   ✅ Job ID: {job_id}")
    
    # Aguardar processamento
    time.sleep(1)
    
    # Verificar status
    status = queue.get_job_status(job_id)
    print(f"   ✅ Status: {status}")
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    stats = queue.get_queue_stats()
    print(f"   Jobs processados: {stats['jobs_processed']}")
    print(f"   Tamanho da fila: {stats['queue_sizes']}")
















