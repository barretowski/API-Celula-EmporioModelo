import logging
import os

# Criação de diretórios para armazenar os logs
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Função para configurar o logger
def setup_logger(celula_name: str, level=logging.DEBUG):
    log_path = os.path.join(log_dir, celula_name)
    os.makedirs(log_path, exist_ok=True)
    
    # Configuração do logger específico para a célula
    logger = logging.getLogger(celula_name)
    logger.setLevel(level)
    
    # Formato de log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    
    # Criação de arquivos de log (ex: error.log, debug.log)
    file_handler_error = logging.FileHandler(os.path.join(log_path, "error.log"))
    file_handler_error.setLevel(logging.ERROR)
    file_handler_error.setFormatter(formatter)

    file_handler_debug = logging.FileHandler(os.path.join(log_path, "debug.log"))
    file_handler_debug.setLevel(logging.DEBUG)
    file_handler_debug.setFormatter(formatter)
    
    # Adicionando handlers ao logger
    logger.addHandler(file_handler_error)
    logger.addHandler(file_handler_debug)
    
    return logger
