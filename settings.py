BOT_NAME = 'monitor'
SPIDER_MODULES = [
    'monitor'
]
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': 'postgres',
    'database': 'price_monitor'
}
ITEM_PIPELINES = {
    'pipelines.PriceMonitorPipeline': 300
}
