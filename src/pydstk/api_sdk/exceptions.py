class DstkSdkError(Exception):
    pass


class ResourceFetchingError(DstkSdkError):
    pass


class ResourceCreatingError(DstkSdkError):
    pass


class ResourceCreatingDataError(ResourceCreatingError):
    pass
