"""
Health Check Endpoint
Required for CI/CD pipeline smoke tests
"""

from flask import jsonify
import os
import sys

# Add to your app.py


def register_health_check(app):
    """Register health check endpoint"""
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint for monitoring and CI/CD
        Returns system status and component health
        """
        
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {}
        }
        
        # Check AI providers
        try:
            from backend.src.init_free_ai import ai_manager
            if ai_manager and ai_manager.providers:
                health_status['components']['ai_providers'] = {
                    'status': 'healthy',
                    'count': len(ai_manager.providers),
                    'providers': list(ai_manager.providers.keys())
                }
            else:
                health_status['components']['ai_providers'] = {
                    'status': 'degraded',
                    'message': 'No AI providers configured'
                }
        except Exception as e:
            health_status['components']['ai_providers'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
        
        # Check cache
        try:
            from backend.src.response_cache import response_cache
            cache_stats = response_cache.get_stats()
            health_status['components']['cache'] = {
                'status': 'healthy',
                'backend': cache_stats['backend'],
                'hit_rate': cache_stats['hit_rate']
            }
        except Exception as e:
            health_status['components']['cache'] = {
                'status': 'degraded',
                'error': str(e)
            }
        
        # Check environment
        health_status['components']['environment'] = {
            'status': 'healthy',
            'python_version': sys.version,
            'use_free_ai': os.getenv('USE_FREE_AI', 'false')
        }
        
        # Overall status
        component_statuses = [
            comp['status'] 
            for comp in health_status['components'].values()
        ]
        
        if 'unhealthy' in component_statuses:
            health_status['status'] = 'unhealthy'
            status_code = 503
        elif 'degraded' in component_statuses:
            health_status['status'] = 'degraded'
            status_code = 200
        else:
            health_status['status'] = 'healthy'
            status_code = 200
        
        return jsonify(health_status), status_code
    
    @app.route('/ready', methods=['GET'])
    def readiness_check():
        """
        Readiness check - is the app ready to serve traffic?
        """
        try:
            # Check if critical components are ready
            from backend.src.init_free_ai import ai_manager
            
            if not ai_manager or not ai_manager.providers:
                return jsonify({
                    'ready': False,
                    'message': 'AI providers not initialized'
                }), 503
            
            return jsonify({
                'ready': True,
                'message': 'Application is ready'
            }), 200
            
        except Exception as e:
            return jsonify({
                'ready': False,
                'error': str(e)
            }), 503
    
    @app.route('/live', methods=['GET'])
    def liveness_check():
        """
        Liveness check - is the app alive?
        """
        return jsonify({
            'alive': True,
            'timestamp': datetime.now().isoformat()
        }), 200
