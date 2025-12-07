"""
Chat Router - Main chat endpoint for customer interactions.
Handles message buffering/debouncing and delegates to Gemini service.
"""
from typing import Dict, List
import asyncio
import uuid

from fastapi import APIRouter, HTTPException, status

from app.models.schemas import ChatRequest, ChatResponse
from app.services.gemini_service import get_gemini_service
from app.core.config import settings

router = APIRouter(prefix="/chat", tags=["Chat"])

# Message buffer for debouncing rapid messages
message_buffer: Dict[str, List[str]] = {}
latest_request_token: Dict[str, str] = {}


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message from a customer.
    
    Implements debouncing to group rapid consecutive messages.
    Delegates processing to GeminiService for AI response generation.
    
    Args:
        request: ChatRequest with mensaje and telefono
        
    Returns:
        ChatResponse with tipo, mensaje, and optional orden data
    """
    try:
        phone = request.telefono
        
        # Initialize buffer for this phone if needed
        if phone not in message_buffer:
            message_buffer[phone] = []
        
        # Add message to buffer
        message_buffer[phone].append(request.mensaje)
        
        # Generate unique token for this request
        current_token = str(uuid.uuid4())
        latest_request_token[phone] = current_token
        
        # Wait for potential additional messages (debounce)
        await asyncio.sleep(settings.MESSAGE_BUFFER_SECONDS)
        
        # Check if this is still the latest request
        if latest_request_token.get(phone) != current_token:
            # Another message arrived, this one will be grouped
            return ChatResponse(
                tipo="ignorar",
                mensaje="Mensaje agrupado con el siguiente."
            )
        
        # This is the latest request - process all buffered messages
        full_message = " ".join(message_buffer[phone])
        message_buffer[phone] = []  # Clear buffer
        
        # Process with Gemini
        gemini = get_gemini_service()
        response = await gemini.process_chat(phone, full_message)
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando mensaje: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint for the chat service."""
    return {
        "status": "healthy",
        "service": "chat",
        "model": settings.GEMINI_MODEL
    }