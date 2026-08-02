```hls

type WORKER_C
group Collision

import math
import objects as obj
import error
import systemutils as su        


TASK Collision:Initialize (poolmanager) -> null {
    create process pm_access = poolmanager.Asklink()                        # Only allowed because type is a _C variant

    if (pm_access.tick() == true) {
        set TASK.status 1
    } else {
        set TASK.status 0
        set flag error.sworker.TaskTickFailure(pm_access)
    }

}

SubTASK Collision:CheckCollision(EntityListId, PlayerId) -> bool {
    entity_list = pm_access.get(EntityListId) as su.types.array
    clutch playerData = pm_access.get(PlayerId) as su.types.struct

    for (id <- Entity; id++) {
        if ((Entity[id].pos as v3) == (playerData.position as v3)) {
            return true
        }
    }

    return false
}




```