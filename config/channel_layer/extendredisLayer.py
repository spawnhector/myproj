from channels_redis.core import RedisChannelLayer
import time
class ExtendedRedisChannelLayer(RedisChannelLayer):

    def __init__(self, *args, **kwargs):
        super(ExtendedRedisChannelLayer, self).__init__(*args, **kwargs)
        self.group_channels = ''

    async def get_group_channels(self, group):
        assert self.valid_group_name(group), "Group name not valid"
        key = self._group_key(group)
        connection = self.connection(self.consistent_hash(group))
        # Discard old channels based on group_expiry
        await connection.zremrangebyscore(
            key, min=0, max=int(time.time()) - self.group_expiry
        )
        return [x.decode("utf8") for x in await connection.zrange(key, 0, -1)]

    async def is_group_exists(self,group_name):
        self.group_channels = await self.get_group_channels(group_name)
        if self.group_channels.__len__() > 0:
            return True
        return False

    async def get_group_channel(self):
        return self.group_channels[0]
