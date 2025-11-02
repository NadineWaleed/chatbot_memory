# monitoring.py
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MonitoringSystem:
    """Centralized monitoring & logging system for all runtime and user events."""
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MonitoringSystem, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            try:
                self.logs_dir = Path("logs")
                self.logs_dir.mkdir(exist_ok=True)
                self.setup_logging()
                self._initialized = True
            except Exception as e:
                print(f"⚠️ Failed to initialize monitoring system: {e}")

    # === SETUP ===
    def setup_logging(self):
        """Configure file + console logging."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        daily_log_file = self.logs_dir / f"{current_date}.log"
        comprehensive_log_file = self.logs_dir / "comprehensive.log"

        self.logger = logging.getLogger("HealthInsuranceMonitor")
        self.logger.setLevel(logging.INFO)

        # Remove duplicate handlers
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Daily file handler
        daily_handler = logging.FileHandler(daily_log_file, encoding="utf-8", mode="a")
        daily_handler.setFormatter(formatter)

        # Comprehensive log handler
        comprehensive_handler = logging.FileHandler(comprehensive_log_file, encoding="utf-8", mode="a")
        comprehensive_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Attach handlers
        self.logger.addHandler(daily_handler)
        self.logger.addHandler(comprehensive_handler)
        self.logger.addHandler(console_handler)

        self.logger.info("✅ Monitoring system initialized.")

    # === LOG METHODS ===
    def log_event(self, event_name: str, level: str = "info", **kwargs):
        """Generic structured event logging helper."""
        data = {
            "event": event_name,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        message = json.dumps(data, ensure_ascii=False)
        getattr(self.logger, level.lower(), self.logger.info)(message)

    def log_question_received(self, question: str, request_id: str, user_ip: str = None):
        self.log_event(
            "question_received",
            request_id=request_id,
            question=question,
            user_ip=user_ip or "unknown"
        )

    def log_rephrasing_start(self, request_id: str, original_question: str):
        self.log_event("rephrasing_start", request_id=request_id, original_question=original_question)

    def log_rephrasing_result(self, request_id: str, original: str, rephrased: str):
        self.log_event("rephrasing_result", request_id=request_id, original_question=original, rephrased_question=rephrased)

    def log_qa_processing_start(self, request_id: str, question: str):
        self.log_event("qa_processing_start", request_id=request_id, question=question)

    def log_qa_processing_result(self, request_id: str, question: str, answer: str, sources: str = ""):
        self.log_event(
            "qa_processing_result",
            request_id=request_id,
            question=question,
            answer=(answer[:500] + "...") if len(answer) > 500 else answer,
            answer_length=len(answer),
            has_sources=bool(sources)
        )

    def log_error(self, request_id: str, error_message: str, context: str = ""):
        self.log_event("error", level="error", request_id=request_id, error_message=error_message, context=context)

    def log_processing_time(self, request_id: str, step: str, time_taken: float):
        self.log_event(
            "processing_time",
            request_id=request_id,
            step=step,
            time_taken_seconds=round(time_taken, 3)
        )

    def log_system_event(self, event_type: str, details: Dict[str, Any]):
        self.log_event("system_event", event_type=event_type, details=details)


# ✅ Singleton instance
monitor = MonitoringSystem()
