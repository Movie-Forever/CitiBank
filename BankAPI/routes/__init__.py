"""Routes package"""
from flask import Blueprint

# Import blueprints
from .customers import customers_bp
from .accounts import accounts_bp

__all__ = ['customers_bp', 'accounts_bp']
