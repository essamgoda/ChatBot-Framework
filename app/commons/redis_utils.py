import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""

# The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
# using the default encoding utf-8.  This is client specific.
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
