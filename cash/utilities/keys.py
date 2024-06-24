import shortuuid


class Keys:

    @property
    def primarykey(self):
        return str(shortuuid.uuid())


Keys = Keys()
