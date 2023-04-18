import logging
import time


def create_metric(value, metric_type='RATE'):
    """
    Create a metric dictionary to be sent for monitoring tools.
    """
    return {'value': value, 'type': metric_type}


class BaseHandler:
    def __init__(self):
        """
        Base handler class wrapping custom handlers.
        """
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.health_check_message = 'health_check'

    def serve_request(self, event, context):
        """
        Actual request served by child class.

        This method should return:
        result
        """
        raise NotImplementedError()

    def add_metadata(self, payload, metrics, duration_ms):
        """
        Parse metadata from response and add to payload
        """
        # Init payload metadata
        payload['metadata'] = {}

        # Add metrics for monitoring
        metrics['time_duration'] = create_metric(value=duration_ms)
        metrics['num_requests'] = create_metric(value=1, metric_type='COUNT')
        payload['metadata']['metrics'] = metrics

        return payload

    def prepare_metrics(self, _):
        """
        Child classes can override this to parse metrics for monitoring at run time
        """
        return {}

    def handle_request(self, event, context):
        """
        Handle request wrapping individual handlers.

        Expected model handler response
        result - json output the model's handler returns to be passed on to client
        """
        # Catch ping
        if event.get('action', None) == self.health_check_message:
            return {'status': 200}

        # Execute the handler
        try:
            # Start timer
            start_ms = time.time()
            # Serve the request
            results = self.serve_request(event, context)
            # Prepare metrics
            metrics = self.prepare_metrics(results)
            # Get wallclock time metrics
            duration_ms = time.time() - start_ms
        except Exception as e:
            self.logger.error(e.__class__.__name__)
            message = f'{e.__class__.__name__} when calling handler'
            self.logger.error(message)

            # Return a brief error message
            return {'message': message, 'status': 500}

        # Return result
        results = self.add_metadata(results, metrics, duration_ms)
        return results
