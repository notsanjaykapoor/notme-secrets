import sqlmodel

import models
import services.convs.reqs


def restart_list(db_session: sqlmodel.Session, offset: int = 0, limit: int = 50) -> list[models.ConvReq]:
    """
    Get conversation requests in cancelled state.
    """
    reqs_struct = services.convs.reqs.list(
        db_session=db_session, query=f"state:{models.conv_req.STATE_CANCELLED}", offset=offset, limit=limit
    )
    return reqs_struct.objects
