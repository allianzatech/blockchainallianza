#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Processamento Assíncrono
Filas para processamento de tarefas pesadas
"""

import time
import json
from typing import Dict, Optional, Callable, Any
from queue import Queue
from threading import Thread
from enum import Enum

# Tentar importar Redis Queue, mas funcionar sem ele
try:
    from rq import Queue as RQQueue
    from rq.job import Job
    RQ_AVAILABLE = True
except ImportError:
    RQ_AVAILABLE = False
    print("⚠️  RQ não disponível. Usando fila em memória.")

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class AsyncProcessor:
    """Processador assíncrono de tarefas"""
    
    def __init__(self, use_redis: bool = False, redis_host: str = "localhost", redis_port: int = 6379):
        self.use_redis = use_redis and RQ_AVAILABLE
        self.tasks = {}  # Armazenar status das tarefas
        self.task_queue = None
        self.workers = []
        self.worker_threads = []
        
        if self.use_redis:
            try:
                import redis
                redis_conn = redis.Redis(host=redis_host, port=redis_port)
                self.task_queue = RQQueue('allianza_tasks', connection=redis_conn)
                print("✅ Redis Queue conectado!")
            except Exception as e:
                print(f"⚠️  Redis Queue não disponível: {e}. Usando fila em memória.")
                self.use_redis = False
        
        if not self.use_redis:
            self.task_queue = Queue()
            self._start_workers(num_workers=3)
    
    def _start_workers(self, num_workers: int = 3):
        """Inicia workers para processar tarefas"""
        def worker():
            while True:
                try:
                    task = self.task_queue.get(timeout=1)
                    if task is None:
                        break
                    
                    task_id, func, args, kwargs = task
                    self.tasks[task_id]["status"] = TaskStatus.PROCESSING.value
                    
                    try:
                        result = func(*args, **kwargs)
                        self.tasks[task_id]["status"] = TaskStatus.COMPLETED.value
                        self.tasks[task_id]["result"] = result
                        self.tasks[task_id]["completed_at"] = time.time()
                    except Exception as e:
                        self.tasks[task_id]["status"] = TaskStatus.FAILED.value
                        self.tasks[task_id]["error"] = str(e)
                        self.tasks[task_id]["failed_at"] = time.time()
                    
                    self.task_queue.task_done()
                except:
                    continue
        
        for i in range(num_workers):
            thread = Thread(target=worker, daemon=True)
            thread.start()
            self.worker_threads.append(thread)
    
    def enqueue(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> str:
        """
        Adiciona tarefa à fila
        
        Returns:
            task_id
        """
        import secrets
        task_id = f"task_{int(time.time())}_{secrets.token_hex(8)}"
        
        # Registrar tarefa
        self.tasks[task_id] = {
            "task_id": task_id,
            "status": TaskStatus.PENDING.value,
            "created_at": time.time(),
            "function": func.__name__
        }
        
        if self.use_redis:
            # Usar Redis Queue
            job = self.task_queue.enqueue(func, *args, **kwargs, job_id=task_id)
            self.tasks[task_id]["job_id"] = job.id
        else:
            # Usar fila em memória
            self.task_queue.put((task_id, func, args, kwargs))
        
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Obtém status de uma tarefa"""
        if task_id not in self.tasks:
            return None
        
        task_info = self.tasks[task_id].copy()
        
        # Se usando Redis Queue, atualizar status
        if self.use_redis and "job_id" in task_info:
            try:
                job = Job.fetch(task_info["job_id"], connection=self.task_queue.connection)
                if job.is_finished:
                    task_info["status"] = TaskStatus.COMPLETED.value
                    task_info["result"] = job.result
                elif job.is_failed:
                    task_info["status"] = TaskStatus.FAILED.value
                    task_info["error"] = str(job.exc_info)
            except Exception:
                pass
        
        return task_info
    
    def wait_for_task(self, task_id: str, timeout: int = 300) -> Optional[Dict]:
        """Aguarda conclusão de tarefa"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_task_status(task_id)
            if not status:
                return None
            
            if status["status"] in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value]:
                return status
            
            time.sleep(0.5)
        
        return {"status": "timeout", "task_id": task_id}

# Instância global
global_async_processor = AsyncProcessor()







