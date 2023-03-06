from fastapi import FastAPI

from containers import AdaptersLayer, BusinessLayer, FrameworksLayer, SystemConfiguration


def create_app() -> FastAPI:
    system_configuration = SystemConfiguration.initialize()
    framework_layer = FrameworksLayer.initialize(config=system_configuration.config)
    adapters_layer = AdaptersLayer(frameworks=framework_layer)
    BusinessLayer(adapters=adapters_layer)
    return framework_layer.api_app()


app = create_app()
