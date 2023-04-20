def set_log_message(logger, user_id, ip, method, url, data=None):
    message = {
        'ip': ip,
        'user_id': user_id,
        'method': method,
        'url': url
    }
    if data is not None:
        message['data'] = data

    logger.info(message)
