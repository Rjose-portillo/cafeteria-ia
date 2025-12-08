"""
Scheduler Service - Manejo de tareas en segundo plano.
Usa APScheduler para programar mensajes de feedback post-venta.
"""
from typing import Optional
from datetime import datetime, timedelta, timezone
from functools import lru_cache
import random

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from app.services.firestore_service import get_firestore_service
from app.core.config import settings

class SchedulerService:
    """
    Singleton service for background tasks.
    Handles automated follow-up messages and scheduled notifications.
    """

    _instance: Optional['SchedulerService'] = None
    _scheduler: Optional[AsyncIOScheduler] = None

    def __new__(cls) -> 'SchedulerService':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._scheduler is None:
            self._scheduler = AsyncIOScheduler()
            # Configure scheduler with proper timezone
            self._scheduler.configure(timezone=timezone.utc)

    def start(self):
        """Start the scheduler."""
        if not self._scheduler.running:
            self._scheduler.start()
            print("⏰ Scheduler iniciado correctamente")

    def shutdown(self):
        """Shutdown the scheduler gracefully."""
        if self._scheduler and self._scheduler.running:
            self._scheduler.shutdown(wait=True)
            print("⏰ Scheduler detenido correctamente")

    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return self._scheduler is not None and self._scheduler.running

    async def _send_feedback_message(self, telefono: str, nombre_cliente: str):
        """
        Callback function executed by the scheduler.
        Injects a follow-up message into the chat history.
        """
        try:
            firestore = get_firestore_service()

            # Estrategias de mensaje aleatorias con más variedad
            opciones = [
                f"¡Hola {nombre_cliente}! 🌟 Esperamos que hayas disfrutado tu pedido. ¿Nos regalas 5 estrellitas en Google Maps? Ayuda mucho al equipo.",
                f"Oye {nombre_cliente}, ¿te gustó el café? ☕ Recuerda que si traes a un amigo, ambos ganan puntos en nuestro Plan de Justicia.",
                f"¡Qué onda {nombre_cliente}! Solo pasaba a confirmar que todo estuvo delicioso. ¡Bonito día! ✨",
                f"Hola {nombre_cliente} 👋 ¿Cómo estuvo tu experiencia en Justicia y Café? Tu opinión es muy importante para nosotros.",
                f"¡Saludos {nombre_cliente}! ☕ ¿Te gustaría recibir recomendaciones personalizadas la próxima vez? ¡Somos expertos en café!",
                f"Oye {nombre_cliente}, ¿sabes que tenemos un programa de fidelización? Cada compra te acerca más a recompensas deliciosas. 🌟"
            ]

            mensaje = random.choice(opciones)

            # Guardamos el mensaje en Firestore para que aparezca en el chat del cliente
            print(f"📧 Enviando feedback automático a {telefono} ({nombre_cliente})")
            success = await firestore.save_message(telefono, "model", mensaje)

            if success:
                print(f"✅ Feedback enviado exitosamente a {nombre_cliente}")
            else:
                print(f"❌ Error al enviar feedback a {nombre_cliente}")

        except Exception as e:
            print(f"❌ Error en _send_feedback_message para {telefono}: {e}")

    def schedule_feedback(self, telefono: str, nombre: str, delay_minutes: int = 30):
        """
        Schedule a feedback message for the future.

        Args:
            telefono: Customer phone number
            nombre: Customer name
            delay_minutes: Minutes to wait before sending (default: 30)
        """
        if not self._scheduler:
            print("❌ Scheduler no inicializado")
            return

        # Validate inputs
        if not telefono or not nombre:
            print("❌ Teléfono y nombre son requeridos para programar feedback")
            return

        run_date = datetime.now(timezone.utc) + timedelta(minutes=delay_minutes)

        # Para desarrollo/demo, podemos usar segundos en lugar de minutos
        if settings.DEBUG:
            run_date = datetime.now(timezone.utc) + timedelta(seconds=30)
            print(f"🐛 DEBUG MODE: Feedback programado en 30 segundos en lugar de {delay_minutes} minutos")

        job_id = f"feedback_{telefono}_{int(datetime.now().timestamp())}"

        try:
            self._scheduler.add_job(
                self._send_feedback_message,
                trigger=DateTrigger(run_date=run_date),
                args=[telefono, nombre],
                id=job_id,
                replace_existing=True,  # Replace if exists
                max_instances=1  # Only run once
            )
            print(f"⏰ Feedback programado para {nombre} ({telefono}) en {delay_minutes} min - Job ID: {job_id}")
        except Exception as e:
            print(f"❌ Error programando feedback para {nombre}: {e}")

    def cancel_feedback(self, telefono: str) -> bool:
        """
        Cancel any pending feedback jobs for a customer.

        Args:
            telefono: Customer phone number

        Returns:
            bool: True if jobs were cancelled, False otherwise
        """
        if not self._scheduler:
            return False

        try:
            # Find and remove jobs for this customer
            jobs_removed = 0
            for job in self._scheduler.get_jobs():
                if telefono in job.id and "feedback" in job.id:
                    job.remove()
                    jobs_removed += 1

            if jobs_removed > 0:
                print(f"🗑️ Cancelados {jobs_removed} jobs de feedback para {telefono}")
                return True
            else:
                print(f"ℹ️ No se encontraron jobs pendientes para {telefono}")
                return False

        except Exception as e:
            print(f"❌ Error cancelando feedback para {telefono}: {e}")
            return False

    def get_pending_jobs(self) -> list:
        """
        Get list of pending jobs for monitoring.

        Returns:
            list: List of pending job information
        """
        if not self._scheduler:
            return []

        try:
            jobs = []
            for job in self._scheduler.get_jobs():
                jobs.append({
                    'id': job.id,
                    'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None,
                    'func': job.func.__name__,
                    'args': job.args
                })
            return jobs
        except Exception as e:
            print(f"❌ Error obteniendo jobs pendientes: {e}")
            return []

@lru_cache()
def get_scheduler_service() -> SchedulerService:
    """Get singleton instance of SchedulerService."""
    return SchedulerService()