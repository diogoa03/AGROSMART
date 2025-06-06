"""
Utilitários para gerenciamento de threads no AGROSMART.

Este módulo fornece classes e funções para:
- Execução segura de tarefas em threads
- Pool de threads com limite
- Decorators para sincronização
- Helpers para timeout
"""

import threading
import queue
from typing import Callable, Any, Optional
from functools import wraps
from concurrent.futures import ThreadPoolExecutor
from src.utils.logger import Logger

logger = Logger(__name__)

class ThreadSafeCounter:
    """Contador thread-safe com lock."""
    
    def __init__(self, initial: int = 0):
        self._value = initial
        self._lock = threading.Lock()
        
    def increment(self) -> int:
        """Incrementa o contador de forma thread-safe."""
        with self._lock:
            self._value += 1
            return self._value
            
    def decrement(self) -> int:
        """Decrementa o contador de forma thread-safe."""
        with self._lock:
            self._value -= 1
            return self._value
            
    @property
    def value(self) -> int:
        """Retorna valor atual do contador."""
        with self._lock:
            return self._value

class SafeQueue:
    """Fila thread-safe com timeout e capacity."""
    
    def __init__(self, maxsize: int = 0):
        self._queue = queue.Queue(maxsize=maxsize)
        
    def put(self, item: Any, timeout: Optional[float] = None) -> bool:
        """
        Adiciona item na fila com timeout.
        
        Args:
            item: Item para adicionar
            timeout: Timeout em segundos
            
        Returns:
            bool: True se sucesso, False se timeout
        """
        try:
            self._queue.put(item, timeout=timeout)
            return True
        except queue.Full:
            logger.warning("Queue full - item discarded")
            return False
            
    def get(self, timeout: Optional[float] = None) -> Optional[Any]:
        """
        Remove e retorna item da fila com timeout.
        
        Args:
            timeout: Timeout em segundos
            
        Returns:
            Any: Item removido ou None se timeout
        """
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

def synchronized(lock: Optional[threading.Lock] = None) -> Callable:
    """
    Decorator para sincronizar método/função.
    
    Args:
        lock: Lock opcional ou cria novo se None
        
    Returns:
        Callable: Função decorada
    """
    if lock is None:
        lock = threading.Lock()
        
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with lock:
                return func(*args, **kwargs)
        return wrapper
    return decorator

class ThreadPool:
    """Gerenciador de pool de threads."""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active = ThreadSafeCounter()
        
    def submit(self, func: Callable, *args, **kwargs) -> None:
        """
        Submete tarefa para execução.
        
        Args:
            func: Função a executar
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados
        """
        def wrapped():
            self.active.increment()
            try:
                func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in thread: {str(e)}")
            finally:
                self.active.decrement()
                
        self.executor.submit(wrapped)
        
    def shutdown(self, wait: bool = True) -> None:
        """
        Finaliza pool de threads.
        
        Args:
            wait: Se deve aguardar conclusão
        """
        self.executor.shutdown(wait=wait)
