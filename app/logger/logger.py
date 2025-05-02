import logging
import os
from datetime import datetime
import inspect

class Logger:
    """
    A logger class that configures logging for a specific module
    and writes log records to a dedicated file named after the module.

    Usage:
        In your module (e.g., my_module.py):
        ------------------------------------
        from module_logger import ModuleLogger # Assuming logger class is in module_logger.py
        logger = ModuleLogger(__name__) # Pass the module's __name__
        logger.info("This message comes from my_module")
        ------------------------------------
    """
    _loggers = {} # Class-level dictionary to store initialized loggers

    def __init__(self, module_name: str, log_level: int = logging.INFO, log_dir: str = "logs",
                 log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                 date_format: str = '%Y-%m-%d %H:%M:%S'):
        """
        Initializes the ModuleLogger.

        Args:
            module_name (str): The name of the module (__name__). Used for logger
                               identity and the log filename.
            log_level (int): The minimum logging level (e.g., logging.DEBUG, logging.INFO).
                             Defaults to logging.INFO.
            log_dir (str): The directory where log files will be stored.
                           Defaults to "logs". Will be created if it doesn't exist.
            log_format (str): The format string for log messages.
            date_format (str): The format string for the date/time in log messages.
        """
        self.module_name = module_name
        self.log_level = log_level
        self.log_dir = log_dir
        self.log_format = log_format
        self.date_format = date_format

        # Use class-level dictionary to avoid reconfiguring the same logger
        if module_name in Logger._loggers:
            self.logger = Logger._loggers[module_name]
        else:
            self.logger = self._setup_logger()
            Logger._loggers[module_name] = self.logger

    def _setup_logger(self) -> logging.Logger:
        """Configures and returns a logger instance."""
        # --- Get the logger instance for this module ---
        logger = logging.getLogger(self.module_name)
        logger.setLevel(self.log_level) # Set the minimum level for the logger

        # --- Prevent log messages from propagating to the root logger ---
        # This ensures messages only go to this module's specific file handler,
        # unless you explicitly add other handlers or change this setting.
        logger.propagate = False

        # --- Create log directory if it doesn't exist ---
        try:
            os.makedirs(self.log_dir, exist_ok=True)
        except OSError as e:
            # Use standard print for setup errors as logging might not be ready
            print(f"Error creating log directory '{self.log_dir}': {e}")
            # Fallback to basic console logging if directory fails? Or raise error?
            # For now, we'll continue and FileHandler will likely raise error.

        # --- Create File Handler ---
        log_file_name = f"{self.module_name}_{datetime.now().strftime("%Y-%m-%d")}.log"
        log_file_path = os.path.join(self.log_dir, log_file_name)
        try:
            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            file_handler.setLevel(self.log_level) # Set the minimum level for this handler
        except Exception as e:
             print(f"Error creating file handler for '{log_file_path}': {e}")
             # Consider raising an exception or handling this more gracefully
             raise # Re-raise the exception

        # --- Create Formatter ---
        formatter = logging.Formatter(self.log_format, datefmt=self.date_format)
        file_handler.setFormatter(formatter)

        # --- Add Handler to Logger (only if no handlers exist for this logger) ---
        # This check prevents adding duplicate handlers if __init__ were called
        # multiple times for the same module_name (though _loggers dict handles this now).
        if not logger.handlers:
            logger.addHandler(file_handler)
            print(f"Logger '{self.module_name}' configured. Logging to: {log_file_path}") # Optional: Confirm setup

        return logger

    # --- Convenience methods to call the underlying logger ---
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """Logs a message with level ERROR and exception information."""
        self.logger.exception(msg, *args, exc_info=exc_info, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        """Logs a message with the specified level."""
        self.logger.log(level, msg, *args, **kwargs)