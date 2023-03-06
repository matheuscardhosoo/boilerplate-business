from business.use_cases.interfaces import InputPort, OutputPort, UseCase


class CheckHealthInputPort(InputPort):
    """InputPort for CheckHealthUseCase."""


class CheckHealthOutputPort(OutputPort):
    """OutputPort for CheckHealthUseCase."""

    response: str


class CheckHealthUseCase(UseCase):
    """Use case that checks if the application is running correctly."""

    async def execute(self, _: CheckHealthInputPort) -> CheckHealthOutputPort:
        """Checks if the application is running correctly."""
        return CheckHealthOutputPort(response="I'm good!")
