#!/usr/bin/env python3
"""
GPT API Bridge - Real OpenAI Integration
Provides webhook module and rate-limited GPT-4 access
"""

import openai
import time
import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from flask import Flask, request, jsonify
import threading
import queue

@dataclass
class APIConfig:
    openai_api_key: str
    model: str = "gpt-4"
    max_tokens: int = 4000
    temperature: float = 0.7
    rate_limit_rpm: int = 60
    fallback_model: str = "gpt-3.5-turbo"

class RateLimiter:
    def __init__(self, max_requests_per_minute: int):
        self.max_requests = max_requests_per_minute
        self.requests = queue.Queue()
        self.lock = threading.Lock()
    
    def can_make_request(self) -> bool:
        with self.lock:
            now = time.time()
            # Remove requests older than 1 minute
            while not self.requests.empty():
                if now - self.requests.queue[0] > 60:
                    self.requests.get()
                else:
                    break
            
            if self.requests.qsize() < self.max_requests:
                self.requests.put(now)
                return True
            return False

class GPTAPIBridge:
    def __init__(self, config: APIConfig):
        self.config = config
        self.rate_limiter = RateLimiter(config.rate_limit_rpm)
        openai.api_key = config.openai_api_key
        self.logger = logging.getLogger(__name__)
        
    def send_message(self, message: str, system_prompt: str = None) -> Dict:
        """Send message to GPT with rate limiting and fallback"""
        if not self.rate_limiter.can_make_request():
            return {
                "error": "Rate limit exceeded",
                "retry_after": 60,
                "status": "rate_limited"
            }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        try:
            # Try primary model first
            response = openai.ChatCompletion.create(
                model=self.config.model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            return {
                "response": response.choices[0].message.content,
                "model_used": self.config.model,
                "tokens_used": response.usage.total_tokens,
                "status": "success"
            }
            
        except openai.error.RateLimitError:
            self.logger.warning("Rate limit hit, waiting...")
            time.sleep(60)
            return self.send_message(message, system_prompt)
            
        except openai.error.InvalidRequestError as e:
            # Try fallback model
            try:
                response = openai.ChatCompletion.create(
                    model=self.config.fallback_model,
                    messages=messages,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature
                )
                
                return {
                    "response": response.choices[0].message.content,
                    "model_used": self.config.fallback_model,
                    "tokens_used": response.usage.total_tokens,
                    "status": "fallback_used",
                    "original_error": str(e)
                }
            except Exception as fallback_error:
                return {
                    "error": f"Both models failed: {str(e)}, {str(fallback_error)}",
                    "status": "failed"
                }
        
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }

class WebhookServer:
    def __init__(self, gpt_bridge: GPTAPIBridge, port: int = 5000):
        self.app = Flask(__name__)
        self.gpt_bridge = gpt_bridge
        self.port = port
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/webhook/gpt', methods=['POST'])
        def gpt_webhook():
            data = request.json
            message = data.get('message', '')
            system_prompt = data.get('system_prompt', '')
            
            result = self.gpt_bridge.send_message(message, system_prompt)
            return jsonify(result)
        
        @self.app.route('/webhook/health', methods=['GET'])
        def health_check():
            return jsonify({"status": "healthy", "service": "GPT API Bridge"})
        
        @self.app.route('/webhook/config', methods=['POST'])
        def update_config():
            data = request.json
            # Update configuration dynamically
            if 'api_key' in data:
                self.gpt_bridge.config.openai_api_key = data['api_key']
                openai.api_key = data['api_key']
            if 'model' in data:
                self.gpt_bridge.config.model = data['model']
            if 'rate_limit' in data:
                self.gpt_bridge.rate_limiter = RateLimiter(data['rate_limit'])
            
            return jsonify({"status": "config_updated"})
    
    def run(self, debug=False):
        self.app.run(host='0.0.0.0', port=self.port, debug=debug)

# Example usage and testing
if __name__ == "__main__":
    # Load config from file or environment
    config = APIConfig(
        openai_api_key="your-api-key-here",  # Replace with actual key
        model="gpt-4",
        max_tokens=4000,
        temperature=0.7,
        rate_limit_rpm=60
    )
    
    # Initialize bridge
    bridge = GPTAPIBridge(config)
    
    # Start webhook server
    server = WebhookServer(bridge, port=5000)
    
    print("GPT API Bridge starting on port 5000...")
    print("Webhook endpoint: http://localhost:5000/webhook/gpt")
    print("Health check: http://localhost:5000/webhook/health")
    
    server.run(debug=True)

