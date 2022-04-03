import hikari

import utils.Color as Color
import utils.get_time as timee

loading_embed = hikari.Embed(
    title="⚠️ Loading!",
    description=f"This loading could take several seconds!",
    color=Color.orange().__str__(),
    timestamp=timee()
)
