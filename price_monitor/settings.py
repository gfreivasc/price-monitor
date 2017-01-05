BOT_NAME = 'price_monitor'
SPIDER_MODULES = [
    'price_monitor.spiders.monitors'
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
    'price_monitor.pipelines.PriceMonitorPipeline': 300
}
