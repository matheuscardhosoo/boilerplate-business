from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from business.use_cases import CheckHealthInputPort, CheckHealthUseCase
from containers import BusinessLayer

from .interfaces import OutputDTO

router = APIRouter(tags=["System State"])


class HealthCheckOutputDTO(OutputDTO):
    """OutputDTO for receive_and_reply example."""

    response: str


@router.get("/health_check", response_model=HealthCheckOutputDTO)
@inject
async def health_check(
    use_case: CheckHealthUseCase = Depends(Provide[BusinessLayer.check_health]),
) -> HealthCheckOutputDTO:
    """Check if the system is running OK."""
    input_port = CheckHealthInputPort()
    output_port = await use_case.execute(input_port)
    return HealthCheckOutputDTO(response=output_port.response)
